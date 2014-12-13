
文件说明：

conf/dp.conf ： 所有数据文件或者结果存放的路径设置，由readconf.py解析
data/× ： 人民日报语料和gb/lex存放
result/× ： 分词统计后的unigram和bgram的统计和最后的word_dict/py_dict等
pywork/ ： py_ngram.py 分词，统计词频 py_to_word.py 根据统计的词频实现音字转换 readconf.py 读取文档路径 word.py 定义的一个字类

使用说明：

具体使用时，只需讲conf/dp.conf 中的地址路径信息改为自己电脑存放的相应路径即可
然后进入pywork中，执行 $python py_to_word.py 按照输出要求输入即可
