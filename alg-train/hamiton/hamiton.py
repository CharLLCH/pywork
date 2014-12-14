#coding=utf-8

import random
import numpy as np

INF = 1000
BOUNDVAL = 1000
PATHLINE = []

def inf_set(cost_matrix,n):
    for i in xrange(n):
        for j in xrange(n):
            if cost_matrix[i,j] > 900:
                cost_matrix[i,j] = INF

def initial_cost_matrix(n):
    random_val = [random.randint(0,100) for i in range(n**2)]
    cost_matrix = np.array(random_val).reshape(n,n)
    inf_set(cost_matrix,n)
    return cost_matrix

def checkout_matrix(c_matrix,n):
    cost_matrix = np.array([0]*n**2).reshape(n,n)
    for i in xrange(n):
        for j in xrange(n):
            cost_matrix[i,j] = c_matrix[i,j]
    #print "==> before the checkout <=="
    #print cost_matrix
    tmp_val = 0
    for idx in xrange(n):
        min_num = min(cost_matrix[idx,:])
        if min_num != 0 and min_num != INF:
            cost_matrix[idx,:] -= np.array([min_num]*n)
            inf_set(cost_matrix,n)
            tmp_val += min_num
    for idx in xrange(n):
        min_num = min(cost_matrix[:,idx])
        if min_num != 0 and min_num != INF:
            cost_matrix[:,idx] -= np.array([min_num]*n)
            inf_set(cost_matrix,n)
            tmp_val += min_num
    #print "==> after the checkout <=="
    #print cost_matrix
    return cost_matrix,tmp_val

def check_path(pathline,i,j):
    #test is there a circle?!
    path_dict = {}
    for idx in pathline:
        path_dict[idx[1]] = idx[2]
    path_dict[i] = j
    for idx in path_dict:
        Head = idx
        tmp = path_dict[Head]
        while tmp in path_dict:
            tmp = path_dict[tmp]
            if tmp == Head:
                return False
    return True

#get the 0's pos i row j col 's min's sum's max.
def get_the_edge(cost_matrix,n,path_line):
    tmp_edge = tuple([-1,-1,-1])
    for i_row in xrange(n):
        for j_col in xrange(n):
            if cost_matrix[i_row,j_col] == 0:
                tmp_row = [cost_matrix[i_row,idx] for idx in xrange(n) if idx != j_col]
                tmp_col = [cost_matrix[idx,j_col] for idx in xrange(n) if idx != i_row]
                tmp_val = min(tmp_row) + min(tmp_col)
                if tmp_val > tmp_edge[0] and tmp_val < INF and check_path(path_line,i_row,j_col):
                    tmp_edge = tuple([tmp_val,i_row,j_col])
                if tmp_val > INF and check_path(path_line,i_row,j_col):
                    tmp_edge = tuple([cost_matrix[i_row,j_col],i_row,j_col])
    return tmp_edge

def adjust_matrix(c_matrix,cut_edge,is_in,no_edge,n):
    cost_matrix = np.array([0]*n**2).reshape(n,n)
    for i in xrange(n):
        for j in xrange(n):
            cost_matrix[i,j] = c_matrix[i,j]
    i = cut_edge[1]
    j = cut_edge[2]
    if is_in:
        cost_matrix[j,i] = INF
        cost_matrix[i,:] = np.array([INF]*n)
        cost_matrix[:,j] = np.array([INF]*n)
        if no_edge == 0:
            cost_matrix[:,i] = np.array([INF]*n)
    else:
        cost_matrix[i,j] = INF
    return cost_matrix

def update_path(tmp_path,base_val):
    global BOUNDVAL,PATHLINE
    PATHLINE = [x for x in tmp_path]
    BOUNDVAL = base_val
    print PATHLINE,BOUNDVAL

def build_node(b_v,cost_matrix,path_line,n_e,n):
    global BOUNDVAL,PATHLINE
    no_edge = n_e
    base_val = b_v
    tmp_out_path = [x for x in path_line]
    tmp_in_path = [x for x in path_line]
    if no_edge == 0:
        if cost_matrix.min() == INF:
            return -1
        cost_matrix,tmp_val = checkout_matrix(cost_matrix,n)
        base_val += tmp_val
        cut_edge = get_the_edge(cost_matrix,n,path_line)
        if cut_edge[0] == -1 or cut_edge[1] == cut_edge[2]:
            return -1
        tmp_in_path.append(cut_edge)
        in_cmatrix = adjust_matrix(cost_matrix,cut_edge,True,no_edge,n)
        build_node(base_val,in_cmatrix,tmp_in_path,no_edge+1,n)
        #get the right i,j add value.
        out_cmatrix = adjust_matrix(cost_matrix,cut_edge,False,no_edge,n)
        build_node(base_val+cut_edge[0],out_cmatrix,tmp_out_path,no_edge,n)
    elif no_edge < n-1:
        cost_matrix,tmp_val = checkout_matrix(cost_matrix,n)
        base_val += tmp_val
        if base_val > BOUNDVAL:
            return -1
        if cost_matrix.min() == INF:
            return -1
        else:
            cut_edge = get_the_edge(cost_matrix,n,path_line)
            if cut_edge[0] == -1 or cut_edge[1] == cut_edge[2]:
                return -1
            tmp_in_path.append(cut_edge)
            in_cmatrix = adjust_matrix(cost_matrix,cut_edge,True,no_edge,n)
            build_node(base_val,in_cmatrix,tmp_in_path,no_edge+1,n)
            out_cmatrix = adjust_matrix(cost_matrix,cut_edge,False,no_edge,n)
            build_node(base_val+cut_edge[0],out_cmatrix,tmp_out_path,no_edge,n)
    else:
        if base_val < BOUNDVAL:
            print "Once Update the BOUNDVAL and PATHLINE"
            update_path(tmp_in_path,base_val)
            return 1
        else:
            return -1

if __name__ == "__main__":
    path_line = []
    base_val = 0
    no_edge = 0
    n = 8
    cost_matrix = initial_cost_matrix(n)
    print "====>  Initial the cost matrix  <==="
    build_node(base_val,cost_matrix,path_line,no_edge,n)
