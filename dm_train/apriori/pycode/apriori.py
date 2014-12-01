#coding=utf-8

'''
python code for apriori algorithm
python xx.py -f task_file
'''

from optparse import OptionParser
from read_conf import config
import itertools
import sys

'''
1:python 排列组合
import itertools
list(itertools.permutations([1,2,3,4],2))
将 1,2,3,4  全2排列 1,2 1,3 1,4, 2,1 2,3, ...顺序！
list(itertools.combinations([1,2,3,4],2))
组合！ 1,2 1,3, 1,4 2,3 2,4 3,4
2:计数
每次长度要记录，多维数组+dict！？
3:判断是否在task集合里，用set？！每个tast变成set，若是都在，就在
！用数组就好了！
'''

min_sup = 2

def c_to_l(c_dict,min_sup,times):
    if c_dict=={}:
        return {}
    l_dict = {}
    if times == 1:
        item_list = []
        for i in c_dict:
            if c_dict[i] >= min_sup:
                item_list.append(i)
                l_dict[i] = c_dict[i]
        return item_list,l_dict
    else:
        for i in c_dict:
            if c_dict[i] >= min_sup:
                l_dict[i] = c_dict[i]
        return l_dict

def get_task(path):
    task_list = []
    c_dict = {}
    with open(path,"rb") as infile:
        #get to work.
        firstline = 1
        tasks = infile.readlines()
        for line in tasks:
            if firstline:
                firstline = 0
                continue
            items = line.rstrip().split(',')
            task_list.append(items[1:])
            for i in items[1:]:
                if i in c_dict:
                    c_dict[i] += 1
                else:
                    c_dict[i] = 1
        infile.close()
    return task_list,c_dict

def get_ldict(task_list,com_list,min_sup,times):
    l_dict = {}
    for com in com_list:
        for task in task_list:
            is_in = 1
            for it in com:
                if it not in task:
                    is_in = 0
            if is_in:
                if com in l_dict:
                    l_dict[com] += 1
                else:
                    l_dict[com] = 1
    return c_to_l(l_dict,min_sup,times)

def get_rules(l_list):
    for l_dict in l_list[1:]:
        for item in l_dict:
            target_list = []
            for idx in item:
                target_list.append(idx)
            if len(target_list) == 2:
                get_double(target_list,l_list)
            else:
                get_multiple(target_list,l_list)

def get_double(target_list,l_list):
    print "           ---->{%s}<----         "%(target_list)
    tmp_sup = l_list[1][tuple(target_list)]*1.0 / len(l_list[0])
    tmp_conf = l_list[1][tuple(target_list)]*1.0 / l_list[0][target_list[0]]
    print "   %s  =>  %s     sup = %f     conf = %f"%(target_list[0],target_list[1],tmp_sup,tmp_conf)
    tmp_sup = l_list[1][tuple(target_list)]*1.0 / len(l_list[1])
    tmp_conf = l_list[1][tuple(target_list)]*1.0 / l_list[0][target_list[1]]
    print "   %s  =>  %s     sup = %f     conf = %f"%(target_list[1],target_list[0],tmp_sup,tmp_conf)

def get_multiple(target_list,l_list):
    print "           ---->{%s}<----     "%(target_list)
    m_len = len(target_list)-1
    com_list = list(itertools.combinations(target_list,m_len))
    for idx in com_list:
        target_task = get_rest_one(idx,target_list)
        tmp_sup = l_list[m_len][tuple(target_list)]*1.0 / len(l_list[m_len-1])
        tmp_conf = l_list[m_len][tuple(target_list)]*1.0 / l_list[m_len-1][tuple(idx)]
        print "%s => %s     sup = %f    conf = %f"%(idx,target_task,tmp_sup,tmp_conf)
        tmp_sup = l_list[m_len][tuple(target_list)]*1.0 / len(l_list[m_len-1])
        tmp_conf = l_list[m_len][tuple(target_list)]*1.0 / l_list[m_len-2][target_task]
        print "%s => %s     sup = %f    conf = %f"%(target_task,idx,tmp_sup,tmp_conf)

def get_rest_one(idx,target_list):
    tmp = ''
    for i in target_list:
        if i not in idx:
            return i

def main():
    parser = OptionParser()
    parser.add_option("-f","--filename",type="string",dest="file",default="DataBaseDB",help="NEED CORRECT PARAMETERS")
    (options,args) = parser.parse_args()
    if options.file == "error":
        print "hello world"
        sys.exit(1)
    task_file = options.file

    t_path = config("../conf/dp.conf")
    data_path = t_path["data_path"]

    L_list = []

    task_list,c_dict = get_task(data_path)
    item_list,l_dict = c_to_l(c_dict,min_sup,1)

    i_len = 1
    while l_dict != {}:
        L_list.append(l_dict)
        i_len += 1
        com_list = list(itertools.combinations(item_list,i_len))
        l_dict = get_ldict(task_list,com_list,min_sup,i_len)

    get_rules(L_list)

if __name__ == "__main__":
    main()
