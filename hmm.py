from __future__ import division
import sys

#1 将train文件中的词和tag分出来，并将句子开头结尾加上*和stop标记，方便统计count
def FRline(filetoread,n):
	try:
		infile = file(filetoread,"r")
	except IOError:
		sys.stderr.write("can not open the file")
		sys.exit(1)
	tlist = (n-1) * [[None,"*"]]
	fl = infile.readline()
	while fl:
		l = fl.strip()
		ntmp = 1
		if l:
			fline = l.split(" ")
			wtag = fline[-1]
			wd = " ".join(fline[:-1])
			tlist.append([wd,wtag])
		else:
			tlist.append([None,"STOP"])
			for i in xrange(n-1):
				tlist.append([None,"*"])
			ntmp += 1
		fl = infile.readline()
	tlist.append([None,"STOP"])
	return tlist

#2 计算出所有W-T对的个数，以及个数不大于5个的_Rare_类Word的Xlist
#W-T对与之后计算的1-gram组合可以计算出e(x|y)
def CountWTandX(wlist):
	wlen = len(wlist)
	WTdict = {}
	Xdict = {}
	Xlist = []
	for i in xrange(wlen):
		if wlist[i][0] in Xdict:
			Xdict[wlist[i][0]] += 1
		else:
			Xdict[wlist[i][0]] = 1
	for countx in Xdict:
		if Xdict[countx] >= 5:
			Xlist.append(countx)
	for i in xrange(wlen):
		if wlist[i][0] in Xlist:
			tmp = tuple(wlist[i])
		else:
			tmp = tuple(["_Rare_",wlist[i][1]])
		if tmp in WTdict:
			WTdict[tmp] += 1
		else:
			WTdict[tmp] = 1
	return WTdict,Xlist

#3 计算出n-gram的个数，方便计算条件概率p(y3|y1y2)
def CountNGram(wlist,n):
	wlen = len(wlist)
	WTdict,Xlist = CountWTandX(wlist)
	for j in xrange(wlen):
		if wlist[j][0] in Xlist:
			wlist[j][0] = wlist[j][0]
		else:
			wlist[j][0] = "_Rare_"
	NGramdict = {}
	for i in xrange(wlen - n + 2):
		tmpl = wlist[i:i+n]
		#1-gram
		if tmpl[0][1] in NGramdict:
			NGramdict[tmpl[0][1]] += 1
		else:
			NGramdict[tmpl[0][1]] = 1
		#2-gram
		if (tmpl[0][1],tmpl[1][1]) in NGramdict:
			NGramdict[(tmpl[0][1],tmpl[1][1])] += 1
		else:
			NGramdict[(tmpl[0][1],tmpl[1][1])] = 1
		#3-gram
		if i <= wlen -n:
			if(tmpl[0][1],tmpl[1][1],tmpl[2][1]) in NGramdict:
				NGramdict[(tmpl[0][1],tmpl[1][1],tmpl[2][1])] += 1
			else:
				NGramdict[(tmpl[0][1],tmpl[1][1],tmpl[2][1])] = 1
	return NGramdict,WTdict,Xlist

#4 条件概率p(y3|y1y2)计算
def Pyyy(y1,y2,y3,NGramdict):
	val = NGramdict[(y1,y2,y3)] / NGramdict[(y1,y2)]
	return val

#5 e(x|y)概率计算
def Exy(x,y,Xlist,NGramdict,WTdict):
	tmpval = 0
	if (x,y) in WTdict:
		tmpval = WTdict[(x,y)] / NGramdict[y]
	return tmpval

#6 标记预处理，将待标记的句子化成以STOP结尾的序列:
def TagPre(tagfile):
	try:
		tfile = file(tagfile,"r")
	except IOError:
		sys.stderr.write("error...")
		sys.exit(1)
	fl = tfile.readline()
	taglist = []
	while fl:
		f = fl.strip()
		if f:
			taglist.append(f)
		else:
			taglist.append("STOP")
		fl = tfile.readline()
	if taglist[-1] != "STOP":
		taglist.append("STOP")
	return taglist

#8 Refine the tagline..
def ReFine(Tlist,priorlist,k,tagn):
	taglist = ["I-GENE","O"]
	senlen = len(priorlist[0])
	tmpn = tagn
	tk = k - 1
	matchlist = []
	matchlist.insert(0,(Tlist[tk],taglist[priorlist[tmpn][senlen-1]]))
	while senlen > 1:
		tmpn = priorlist[tmpn][senlen-1]
		tk -= 1
		senlen -= 1
		matchlist.insert(0,(Tlist[tk],taglist[priorlist[tmpn][senlen-1]]))
	addwfile("gene.out",matchlist)

#9 write the result into the file.
def addwfile(outputfile,tlist):
	try:
		ofile = file(outputfile,"a")
	except IOError:
		sys.stderr.write("error..")
		sys.exit(1)
	for i in tlist:
		ofile.write("%s %s\n"%(i[0],i[1]))
	ofile.write("\n")
	ofile.close()

#7 前进后退
def FandB(Tlist,Xlist,NGramdict,WTdict,N):
	priorlist = [[],[]]
	pi = [0,0]
	ppi = [0,0]
	taglist = ["I-GENE","O"]
	tmpj = 0
	for k in xrange(len(Tlist)):
		if Tlist[k] in Xlist:
			tmpl = Tlist[k]
		else:
			tmpl = "_Rare_"
		if Tlist[k] == "STOP":
			for i in xrange(N-1):
				for j in xrange(N-1):
					if (j,i,"STOP") in NGramdict:
						tmpval = ppi[i] * Pyyy(taglist[j],taglist[i],"STOP",NGramdict)
						if tmpval > pi[0]:
							pi[0] = tmpval
							tmpj= i
			priorlist[0].append(tmpj)
			#这样，所有pi都算完了，该回溯了。	
			partlist = ReFine(Tlist,priorlist,k,0)
			priorlist = [[],[]]
			pi = [0,0]
			ppi = [0,0]
			tmpj = 0
		elif k == 0 or Tlist[k-1] == "STOP":
			for i in xrange(N-1):
				if ("*","*",taglist[i]) in NGramdict:
					tmpval = 1 * Pyyy("*","*",taglist[i],NGramdict) * Exy(tmpl,taglist[i],Xlist,NGramdict,WTdict)
					if tmpval > pi[i]:
						pi[i] = tmpval
			ppi = pi
			pi = [0,0]
		elif k == 1 or Tlist[k-2] == "STOP":
			for i in xrange(N-1):
				for j in xrange(N-1):
					if ("*",taglist[j],taglist[i]) in NGramdict:
						tmpval = ppi[j] * Pyyy("*",taglist[j],taglist[i],NGramdict) * Exy(tmpl,taglist[i],Xlist,NGramdict,WTdict)
						if tmpval >pi[i]:
							pi[i] = tmpval
							tmpj = j
				priorlist[i].append(tmpj)
			ppi = pi
			pi = [0,0]
		else:
			for i in xrange(N-1):
				for j in xrange(N-1):
					for m in xrange(N-1):
						if (taglist[m],taglist[j],taglist[i]) in NGramdict:
							tmpval = ppi[j] * Pyyy(taglist[m],taglist[j],taglist[i],NGramdict) * Exy(tmpl,taglist[i],Xlist,NGramdict,WTdict)
							if tmpval > pi[i]:
								pi[i] = tmpval
								tmpj = j
				priorlist[i].append(tmpj)
			ppi = pi
			pi = [0,0]
#10 写list与dict去文件
def DtoFile(gdict,outfile):
	try:
		ofile = file(outfile,"w")
	except IOError:
		sys.stderr.write("can not open the file")
		sys.exit(1)
	for words in gdict:
		ofile.write("%s:%s\n" % (words,gdict[words]))
	ofile.close()
def LtoFile(xlist,outfile):
	try:
		ofile = file(outfile,"w")
	except IOError:
		sys.stderr.write("Can not open the file")
		sys.exit(1)
	for listnode in xlist:
		ofile.write("%s\n"%listnode)
	ofile.close()

if __name__ == "__main__":
	wlist = FRline("gene.train",3)
	NGramdict,WTdict,Xlist = CountNGram(wlist,3)
	Tlist = TagPre("gene.dev")
	FandB(Tlist,Xlist,NGramdict,WTdict,3)
	
