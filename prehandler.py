from __future__ import division
#word:X->Y
class word(object):
	def __init__(self,name,wdict={}):
		self.name = name
		self.tdict = wdict
	def update(self,term,counts):
		self.tdict[term] = int(counts)
	def additem(self,term,counts):
		if term in self.tdict:
			self.tdict[term] += counts
		else:
			self.tdict[term] = counts
#gram:X->Y1Y2
class gram(object):
	def __init__(self,counts=0,strs=[]):
		self.counts = counts
		self.strs = strs
#nonterm:X
class nonterm(object):
	def __init__(self,name,counts=0):
		self.name = name
		self.counts = counts
#check if already exist.
def isexisted(wtlist,name):
	for i in xrange(0,len(wtlist)-1):
		if name == wtlist[i].name:
			return i
	return -1
#prehandle the word/gram/nonterm without the RARE.
words = []
nonterms = []
grams = []
with open("cfg.counts","r") as ifile:
	for fline in ifile.readlines():
		fl = fline.strip()
		sl = fl.split(" ")
		if sl[1] == 'UNARYRULE' and len(sl) != 0:
			name = sl[3]
			i = isexisted(words,name)
			if i == -1:
			#do not exist,add new word into words
				newWord = word(sl[3],{sl[2]:int(sl[0])})
				words.append(newWord)
			else:
			#existed,update.
				words[i].update(sl[2],sl[0])
		#NONTERMINAL&BINARYRULE has no same ones,so just addnew.
		elif sl[1] == 'NONTERMINAL' and len(sl) != 0:
			newNonterm = nonterm(sl[2],int(sl[0]))
			nonterms.append(newNonterm)
		elif sl[1] == 'BINARYRULE' and len(sl) != 0:
			newgram = gram(int(sl[0]),sl[2:])
			grams.append(newgram)
		else:
			print "There is something happending..."
ifile.close()
#Count one words counts.
def countword(someword):
	tmp = 0
	for non in someword.tdict:
		tmp += someword.tdict[non]
	return tmp
#take rare into consideration..
rarewords = []
rareitem = word("_RARE_",{})
rarewords.append(rareitem)
for w in words:
	if countword(w) < 5:
		#add the w's info to RARE.
		for its in w.tdict:
			rarewords[0].additem(its,w.tdict[its])
	else:
		rarewords.append(w)
#Now has the X,X->Y,X->Y1Y2 list nonterms,rarewords,grams
#q([x,y1,y2],grams,nonterms)=>compute the q(x->y1y2)
def q(xrules,nonterms):
	u = xrules
	d = xrules.strs[0]
	uc = xrules.counts
	dc = 0
	for non in nonterms:
		if non.name == d:
			dc = non.counts
			return 1.0 * uc / dc
	print "Stil has zeros.."
	return 0.0
#p([x.name,word[i]],rarewords,nonterms)=>compute the q(x->w)
def p(strs,rarewords,nonterms):
	u = strs
	d = strs[0]
	uc = 0
	dc = 0
	i = isexisted(rarewords,u[1])
	if i == -1:
		if u[0] in rarewords[0].tdict:
			uc = rarewords[0].tdict[u[0]]
		else:
			uc = 0
	else:
		if u[0] in rarewords[i].tdict:
			uc = rarewords[i].tdict[u[0]]
		else:
			uc = 0
	for non in nonterms:
		if non.name == d:
			dc = non.counts
			break
	return 1.0 * uc / dc
#test P(...)
'''
testmp = ['NOUN','WHO']
for x in nonterms:
	testmp = [x.name,'WHO']
	print p(testmp,rarewords,nonterms)
'''
#rlist[i][0]->y1 rlist[i][1]->y2
def xrule(x,grams):
	rlist = []
	for g in grams:
		if g.strs[0] == x.name:
			rlist.append(g.strs)
	return rlist
#Should I compute all rule-p now!?
rdict = {}
for r in grams:
	tmpr = tuple(r.strs)
	rdict[tmpr] = q(r,nonterms)

#Wordlist!
Wlist = []
with open("parse_dev.dat","r") as wfile:
	for wline in wfile.readlines():
		wl = wline.strip()
		wlt = wl.split(" ")
		Wlist.append(wlt)
wfile.close()
#'''
#Let's compute the dp..
for wlist in Wlist:
	pidict = {}
	bpdict = {}
	n = len(wlist)
	#Initialization..
	for i in xrange(n):
		for xn in nonterms:
			tmp = p([xn.name,wlist[i]],rarewords,nonterms)
			if tmp != 0:
				pidict[(i+1,i+1,xn.name)] = tmp 
	for l in xrange(1,n):
		for i in xrange(1,n-l):
			j = i + l
			tmpmax = 0
			tmps = 0
			tmpr = ""
			for x in nonterms:
				for r in xrule(x,grams):
					for s in xrange(i,j):
						if ((i,s,r[1]) in pidict) and ((s+1,j,r[2]) in pidict):
							tmp = rdict[tuple(r)] * pidict[(i,s,r[1])] * pidict[(s+1,j,r[2])]
							if tmp > tmpmax:
								tmpmax = tmp
								tmps = s
								tmpr = r
				if (i,j,x.name) in pidict:
					if tmpmax > pidict[(i,j,x.name)]:
						pidict[(i,j,x.name)] = tmpmax
						bpdict[(i,j,x.name)] = (tmpr,tmps)
				else:
					pidict[(i,j,x.name)] = tmpmax
					bpdict[(i,j,x.name)] = (tmpr,tmps)
	lmax = 0
	lx = []
	for nx in nonterms:
		if (1,n-1,nx.name) in pidict:
			if lmax < pidict[(1,n-1,nx.name)]:
				lmax = pidict[(1,n-1,nx.name)]
				lx = nx.name
	print lmax,lx
	print bpdict[(1,n-1,lx)]
	break
#'''
