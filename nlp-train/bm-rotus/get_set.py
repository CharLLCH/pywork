#coding=utf-8
#to get the word_set and something else.
from word import word
from stopword import stop_set
from read_conf import config
import os
import nltk
import csv

cat_dic = {'acq':0,'corn':1,'crude':2,'earn':3,'grain':4,'interest':5,'money-fx':6,'ship':7,'trade':8,'wheat':9}

t_path = config("../conf/dp.conf")
train_path = t_path["train_path"]
test_path = t_path["test_path"]
wordset_path = t_path["wordset_path"]

stopword = stop_set(t_path["stopword_path"])
pattern = r'''[a-zA-Z]+'''

def get_num():
    num_set = {}
    doc_num = 0
    doc_dir = os.listdir(train_path)
    for dd in doc_dir:
        f_list = os.listdir(train_path+dd)
        num_set[cat_dic[dd]] = len(f_list)
        doc_num += len(f_list)
    return num_set,doc_num
        

def get_set(doc_num,num_set):
    word_set = {}
    doc_dir = os.listdir(train_path)
    w_dict = {}
    for dd in doc_dir:
        f_list = os.listdir(train_path+dd)
        print "get in the --->   "+dd+"  <---"
        for fpath in f_list:
            d_path = train_path+dd+'/'+fpath
            with open(d_path,"rb") as d_file:
                list_tmp = []
                lines = d_file.readlines()
                for line in lines:
                    tokens = nltk.regexp_tokenize(line,pattern)
                    for t in tokens:
                        if t.lower() not in stopword:
                            list_tmp.append(t.lower())
                set_tmp = set(list_tmp)
                for w in set_tmp:
                    if w in word_set:
                        word_set[w].update_dict(cat_dic[dd])
                    else:
                        #superise! if I did not initial the dict, all will use the same dict!
                        word_set[w] = word(w,0,0,0,{cat_dic[dd]:1})
            d_file.close()
    #get the word_in_doc nums
    for idx in word_set:
        word_set[idx].get_docs()
        word_set[idx].get_widf(doc_num)
        word_set[idx].get_s(doc_num,num_set)
    return word_set

def set_save(word_set,N):
    tmp_set = {}
    for idx in word_set:
        tmp_set[idx] = word_set[idx].get_svalue()
    #dict sorted..
    tmp_tuple = sorted(tmp_set.iteritems(),key=lambda asd:asd[1],reverse=True)
    x_tmp = []
    #sorted 后变成tuple元祖了,tmp_tuple[i][0]存起来就好了
    num_save = min(N,len(word_set))
    for i in xrange(num_save):
        x_tmp.append(tmp_tuple[i][0])
    with open(wordset_path,'wb') as csv_file:
        w_ter = csv.writer(csv_file)
        w_ter.writerow(x_tmp)
    csv_file.close()


if __name__ == "__main__":
	num_set,doc_num = get_num()
	word_set = get_set(doc_num,num_set)
        set_save(word_set,3000)
