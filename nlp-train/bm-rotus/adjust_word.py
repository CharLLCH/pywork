#coding=utf-8

import pickle
import os
import nltk
import csv
from read_conf import config
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.decomposition import PCA

cat_dic = {'acq':0,'corn':1,'crude':2,'earn':3,'grain':4,'interest':5,'money-fx':6,'ship':7,'trade':8,'wheat':9}

t_path = config("../conf/dp.conf")
train_path = t_path["train_path"]
test_path = t_path["test_path"]

def handle_doc(word_set,rs_path):
    doc_dir = os.listdir(rs_path)
    doc_matrix = []
    doc_cat = []
    for docs in doc_dir:
        files = os.listdir(rs_path+docs)
        print "start to handle the -->  "+docs
        for file_d in files:
            d_path = rs_path+docs+'/'+file_d
            #get the single file path
            with open(d_path,'rb') as text_file:
                str_tmp = ''
                file_lines = text_file.readlines()
                for line in file_lines:
                    pattern = r'''[a-zA-Z]+'''
                    tokens = nltk.regexp_tokenize(line,pattern)
                    for t in tokens:
                        if t.lower() in word_set:
                            str_tmp += t.lower()
                            str_tmp += ' '
                doc_matrix.append(str_tmp)
                doc_cat.append(cat_dic[docs])
            text_file.close()
    str_tmp = ''
    for sw in word_set:
        str_tmp += sw
        str_tmp += ' '
    doc_matrix.append(str_tmp)
    doc_cat.append('NAN')
    vectorizer = CountVectorizer()
    doc_num = vectorizer.fit_transform(doc_matrix)
    tfidf = TfidfTransformer()
    doc_tfidf = tfidf.fit_transform(doc_num)
    return doc_tfidf[:-1,:],doc_cat[:-1]

def get_wset(path):
    with open(path,'rb') as infile:
        reader = csv.reader(infile)
        tmp = []
        for i in reader:
            tmp = i
            break
        return set(tmp)

def save_matrix(path,matrix):
    outfile = open(path,'wb')
    pickle.dump(matrix,outfile,True)

if __name__ == "__main__":
    word_set = get_wset(t_path["wordset_path"])
    tr_m,tr_c = handle_doc(word_set,train_path)
    te_m,te_c = handle_doc(word_set,test_path)
    save_matrix(t_path['train_matrix'],tr_m)
    save_matrix(t_path['train_cat'],tr_c)
    save_matrix(t_path['test_matrix'],te_m)
    save_matrix(t_path['test_cat'],te_c)
    logreg = linear_model.LogisticRegression(C=8.5)
    logreg.fit(tr_m,tr_c)
    test_pre = logreg.predict(te_m)
    '''
    neigh = KNeighborsClassifier(n_neighbors=8,weights='distance')
    neigh.fit(tr_m,tr_c)
    test_pre = neigh.predict(te_m)
    '''
    succ_num = 0
    for i in range(len(test_pre)):
        if te_c[i] == test_pre[i]:
            succ_num += 1
    print "Acc : %lf"%(1.0*succ_num/len(te_c)*100)
