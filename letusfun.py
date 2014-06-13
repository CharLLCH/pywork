from __future__ import division
import sys

def FRline(filetoread,n):
	try:
		infile = file(filetoread,"r")
	except IOError:
		sys.stderr.write("Can not open the file")
		sys.exit(1)
	tlist = (n - 1) * [[None,"*"]]
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

def CountX(wlen):
	wlen = len(wlist)
	xdict = {}
	xlist = []
	for i in xrange(wlen):
		if wlist[i][0] in xdict:
			xdict[wlist[i][0]] +=1
		else:
			xdict[wlist[i][0]] = 1
	for c in xdict:
		if xdict[c] <= 5:
			xlist.append(c)
	return xlist

def CountWTag(wlist):
	wlen = len(wlist)
	tdict = {}
	for i in xrange(wlen):
		tmp = tuple(wlist[i])
		if tmp in tdict:
			tdict[tmp] += 1
		else:
			tdict[tmp] = 1
	return tdict

def CGWithRare(wlist,n):
	wlen = len(wlist)
	xlist = CountX(wlist)
#print xlist
	for j in xrange(wlen):
		if wlist[j][0] in xlist:
			wlist[j][0] = "_Rare_"
#print j
	gdict = {}
	for i in xrange(wlen - n + 2):
		tmpl = wlist[i:i+n]
		#1-gram
		if tmpl[0][1] in gdict:
			gdict[tmpl[0][1]] += 1
		else:
			gdict[tmpl[0][1]] = 1
		#2-gram
		if (tmpl[0][1],tmpl[1][1]) in gdict:
			gdict[(tmpl[0][1],tmpl[1][1])] += 1
		else:
			gdict[(tmpl[0][1],tmpl[1][1])] = 1
		#3-gram
		if i <= wlen - n:
			if (tmpl[0][1],tmpl[1][1],tmpl[2][1]) in gdict:
				gdict[(tmpl[0][1],tmpl[1][1],tmpl[2][1])] += 1
			else:
				gdict[(tmpl[0][1],tmpl[1][1],tmpl[2][1])] = 1
	if '*' in gdict:
		del gdict['*']
	if ('STOP','*','*') in gdict:
		del gdict[('STOP','*','*')]
	if 'STOP' in gdict:
		del gdict['STOP']
	if ('I-GENE','STOP','*') in gdict:
		del gdict[('I-GENE','STOP','*')]
	if ('STOP','*') in gdict:
		del gdict[('STOP','*')]
	if ('O','STOP','*') in gdict:
		del gdict[('O','STOP','*')]
	return gdict,xlist

def LtoFile(xlist,outfile):
	try:
		ofile = file(outfile,"w")
	except IOError:
		sys.stderr.write("Can not open the file")
		sys.exit(1)
	for listnode in xlist:
		ofile.write("%s\n"%listnode)
	ofile.close()

def DtoFile(gdict,outfile):
	try:
		ofile = file(outfile,"w")
	except IOError:
		sys.stderr.write("can not open the file")
		sys.exit(1)
	for words in gdict:
		ofile.write("%s:%s\n" % (words,gdict[words]))
	ofile.close()

def exy(totagterm,ytotag,gdict,tdict):
	tmpvalue = 0
	if totagterm in tdict:
		tmpl = totagterm
	else:
		tmpl = "_Rare_"
	if (tmpl,ytotag) in tdict:
		tmpvalue = (tdict[(tmpl,ytotag)] / gdict[ytotag])
	else:
		tmpvalue = 0
	return tmpvalue

def pyyy(y1,y2,y3,gdict):
	val = gdict[(y1,y2,y3)] / gdict[(y1,y2)]
	return val

def prehandle(totagfile):
	try:
		ttagfile = file(totagfile,"r")
	except IOError:
		sys.stderr.write("error..")
		sys.exit(1)
	fl = ttagfile.readline()
	filelist = []
	filelist.append('*')
	filelist.append('*')
	while fl:
		f = fl.strip()
		if len(filelist) != 0:
			if filelist[-1] == 'STOP':
				filelist.append('*')
				filelist.append('*')
		if f:
			filelist.append(f)
		else:
			filelist.append('STOP')
		fl = ttagfile.readline()
	if filelist[-1] != 'STOP':
		filelist.append('STOP')
	return filelist
	
def addwfile(outputfile,tlist):
	try:
		ofile = file(outputfile,"w+")
	except IOError:
		sys.stderr.write("error..")
		sys.exit(1)
	for i in tlist:
		ofile.write("%s %s\n"%(i[0],i[1]))
	ofile.write("\n")
	ofile.close()

def refindline(priorlist,tolist,k,tmpln):
	taglist = ['*','STOP','I-GENE','O']
	senlen = len(priorlist[0])
	matchlist = []
	tmpn = tmpln
	tk = k-1
	while senlen > 0:
		matchlist.insert(0,(tolist[tk],taglist[(priorlist[tmpn][senlen-1])]))
		senlen -= 1
		tk -= 1
		tmpn = priorlist[tmpn][senlen]
	addwfile("test.out",matchlist)
	
def FandB(tolist,gdict,tdict):
	priorlist = [[],[],[],[]]
	pit = [0,0,0,0]
	pitp = [0,0,0,0]
	tmpj = 0
	taglist = ['*','STOP','I-GENE','O']
	taglen = len(taglist)
	for k in xrange(len(tolist)):
		if tolist[k] in tdict:
			tmpl = tolist[k]
		else:
			tmpl = "_Rare_"
		if tolist[k] == 'STOP':
			for i in taglist:
				for j in taglist:
					if (j,i,'STOP') in gdict:
						tmpval = pitp[taglist.index(i)] * pyyy(j,i,'STOP',gdict)
						if tmpval > pit[taglist.index(i)]:
							pit[taglist.index(i)] = tmpval
							tmpj = taglist.index(j)
				priorlist[taglist.index(i)].append(tmpj)
			tmpn = 0
			tmpln = 0
			for n in xrange(taglen):
				if tmpn < priorlist[n][-1]:
					tmpn = priorlist[n][-1]
					tmpln = n
			refindline(priorlist,tolist,k,tmpln)
			priorlist = [[],[],[],[]]
			pit = [0,0,0,0]
			pitp = [0,0,0,0]
			tmpval = 0
		elif tolist[k] == '*':
			pit = [0,0,0,0]
			pitp = pit
		else:
			if tolist[k-2] == '*':
				if tolist[k-1] == '*':
					for i in taglist:
						if ('*','*',i) in gdict:
							tmpval = 1 * pyyy('*','*',i,gdict) * exy(tolist[k],i,gdict,tdict)
							if tmpval > pit[taglist.index(i)]:
								pit[taglist.index(i)] = tmpval
					pitp = pit
					pit = [0,0,0,0]
				else:
					for i in taglist:
						for j in taglist:
							if ('*',j,i) in gdict:
								tmpval = pitp[taglist.index(j)] * pyyy('*',j,i,gdict) * exy(tolist[k],i,gdict,tdict)
								if tmpval > pit[taglist.index(i)]:
									pit[taglist.index(i)] = tmpval
									tmpj = taglist.index(j)
						priorlist[taglist.index(i)].append(tmpj)
					pitp = pit
					pit = [0,0,0,0]
			else:
				for i in taglist:
					for j in taglist:
						for m in taglist:
							if (m,j,i) in gdict:
								tmpval = pitp[taglist.index(j)] * pyyy(m,j,i,gdict) * exy(tolist[k],i,gdict,tdict)
								if tmpval > pit[taglist.index(i)]:
									pit[taglist.index(i)] = tmpval
									tmpj = taglist.index(j)
					priorlist[taglist.index(i)].append(tmpj)
				pitp = pit
				pit = [0,0,0,0]

if __name__ == "__main__" :
	wlist = FRline("gene.train",3)
	(gdict,xlist) = CGWithRare(wlist,3)
	tdict = CountWTag(wlist)
	totag = prehandle("gene.dev")
	FandB(totag,gdict,tdict)
#tagdict = exy("gene.dev",gdict,tdict)
#DtoFile(tagdict,"genedevtest.txt")
#gdict=>(y1,y2..) n-gram's Nums
#tdict=>(x,y):num  x tagged as y's num
#xlist=>the x that is translate as _Rare_
#wlist=>have handled with the rare x list
#	LtoFile(xlist,"Listout.txt")
#	DtoFile(gdict,"Gramout.txt")
#	DtoFile(tdict,"WTagout.txt")
