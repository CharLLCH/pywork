#coding=utf-8

from read_conf import config
import jieba
import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

t_path = config('../conf/dp.conf')

def get_stop_list(path):
    stop_list = []
    with open(path,'rb') as infile:
        lines = infile.readlines()
        line_num = 1
        for line in lines:
            if line_num < 277:
                stop_list.append(line.rstrip().decode('gbk'))
                line_num += 1
            else:
                break
        infile.close()
    return stop_list

def get_word_pinyin_dict(path):
    word_dict = {}
    with open(path,'rb') as infile:
        lines = infile.readlines()
        for line in lines:
            str_tmp = line.rstrip().split('\t')
            word_dict[str_tmp[0].decode('gbk')] = get_pinyin(str_tmp[1:])
        infile.close()
    return word_dict

def get_pinyin(str_list):
    py_str = ''
    pyre = re.compile(r'''[a-z]+''')
    str_tmp = pyre.findall(str_list[0])
    for s_p in str_tmp:
        py_str += s_p
    return py_str

def get_ngram(path,word_dict,stop_list):
    doc_list = os.listdir(path)
    sw_dict = {}
    bw_dict = {}
    for doc in doc_list:
        str_tmp = ''
        file_path = path + doc
        with open(file_path,'rb') as infile:
            print "Handle the %s .."%file_path
            str_list = []
            lines = infile.readlines()
            for line in lines:
                str_tmp += line.rstrip().decode('gbk','ignore')
            infile.close()
            seg_list = list(jieba.cut(str_tmp,cut_all=False))
            for seg in seg_list:
                if seg in word_dict:
                    if seg in sw_dict:
                        sw_dict[seg] += 1
                    else:
                        sw_dict[seg] = 1
            for idx in xrange(len(seg_list)-1):
                if (seg_list[idx] in stop_list) or (seg_list[idx+1] in stop_list):
                    continue
                else:
                    tmp = seg_list[idx]+seg_list[idx+1]
                    if tmp in bw_dict:
                        bw_dict[tmp] += 1
                    else:
                        bw_dict[tmp] = 1
            infile.close()
    return sw_dict,bw_dict

def dict_to_file(word_dict,path):
    tmp_tuple = sorted(word_dict.iteritems(),key=lambda asd:asd[1],reverse=True)
    with open(path,'wb') as infile:
        for idx in xrange(len(word_dict)):
            str_tmp = str(tmp_tuple[idx][0])+'\t'+str(tmp_tuple[idx][1])+'\n'
            infile.write(str_tmp)
        infile.close()


if __name__ == "__main__":
    stop_list = get_stop_list(t_path['gb_path'])
    word_dict = get_word_pinyin_dict(t_path['lex_path'])
    sw_dict,bw_dict = get_ngram(t_path['text_path'],word_dict,stop_list)
    dict_to_file(sw_dict,t_path['sw_path'])
    dict_to_file(bw_dict,t_path['bw_path'])
