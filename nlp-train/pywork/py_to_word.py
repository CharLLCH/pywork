#coding=utf-8

import os
import sys
import pickle
from word import word
from read_conf import config

def py_to_word(py_str,py_dict,word_dict,num_sum,theta):
    py_str=py_str.lower()
    length_pin=len(py_str)
    keep_num=0
    if length_pin>50:
        keep_num=15 
    else:
        keep_num=20        
    dp_list=[[{} for j in xrange(length_pin)] for i in xrange(length_pin)]
    for i in xrange(length_pin):
        for j in xrange(length_pin-i):
            if py_dict.has_key(py_str[j:i+j+1]):
                for word in py_dict[py_str[j:i+j+1]]:
                    temp_list=[word,word,word_dict[word].freq]
                    dp_list[j][i+j][word]=temp_list
            for k in xrange(i):
                if dp_list[j][j+k]!={} and dp_list[j+k+1][j+i]!={}:
                    dict1=dp_list[j][j+k]
                    dict2=dp_list[j+k+1][j+i]
                    for key1 in dict1.keys():
                        for key2 in dict2.keys():
                            temp_string=key1+key2
                            temp_p=dict1[key1][2]/(word_dict[dict2[key2][0]].freq)
                            p_link=0
                            if word_dict[dict1[key1][1]].bigram.has_key(dict2[key2][0]):
                                p_link=word_dict[dict1[key1][1]].bigram[dict2[key2][0]]*(word_dict[dict1[key1][1]].freq**2)*word_dict[dict2[key2][0]].freq
                            else:
                                p_link=theta/(num_sum)*word_dict[dict1[key1][1]].freq*word_dict[dict2[key2][0]].freq
                            temp_p*=p_link*dict2[key2][2]
                            if dp_list[j][i+j].has_key(temp_string):
                                if dp_list[j][i+j][temp_string][2]<temp_p:
                                    dp_list[j][i+j][temp_string][2]=temp_p
                            else:
                                temp_list=[dict1[key1][0],dict2[key2][1],temp_p]
                                dp_list[j][i+j][temp_string]=temp_list
            if len(dp_list[j][i+j])>keep_num:
                temp_list=sorted(dp_list[j][i+j].keys(),key=lambda x:dp_list[j][i+j][x][2])[:-keep_num]
                for x in temp_list:
                    del(dp_list[j][i+j][x])
    return dp_list[0][length_pin-1]

def py_word_change(py_str):
    pyword_dict = py_to_word(py_str,py_dict,word_dict,num_sum,theta)
    tmp_list = sorted(pyword_dict.keys(),key=lambda x:pyword_dict[x][2],reverse=True)
    for idx in tmp_list:
        print (str(idx) + ' ' + str(pyword_dict[x][2])).decode('gbk').encode('utf-8')

if __name__ == "__main__":
    t_path = config('../conf/dp.conf')
    theta = 0.2
    print "Loading The Word And Pinyin Dataset"
    word_dict = pickle.load(open(t_path['word_path'],'rb'))
    py_dict = pickle.load(open(t_path['py_path'],'rb'))
    num_sum = pickle.load(open(t_path['num_path'],'rb'))
    print "@LOADED@"
    print "=========instructions==========="
    print "input the pinyin line and enter!"
    print "Q for exit the program and exit!"
    while True:
        line = sys.stdin.readline()
        if line.uper() == "Q\n":
            print "exiting the program.BYE"
            exit(0)
        else:
            test(line)
