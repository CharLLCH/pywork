#coding=utf-8

import sys
import matplotlib.pyplot as plt
import random
from datetime import datetime

COM_STR = ''

def get_LCS_matrix(a,b):
	len_a=len(a)
	len_b=len(b)
	c=[[0 for i in range(len_b+1)] for j in range(len_a+1)]
	flag=[[0 for i in range(len_b+1)] for j in range(len_a+1)]
	for i in range(len_a):
		for j in range(len_b):
			if a[i]==b[j]:
				c[i+1][j+1]=c[i][j]+1
				flag[i+1][j+1]='ok'
			elif c[i+1][j]>c[i][j+1]:
				c[i+1][j+1]=c[i+1][j]
				flag[i+1][j+1]='lf'
			else:
				c[i+1][j+1]=c[i][j+1]
				flag[i+1][j+1]='up'
	return c,flag

def get_com_LCS(flag,a,i,j):
    global COM_STR
    if i==0 or j==0:
        return
    if flag[i][j]=='ok':
        get_com_LCS(flag,a,i-1,j-1)
        COM_STR += a[i-1]
    elif flag[i][j]=='lf':
        get_com_LCS(flag,a,i,j-1)
    else:
        get_com_LCS(flag,a,i-1,j)

def print_LCS_matrix(cost_matrix,flag_matrix):
    for idx in cost_matrix:
        print "\t%s"%idx
    for idx in flag_matrix:
        print idx

def get_LCS_DC(a,b,a_pos,b_pos):
    if a_pos >= len(a) or b_pos >= len(b):
        return 0
    if a[a_pos] == b[b_pos]:
        return 1+get_LCS_DC(a,b,a_pos+1,b_pos+1)
    else:
        a_tmp = get_LCS_DC(a,b,a_pos+1,b_pos)
        b_tmp = get_LCS_DC(a,b,a_pos,b_pos+1)
        if a_tmp > b_tmp:
            return a_tmp
        else:
            return b_tmp

def random_str(random_length):
    ran_str = ''
    #chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    chars = 'ABCDEFGHIJKL'
    char_len = len(chars)
    for i in xrange(random_length):
        ran_str += chars[random.randint(0,char_len-1)]
    return ran_str

def plot_data(time_len):
    plt.figure(1)
    for idx in time_len:
        plt.plot(idx[0],idx[1],'o')
    plt.show()

def plot_double(dp_list,dc_list):
    plt.figure(2)
    for idx in dp_list:
        plt.plot(idx[0],idx[1],'ro')
    for idx in dc_list:
        plt.plot(idx[0],idx[1],'bo')
    plt.show()

if __name__ == "__main__":
    '''
    print "======>  LCS with DP  <========"
    print "==> Please Input the A_list <=="
    a_str = sys.stdin.readline().rstrip()
    print "==> Please Input the B_list <=="
    b_str = sys.stdin.readline().rstrip()
    print "@@=> A_str: %s <=@@=> B_str: %s <==@@"%(a_str,b_str)
    cost_matrix,flag_matrix = get_LCS_matrix(a_str,b_str)
    get_com_LCS(flag_matrix,a_str,len(a_str),len(b_str))
    print_LCS_matrix(cost_matrix,flag_matrix)
    print "===> The Longest Com Strs <==="
    print "========>  %s  <========"%(COM_STR)
    print "======>  LCS with DC  <========"
    a_list = list(a_str)
    b_list = list(b_str)
    print "@The Length Of The LCS is :==> %s <=="%(get_LCS_DC(a_list,b_list,0,0))
    '''
    n_times = 20
    n_length = [60*x for x in range(1,11)]
    s_length = [x for x in range(1,15)]
    dp_time_len = []

    for t in xrange(n_times):
        for len_t in n_length:
            print "===> No.%s times with Length.%s test! <==="%(t,len_t)
            COM_STR = ''
            str_1 = random_str(len_t)
            str_2 = random_str(len_t)
            print str_1
            print str_2
            print "---> start to DP method.."
            start_dp = datetime.now()
            cost_matrix,flag_matrix = get_LCS_matrix(str_1,str_2)
            get_com_LCS(flag_matrix,str_1,len(str_1),len(str_2))
            print "---> LCS : %s "%COM_STR
            time_tmp = datetime.now() - start_dp
            time_dp = time_tmp.microseconds + time_tmp.seconds * 1000
            dp_time_len.append(tuple([len_t,time_dp]))
            print "---> Time : %s "%time_dp
    print dp_time_len
    plot_data(dp_time_len)

    com_dp_list = []
    com_dc_list = []
    for t in xrange(n_times):
        for len_t in s_length:
            print "===> No.%s times with Length.%s test! <==="%(t,len_t)
            COM_STR = ''
            str_1 = random_str(len_t)
            str_2 = random_str(len_t)
            print str_1
            print str_2
            start_dp = datetime.now()
            cost_matrix,flag_matrix = get_LCS_matrix(str_1,str_2)
            get_com_LCS(flag_matrix,str_1,len(str_1),len(str_2))
            print "---> LCS : %s "%COM_STR
            print "---> start to DP method.."
            time_tmp = datetime.now() - start_dp
            time_dp = time_tmp.microseconds + time_tmp.seconds * 1000
            dp_time_len.append(tuple([len_t,time_dp]))
            print "---> Time : %s "%time_dp
            print "---> start to DC method.."
            start_dc = datetime.now()
            list_1 = list(str_1)
            list_2 = list(str_2)
            len_lcs = get_LCS_DC(list_1,list_2,0,0)
            time_dc = datetime.now() - start_dc
            time_dac = time_dc.microseconds + time_tmp.seconds * 1000
            print "---> LCS len: %s "%len_lcs
            print "---> Time : %s "%time_dac
            com_dp_list.append(tuple([len_t,time_dp]))
            com_dc_list.append(tuple([len_t,time_dac]))
    plot_double(com_dp_list,com_dc_list)
