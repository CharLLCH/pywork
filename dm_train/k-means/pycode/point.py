#coding=utf-8

import math

'''
the class of the point that one point have the feat and the some func
'''

class point:
    def __init__(self,idx,x_pos = 0,y_pos = 0,k_cluster = 0):
        self.__idx = idx
        self.__x_pos = x_pos
        self.__y_pos = y_pos
        self.__k_cluster = k_cluster

    def get_pos(self):
        return self.__x_pos,self.__y_pos

    def get_cluster(self):
        return self.__k_cluster

    def update_cluster(self,new_cluster):
        self.__k_cluster = new_cluster

    def cal_dis(self,p):
        return math.sqrt((self.__x_pos-p[0])**2 + (self.__y_pos-p[1])**2)
