#coding=utf-8
import os
import nltk
import csv
from read_conf import config
from sklearn import linear_model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from math import log

'''
most terrible thing is that using a total str to generate the word_set!
'''
'''
1.根据training_set & test_set抽取出词表voclist
ps:突然发现，如果用nltk，训练前不用自己抽词表，只要按照词表的正则式，
将文章seg成list就好，它在统计时需要记录tf值，而不是单纯用1来表示，
词表我觉得如果Q2是相同的话，只在test=>seg_matrix时，需要有个限定，
不能单纯用test中的文章生成tf-idf矩阵！
2.根据词表，将training的文章word_seg出来，转化成seg_word_list
3.利用nltk将文章_词矩阵转化成tf-idf矩阵，记得记录类别vector
4.训练，然后将同理得到的test文章进行预测
'''

'''
Q1:voclist只包含trainingset
yes!regardless of the missing ones.
Q2:全集同的情况下，然后对于不同的word_seg_list，最后得到的词频矩阵的feat顺序是一样的么？
yes! the same order!
'''

'''
sklearn出来的稀疏存储可以直接用的哦～
'''

#路径以及分类字典，都写成conf型，暂时dict先不写啦，直接给出了
cat_dic = {'acq':0,'corn':1,'crude':2,'earn':3,'grain':4,'interest':5,'money-fx':6,'ship':7,'trade':8,'wheat':9,'NAN':10}

t_path = config("../conf/dp.conf")
train_path = t_path["train_path"]
test_path = t_path["test_path"]


#根据path信息，得到所有的文档，然后依次处理，得到最终的词表
#先简单的tokenize吧，暂且不考虑那些奇怪的存在
#因为training下又有很多类别，所以两次listdir才找到具体的文件
#vocset:table of word.  train_matrix:[[seg_words]s]. train_cat:[doc's cate]
def doc_to_voclist(tr_path,te_path):
    docdir_list = os.listdir(tr_path)
    vocset = set([])
    vocset = vocset_init(vocset,te_path)
    doc_matrix = []
    train_cat = []
    for dd in docdir_list:
        file_list = os.listdir(tr_path+dd)
        print "start to handle the train_set--> "+dd+" <-- directory.."
        for fpath in file_list:
            #get all the filepath start to handle the document, remember to close it.
            d_path = tr_path+dd+'/'+fpath
            vocset,doc_matrix,train_cat = doc_handle(vocset,doc_matrix,train_cat,d_path,dd)
    str_tmp = ''
    for sw in vocset:
        str_tmp += sw
        str_tmp += ' '
    doc_matrix.append(str_tmp)
    train_cat.append(10)
    vectorizer = CountVectorizer()
    doc_m = vectorizer.fit_transform(doc_matrix)
    tfidf = TfidfTransformer()
    train_matrix = tfidf.fit_transform(doc_m)
    #train_matrix = log_sparsematrix(train_matrix)
    return vocset,train_matrix,train_cat

#sparse matrix .log()
def log_sparsematrix(t_matrix):
    non_pos = np.nonzero(t_matrix)
    for i in xrange(len(non_pos[0])):
        t_matrix[non_pos[0][i],non_pos[1][i]] = log(t_matrix[non_pos[0][i],non_pos[1][i]])
    return t_matrix

#to add the test set voc.
def vocset_init(vocset,te_path):
    #vocset empty set of the voc.
    doc_list = os.listdir(te_path)
    for dd in doc_list:
        file_list = os.listdir(te_path+dd)
        print "start to handle the test_set--> "+dd+" <-- directory.."
        for fpath in file_list:
            d_path = te_path+dd+'/'+fpath
            with open(d_path,"rb") as t_file:
                fl = t_file.readlines()
                for doc_line in fl:
                    str_tmp = ''
                    pattern = r'''[a-zA-Z]+'''
                    tokens = nltk.regexp_tokenize(doc_line,pattern)
                    words = set([t.lower() for t in tokens])
                    vocset = vocset | words
            t_file.close()
    return vocset

#处理某个文档，获得其中词表中没有的词，充实词表
def doc_handle(voclist,doc_matrix,doc_cat,docpath,cat):
    with open(docpath,"rb") as text_file:
        fl = text_file.readlines()
        str_tmp = ''
        #porter = nltk.PorterStemmer()
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
        doc_matrix.append(str_tmp)
        doc_cat.append(cat_dic[cat])
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
        print "handling the---> "+dd+" <---directory.."
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
    test_cat.append(10)
    vectorizer = CountVectorizer()
    doc_m = vectorizer.fit_transform(test_m)
    tfidf = TfidfTransformer()
    test_matrix = tfidf.fit_transform(doc_m)
    #test_matrix = log_sparsematrix(test_matrix)
    return test_matrix,test_cat

if __name__ == "__main__":
    #处理trainingset获得wordset
    word_set,train_matrix,train_cat = doc_to_voclist(train_path,test_path)
    test_matrix,test_cat = test_handle(word_set,test_path)
    logreg = linear_model.LogisticRegression(penalty='l2')
    logreg.fit(train_matrix[:-1,:],train_cat[:-1])
    test_pre = logreg.predict(test_matrix[:-1,:])
    succ_num = 0
    for i in range(len(test_cat)-1):
        if test_cat[i] == test_pre[i]:
            succ_num += 1
    print succ_num
    print "  succ  in  "
    print len(test_cat)
