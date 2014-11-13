#coding=utf-8
#以字典形式，读取后用conf中文件名来找到具体的路径
import sys

def config(fn):
    with open(fn,"rb") as infile:
        result = {}
        for line in infile.readlines():
            if len(line) < 4 or line[0] == "#":
                pass
            else:
                sp = line.split()
                result[sp[0]] = sp[2]
    infile.close()
    return result
