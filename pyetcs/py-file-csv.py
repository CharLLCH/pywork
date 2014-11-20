#coding=utf-8
'''
#coding=utf-8
import csv
reader(csvfile[,dialect='excel'][,fmtparam])
csvfile:支持迭代的对象，每次调用next返回值是string，通常的file对象或者list对象都适用，如果是文件对象，打开需要加"b"标志参数
dialect:编码风格，默认excel方式，也就是逗号分隔的，另外支持excel-tab分隔，tab分隔的
fmtparam：格式化参数，用来覆盖之前dialect对象制定的编码风格
eg:
    import csv

    reader = csv.reader(file('yourfile','rb'))
    for line in reader:
        print line

writer(csvfile[,dialect='excel'][,fmtparam])
eg:
    import csv

    writer = csv.writer(file('yourfile','rb'))
    writer.writerow(['column1','column2','column3'])
    lines = [range(3) for i in range(5)]
    for line in lines:
        writer.writerow(line)


DictReader:和reader差不多，会生成一个字典类型返回，而不是迭代类型

DictWriter:普通的writer你需要手动去创建一个列表，但是有时候我们得到的是一个dict类型数据，可以直接把字典用DictWriter来写入csv
eg:
    import csv

    fieldnames = ['column1','column2']
    dict_writer = csv.DictWriter(file('yourfile','wb'),fieldnames=fieldnames)
    dict_writer.writerow(fieldnames)
    dict_writer.writerow(rows)

    rows = [{'column1':0,'column2':1},
            {'column1':1,'column2':2}]
'''

'''
import csv

reader = csv.reader(file('yourfile','rb'))

for line in reader:
    if reader.line_num == 1:
        continue
        #line is a list
        type = line[0]

writer = csv.writer(open('yourfile','wb'),quoting=csv.QUOTE_ALL)

writer.writerow(['12','21'])
writer.writerow([["12","21"]])
'''

'''
import csv

with open('file','rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row

import csv
with open('file','wb') as f:
    writer = csv.writer(f,delimiter=' ',qiotechar='|',quoting=csv.QUOTE_ALL)
    writer.writerow(['a','s'])
    ...
    #在一个单元格中

    writer = csv.writer(csvfile,dialect='excel')
    writer.writerow(['a','b'])
    ...
    #分别写在两个单元格中

'''
