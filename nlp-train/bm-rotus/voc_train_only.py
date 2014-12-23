#coding=utf-8

import pickle
import os
import nltk
import csv
import numpy as np
from read_conf import config
from sklearn import linear_model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.decomposition import PCA
from logistic_nd import LogisticRegression

'''
1.根据trainingset抽取出词表voclist
ps:突然发现，如果用nltk，训练前不用自己抽词表，只要按照词表的正则式，
将文章seg成list就好，它在统计时需要记录tf值，而不是单纯用1来表示，
词表我觉得如果Q2是相同的话，只在test=>seg_matrix时，需要有个限定，
不能单纯用test中的文章生成tf-idf矩阵！
2.根据词表，将training的文章word_seg出来，转化成seg_word_list
3.利用nltk将文章_词矩阵转化成tf-idf矩阵，记得记录类别vector
4.训练，然后将同理得到的test文章进行预测

Q1:voclist只包含trainingset
yes!regardless of the missing ones.
Q2:全集同的情况下，然后对于不同的word_seg_list，最后得到的词频矩阵的feat顺序是一样的么？
yes! the same order!
sklearn出来的稀疏存储可以直接用的哦～应该-应该！

Get the word_set and learn to build sparse matrix to generate the vector without add the totalvector!
'''

#路径以及分类字典，都写成conf型，暂时dict先不写啦，直接给出了
cat_dic = {'acq':0,'corn':1,'crude':2,'earn':3,'grain':4,'interest':5,'money-fx':6,'ship':7,'trade':8,'wheat':9}

t_path = config("../conf/dp.conf")
train_path = t_path["train_path"]
test_path = t_path["test_path"]


#根据path信息，得到所有的文档，然后依次处理，得到最终的词表
#先简单的tokenize吧，暂且不考虑那些奇怪的存在
#因为training下又有很多类别，所以两次listdir才找到具体的文件
#vocset:table of word.  train_matrix:[[seg_words]s]. train_cat:[doc's cate]
def doc_to_voclist(tr_path):
    docdir_list = os.listdir(tr_path)
    vocset = set([])
    doc_matrix = []
    train_cat = []
    for dd in docdir_list:
        file_list = os.listdir(tr_path+dd)
        print "start to handle the -->   "+dd+"   <-- directory.."
        for fpath in file_list:
            #get all the filepath start to handle the document, remember to close it.
            d_path = tr_path+dd+'/'+fpath
            vocset,doc_matrix,train_cat = doc_handle(vocset,doc_matrix,train_cat,d_path,dd)
    vectorizer = CountVectorizer()
    doc_m = vectorizer.fit_transform(doc_matrix)
    tfidf = TfidfTransformer()
    train_matrix = tfidf.fit_transform(doc_m)
    return vocset,train_matrix,train_cat


#处理某个文档，获得其中词表中没有的词，充实词表
def doc_handle(voclist,doc_matrix,doc_cat,docpath,cat):
    with open(docpath,"rb") as text_file:
        fl = text_file.readlines()
        str_tmp = ''
        for doc_line in fl:
            #tokens = nltk.word_tokenize(doc_line)
            pattern = r'''[a-zA-Z]+'''
            #tokens for set but besides for the seg_matrix.
            tokens = nltk.regexp_tokenize(doc_line,pattern)
            for t in tokens:
                str_tmp += t.lower()
                str_tmp += ' '
            words = set([t.lower() for t in tokens])
            voclist = voclist | words
        doc_cat.append(cat_dic[cat])
        doc_matrix.append(str_tmp)
    text_file.close()
    return voclist,doc_matrix,doc_cat

#test的tf-idf获取，撇去不在vocset里的
#Attention:可是！最终得到的seg doc的词表feature不够数...怎么办...
def test_handle(word_list,tr_path):
    docdir_list = os.listdir(tr_path)
    test_m = []
    test_cat = []
    for dd in docdir_list:
        file_list = os.listdir(tr_path+dd)
        print "handling the --->   "+dd+"   <--- directory.."
        for fpath in file_list:
            d_path = tr_path + dd + '/' + fpath
            with open(d_path,"rb") as text_file:
                str_tmp = ''
                test_cat.append(cat_dic[dd])
                fl = text_file.readlines()
                test_por = nltk.PorterStemmer()
                for doc_line in fl:
                    pattern = r'''[a-zA-Z]+'''
                    tokens = nltk.regexp_tokenize(doc_line,pattern)
                    for t in tokens:
                        if t.lower() in word_list:
                            str_tmp += t.lower()
                            str_tmp += ' '
                test_m.append(str_tmp)
            text_file.close()
    #最后增加一维把所有的wordset加进去？！try once!
    str_tmp = ''
    for sw in word_list:
        str_tmp += sw
        str_tmp += ' '
    test_m.append(str_tmp)
    test_cat.append('NAN')
    vectorizer = CountVectorizer()
    doc_m = vectorizer.fit_transform(test_m)
    tfidf = TfidfTransformer()
    test_matrix = tfidf.fit_transform(doc_m)
    return test_matrix,test_cat

def save_matrix(path,matrix):
    outfile = open(path,'wb')
    pickle.dump(matrix,outfile,True)

def rebuild(cat_list):
    if set(cat_list) == 2:
        return np.matrix(np.array(tr_cat).reshape(len(tr_cat),1))
    else:
        cat_num = len(set(cat_list))
        tmp = np.matrix([0]*len(cat_list)*cat_num).reshape(len(cat_list),cat_num)
        for idx in xrange(len(cat_list)):
            tmp[idx,cat_list[idx]] = 1
        return tmp

def get_pred(pred):
    y_list = []
    for n_idx in xrange(pred.shape[0]):
        tmp_max = 0
        tmp_idx = 0
        for c_idx in xrange(pred.shape[1]):
            if pred[n_idx,c_idx] > tmp_max:
                tmp_max = pred[n_idx,c_idx]
                tmp_max = c_idx
        y_list.append(tmp_max)
    return y_list

if __name__ == "__main__":
    #处理trainingset获得wordset
    word_set,train_matrix,train_cat = doc_to_voclist(train_path)
    #save_matrix(t_path['train_matrix'],train_matrix)
    #save_matrix(t_path['train_cat'],train_cat)
    test_matrix,test_cat = test_handle(word_set,test_path)
    #save_matrix(t_path['test_matrix'],test_matrix[:-1,:])
    #save_matrix(t_path['test_cat'],test_cat[:-1])

    logreg = LogisticRegression(0.5,0,0)
    tr_matrix = np.matrix(train_matrix.toarray())
    tr_cat = rebuild(train_cat)
    logreg.fit(tr_matrix,tr_cat)
    te_matrix = np.matrix(test_matrix[:-1,:].toarray())
    te_cat = rebuild(test_cat[:-1])
    pred_y = logreg.predict(te_matrix)
    test_pre = get_pred(pred_y)


    #logreg = linear_model.LogisticRegression()
    #logreg.fit(train_matrix,train_cat)
    #test_pre = logreg.predict(test_matrix[:-1,:])
    #neigh = KNeighborsClassifier(n_neighbors=8)
    #neigh.fit(train_matrix,train_cat)
    #test_pre = neigh.predict(test_matrix[:-1,:])
    succ_num = 0
    for i in range(len(test_pre)):
        if test_cat[i] == test_pre[i]:
            succ_num += 1
    print succ_num
    print "  succ  in  "
    print len(test_cat[:-1])
