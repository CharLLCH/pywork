#coding=utf-8

import random
import numpy as np

INF = 1000

def inf_set(cost_matrix,n):
    for i in xrange(n):
        cost_matrix[i,i] = INF

def initial_cost_matrix(n):
    random_val = [random.randint(0,100) for i in range(n**2)]
    cost_matrix = np.array(random_val).reshape(n,n)
    inf_set(cost_matrix,n)
    return cost_matrix

def checkout_matrix(cost_matrix,n):
    tmp_val = 0
    for idx in xrange(n):
        min_num = min(cost_matrix[idx,:])
        if min_num != 0:
            cost_matrix[idx,:] -= np.array([min_num]*n)
            tmp_val += min_num
    for idx in xrange(n):
        min_num = min(cost_matrix[:,idx])
        if min_num != 0:
            cost_matrix[:,idx] -= np.array([min_num]*n)
            tmp_val += min_num
    inf_set(cost_matrix,n)
    return cost_matrix,tmp_val

def get_second_min(row_list,row_idx,n):
    tmp_min = 101
    for idx in xrange(n):
        if row_list[idx] < tmp_min and row_list[idx] != 0:
            tmp_min = row_list[idx]
            tmp_pos = idx 
    return tmp_min,row_idx,tmp_pos

def get_the_edge(cost_matrix,n):
    edge_tmp = tuple([0,0])
    min_list = [get_second_min(cost_matrix[idx,:],idx,n) for idx in range(n)]
    min_edge = max(min_list)
    return min_edge

def adjust_matrix(cost_matrix,cut_edge,is_in,n):
    i = cut_edge[1]
    j = cut_edge[2]
    if is_in:
        cost_matrix[j,i] = INF
        cost_matrix[i,:] = np.array([INF]*n)
        cost_matrix[:,j] = np.array([INF]*n)
    else:
        cost_matrix[i,j] = INF

if __name__ == "__main__":
    cost_matrix = initial_cost_matrix(8)
    cost_matrix,tmp_val = checkout_matrix(cost_matrix,8)
    print cost_matrix
    cut_edge = get_the_edge(cost_matrix,8)
    print cut_edge
    adjust_matrix(cost_matrix,cut_edge,False,8)
    print cost_matrix
