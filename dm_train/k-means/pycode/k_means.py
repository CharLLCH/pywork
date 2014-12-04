#coding=utf-8

'''
python code for k-means algorithm.
python xx.py -n NUM_OF_POIONTs -k NUM_OF_CLUSTER
parser.add_option("-x","-x_full",action="default is store",type="string/int/float",dest="options.xxx xxx is dest",default="default val",help="..")
'''
from point import point
from optparse import OptionParser
import matplotlib.pyplot as plt
import sys
import random

#according to the -n to create the point_list, randrange(k): 0-k-1 k-val
def initial_points(n,k):
    pos_dict = {}
    point_list = []
    for idx in xrange(n):
        if idx >= 0:
            x_tmp = random.randrange(200)
            y_tmp = random.randrange(200)
            s_tmp = str(x_tmp)+'-'+str(y_tmp)
            while s_tmp in pos_dict:
                x_tmp = random.randrange(200)
                y_tmp = random.randrange(200)
                s_tmp = str(x_tmp)+'-'+str(y_tmp)
            pos_dict[s_tmp] = 1
            point_list.append(point(idx,x_tmp,y_tmp,random.randrange(k)))
        else:
            x_tmp = random.randrange(200)
            y_tmp = random.randrange(200)
            s_tmp = str(x_tmp)+'-'+str(y_tmp)
            while s_tmp in pos_dict:
                x_tmp = random.randrange(200)
                y_tmp = random.randrange(200)
                s_tmp = str(x_tmp)+'-'+str(y_tmp)
            pos_dict[s_tmp] = 1
            point_list.append(point(idx,x_tmp,y_tmp,idx))
    return point_list 

#according to the -k to initial the k random cluster, immediately initial with the random cluster.
#use the dict {cluster:[x_sum,y_sum,num_c]} to cal the point
def get_cluster_point(p_list,n,k):
    p_dict = {}
    for c in xrange(k):
        p_dict[c] = [0,0,0]
    for idx in xrange(n):
        tmp_x,tmp_y = p_list[idx].get_pos()
        tmp_c = p_list[idx].get_cluster()
        p_dict[tmp_c][0] += tmp_x
        p_dict[tmp_c][1] += tmp_y
        p_dict[tmp_c][2] += 1
    for c in xrange(k):
        if p_dict[c][2] != 0:
            p_dict[c][0] = p_dict[c][0]*1.0 / p_dict[c][2]
            p_dict[c][1] = p_dict[c][1]*1.0 / p_dict[c][2]
        else:
            print "too little point",c
    return p_dict

#according to the p_dict to cal new cluster.
def get_new_cluster(p_list,p_dict,n,k):
    for idx in xrange(n):
        tmp_min = 500
        tmp_clu = 0
        for c in xrange(k):
            tmp_d = p_list[idx].cal_dis(p_dict[c])
            if tmp_d < tmp_min:
                tmp_min = tmp_d
                tmp_clu = c
        p_list[idx].update_cluster(tmp_clu)

#cal the SSE
def get_SSE(p_list,p_dict,n,k):
    tmp_sse = 0
    for idx in xrange(n):
        tmp_sse += (p_list[idx].cal_dis(p_dict[p_list[idx].get_cluster()]))
    return tmp_sse

#ploting..
'''
import matplotlib.pyplot as plt

'o' to be the point
color: b-blue, g-green, r-red, c-cyan, m-magenta, y-yellow, k-black, w-white
mark: s-square, *-star! +-+! x-X!
'''
def point_plot(p_list,p_dict,color_dict,mark_dict):
    plt.figure(1)
    for p in p_list:
        x,y = p.get_pos()
        c = p.get_cluster()
        plt.plot(x,y,color_dict[c%8])
    for c in p_dict:
        plt.plot(p_dict[c][0],p_dict[c][1],mark_dict[c%8])
    plt.show()


#one pic but sub nine.
def init_sub_plot():
    plt.figure(1)
    ax = []
    for i in xrange(9):
        ax.append(plt.subplot(3,3,i+1))
    return ax

def sub_plot(p_list,p_dict,ax,color_dict,mark_dict):
    plt.figure(1)
    plt.sca(ax)
    for p in p_list:
        x,y = p.get_pos()
        c = p.get_cluster()
        plt.plot(x,y,color_dict[c%8])
    for c in p_dict:
        plt.plot(p_dict[c][0],p_dict[c][1],mark_dict[c%8])

#to get the parameter of the n and k
def main():

    color_dict = {0:'ob',1:'og',2:'or',3:'oc',4:'om',5:'oy',6:'ok',7:'ow'}
    mark_dict = {0:'b*',1:'g*',2:'r*',3:'c*',4:'m*',5:'y*',6:'k*',7:'w*'}

    parser = OptionParser()
    parser.add_option("-n","--n-number",type="int",dest="number",default=-1,help="hello, please input the correct parameters.")
    parser.add_option("-k","--k-cluster",type="int",dest="cluster",default=-1,help="hello, please input the correct parameters.")
    parser.add_option("-p","--plot",type="string",dest="plot",default="sub-plot",help="hello, please input the correct parameters")

    (options,args) = parser.parse_args()

    if options.number == -1 or options.cluster == -1:
        print "hello world"
        sys.exit(1)

    n = options.number
    k = options.cluster
    p = options.plot

    p_list = initial_points(n,k)
    p_dict = get_cluster_point(p_list,n,k)
    if p == "sub-plot":
        ax = init_sub_plot()
        sub_plot(p_list,p_dict,ax[0],color_dict,mark_dict)
        for i in xrange(8):
            get_new_cluster(p_list,p_dict,n,k)
            p_dict = get_cluster_point(p_list,n,k)
            sub_plot(p_list,p_dict,ax[i+1],color_dict,mark_dict)
        plt.figure(1)
        plt.show()
    else:
        point_plot(p_list,p_dict,color_dict,mark_dict)
        for i in xrange(8):
            get_new_cluster(p_list,p_dict,n,k)
            p_dict = get_cluster_point(p_list,n,k)
            point_plot(p_list,p_dict,color_dict,mark_dict)

if __name__ == "__main__":
    main()
