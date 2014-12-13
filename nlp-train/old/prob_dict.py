#coding=utf-8

def file_to_dict(path):
    with open(path,'rb') as infile:
        lines = infile.readlines()
        for line in lines:
            str_tmp = line.rstrip().split('\t')
            word = str_tmp[0].decode('gbk','ignore')
            num = int(str_tmp[1])
            print word,num

if __name__ == "__main__":
    file_to_dict('../result/bw_dict.txt')
