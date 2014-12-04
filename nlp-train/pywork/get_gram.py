#coding=utf-8

import jieba
from read_conf import config
import codecs
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#python str default is ascii decode, is conflict with unicode

t_path = config("../conf/dp.conf")
ws_path = t_path["gb_path"]
lex_path = t_path["lex_path"]
text_path = t_path["text_path"]

#get the single word_voc
def get_word_set(path):
    seg_set = []
    with open(path,"rb") as in_file:
        lines = in_file.readlines()
        for line in lines:
            str_tmp = line.rstrip().decode('gbk')
            seg_set.append(str_tmp)
        in_file.close()
    return seg_set

def get_words_set(path):
    seg_set = []
    seg_dict = {}
    with open(path,"rb") as in_file:
        lines = in_file.readlines()
        for line in lines:
            str_tmp = line.rstrip().split('\t')
            #seg_set.append(str_tmp[0].decode('gbk'))
            seg_dict[str_tmp[0].decode('gbk')] = str_tmp[1:] 
        #return seg_set,seg_dict
        return seg_dict
'''
def get_d_s(path):
    doc_list = os.listdir(path)
    vocset = set([])
    for dd in doc_list:
        str_tmp = ''
        file_path = path+dd
        data = open(file_path).read()
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
        print file_path
        data.decode('gbk')
'''

def get_doc_set(path,dicts,lists):
    doc_list = os.listdir(path)
    voc_dict = {}
    for dd in doc_list:
        str_tmp = ''
        file_path = path + dd
        with open(file_path,'rb') as infile:
            print "start to handle the file : %s "%(file_path)
            str_len = 0
            str_list = []
            lines = infile.readlines()
            for line in lines:
                str_tmp += line.rstrip().decode('gbk')
            infile.close()
            seg_list = jieba.cut(str_tmp,cut_all=False)
            #get the s_gram word
            for seg in seg_list:
                if (seg in dicts) or (seg in lists):
                    str_list.append(seg)
                    str_len += 1
                    if seg in voc_dict:
                        voc_dict[seg] += 1
                    else:
                        voc_dict[seg] = 1
            #get the b_gram word.
            for idx in xrange(str_len-1):
                tmp = str_list[idx]+str_list[idx+1]
                if tmp in dicts:
                    if tmp in voc_dict:
                        voc_dict[tmp] += 1
                    else:
                        voc_dict[tmp] = 1
    return voc_dict

def word_laplace(voc_dict,word_dict,word_list):
    for i in word_dict:
        if i not in voc_dict:
            voc_dict[i] = 1
    for i in word_list:
        if i not in voc_dict:
            voc_dict[i] = 1
    return voc_dict

if __name__ == "__main__":
    #x = u"阿"
    #sw_list:just has the single word, dw_dict is the dict that has pronouncation.
    sw_list = get_word_set(ws_path)
    dw_dict = get_words_set(lex_path)
    #single word dict, to store each word's appearance times.
    voc_dict = get_doc_set(text_path,dw_dict,sw_list)
    voc_dict = word_laplace(voc_dict,dw_dict,sw_list)
