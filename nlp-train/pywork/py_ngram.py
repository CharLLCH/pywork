#coding=utf-8

from read_conf import config
from word import word
import re
import os
import pickle

t_path = config('../conf/dp.conf')

#get the word_dict that is the dictionary of the word and words.
#just use the lex.txt without the gb.txt
def get_word_dict(path):
    with open(path['lex_path'],'r') as infile:
        word_dict = {}
        py_dict = {}
        for line in infile.readlines():
            str_tmp = line.rstrip().split('\t')
            word_dict[str_tmp[0]] = word(str_tmp[0],{},0)
            py_tmp = get_pinyin(str_tmp[1:])
            if py_tmp in py_dict:
                py_dict[py_tmp].append(str_tmp[0])
            else:
                py_dict[py_tmp] = [str_tmp[0]]
        infile.close()
    print "Have got the word dict"
    #max_len = max(len(x) for x in word_dict)
    return word_dict,py_dict

#rebuild the wo3 shi4 => woshi
def get_pinyin(str_list):
    py_str = ''
    pyre = re.compile(r'''[a-z]+''')
    str_tmp = pyre.findall(str_list[0])
    for s_p in str_tmp:
        py_str += s_p
    return py_str

#get the unigram and the bgrams.
#store in dict of a class of word.
def get_seg(word_dict,path,MAX_LEN):
    doc_str = ''
    for doc in os.listdir(path['text_path']):
        with open(path['text_path']+doc,'r') as infile:
            print "strat to handler -->  %s <-- "%doc
            for str_line in infile.readlines():
                doc_str += str_line.rstrip().decode('gbk','ignore')
            infile.close()
        senre = re.compile(ur'''[\u4e00-\u9fa5]''')
        sen_list = senre.findall(doc_str)
        doc_str = doc_str.replace('\n','')
        sen_list = [s.encode('gbk') for s in sen_list if s != u'']
        for sent in sen_list:
            sent_len = len(sent)
            end = sent_len
            if sent_len <= MAX_LEN:
                begin = 0
            else:
                begin = end-MAX_LEN
            tmp_word_list = []
            while end != 0:
                if sent[begin:end] in word_dict:
                    word_len = end - begin
                    #word_dict[sent[begin:end]].times += 1
                    word_dict[sent[begin:end]].update_times(1)
                    tmp_word_list.append(sent[begin:end])
                    end = begin
                    if end - MAX_LEN <= 0:
                        begin = 0
                    else:
                        begin = end -MAX_LEN
                else:
                    if begin+2 == end:
                        end = begin
                        if end - MAX_LEN <= 0:
                            begin = 0
                        else:
                            begin = end - MAX_LEN
                    else:
                        begin += 2
            if len(tmp_word_list) >= 1:
                tmp_word_list.reverse()
                for x in xrange(len(tmp_word_list)-1):
                    word_dict[tmp_word_list[x]].update_dict(tmp_word_list[x+1])
    return True

#output the ug/bg-ram dict.
def dict_to_file(word_dict,path):
    print "start to write the dict to file!"
    tmp_list = sorted(word_dict.keys(),key=lambda x:word_dict[x].times,reverse=True)
    with open(path['sw_path'],'w') as outfile:
        for w in tmp_list:
            outfile.write(word_dict[w].word+'\t'+str(word_dict[w].times)+'\n')
        outfile.close()
    tmp_dict = {}
    for key in word_dict:
        if len(word_dict[key].bgram) == 0:
            continue
        for bg in word_dict[key].bgram:
            tmp_dict[key+' '+bg] = word_dict[key].bgram[bg]
    tmp_list = sorted(tmp_dict.keys(),key = lambda x:tmp_dict[x],reverse=True)
    with open(path['bw_path'],'w') as outfile:
        for x in tmp_list:
            outfile.write(x + ' ' + str(tmp_dict[x]) + '\n')
        outfile.close()

#laplace smoothing : just find the possibile bgram not in the word.bg add it.
#Actually we can add it in the py_to_word func when you meet a bg, both single of them in the word dict,
#but it does not!
def lap_smooth(word_dict):
    for idx_1 in word_dict:
        for idx_2 in word_dict:
            if idx_2 != idx_1:
                word_dict[idx_1].update_bgram(idx_2)

def dict_to_pickle(word_dict,py_dict,num_sum,path):
    with open(path['word_path'],'rb') as outfile:
        pickle.dump(word_path,outfile)
        outfile.close()
    with open(path['py_path'],'rb') as outfile:
        pickle.dump(py_dict,outfile)
        outfile.close()
    with open(path['num_path'],'rb') as outfile:
        pickle.dum(num_sum,outfile)
        outfile.close()

if __name__ == "__main__":
    word_dict,py_dict = get_word_dict(t_path)
    num_sum = get_seg(word_dict,t_path,6)
    dict_to_file(word_dict,t_path)
    dict_to_pickle(word_dict,py_dict,num_sum,t_path)
