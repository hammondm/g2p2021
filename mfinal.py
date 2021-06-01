# translate sigmorphon low-resource data for openNMT

# 100 in dev
# 800 in train
# 100 in test
# artificial half items added to train

# redistribute 80 from dev, to train

import sys,re

dirname = '2021-task1-main/data/low/'

pfx = sys.argv[1]

trainfile = pfx + '_train.tsv'
devfile = pfx + '_dev.tsv'
testfile = pfx + '_test.txt'

#################read dev items

f = open(dirname+devfile,'r')
t = f.read()
f.close()

t = t.split('\n')
t = t[:-1]

tmpdevset = [line.split('\t') for line in t]

#reserve 20 for dev
devreserve = []
devset = []
i = 0
while i < len(tmpdevset):
	if i % 5 == 0:
		devset.append(tmpdevset[i])
	else:
		devreserve.append(tmpdevset[i])
	i += 1

#write dev inputs
f = open('src-val.txt','w')
for pair in devset:
	item = ' '.join(list(pair[0]))
	f.write(f'{item}\n')
f.close()
#write dev outputs
f = open('tgt-val.txt','w')
for pair in devset:
	item = pair[1]
	f.write(f'{item}\n')
f.close()

##################################read trainfile

f = open(dirname+trainfile,'r')
t = f.read()
f.close()

t = t.split('\n')
t = t[:-1]

pairs = [line.split('\t') for line in t]

#use all items in train file for training plus dev reserve set
trainset = pairs + devreserve

#get all final letters and their correspondents
ends = {}
for pair in trainset:
	letter = pair[0][-1]
	symbol = pair[1].split(' ')[-1]
	if letter in ends:
		if symbol in ends[letter]:
			ends[letter][symbol] += 1
		else:
			ends[letter][symbol] = 1
	else:
		ends[letter] = {}
		ends[letter][symbol] = 1

#get just the unique word ends
newends = {}
for letter in ends:
	if len(ends[letter]) == 1:
		symbols = ends[letter]
		symbol = list(symbols.keys())[0]
		newends[letter] = symbol

#get all initial letters and their correspondents
beginnings = {}
for pair in trainset:
	letter = pair[0][0]
	symbol = pair[1].split(' ')[0]
	if letter in beginnings:
		if symbol in beginnings[letter]:
			beginnings[letter][symbol] += 1
		else:
			beginnings[letter][symbol] = 1
	else:
		beginnings[letter] = {}
		beginnings[letter][symbol] = 1

#get just the unique initial letters
newbeginnings = {}
for letter in beginnings:
	if len(beginnings[letter]) == 1:
		symbols = beginnings[letter]
		symbol = list(symbols.keys())[0]
		newbeginnings[letter] = symbol

#training item inputs as set
settrain = {pair[0] for pair in trainset}
#candidate items to add
newpairs = []

#get medial combinations for unique letters
for end in newends:
	endsym = newends[end]
	for beginning in newbeginnings:
		beginningsym = newbeginnings[beginning]
		wordpair = end + beginning
		transpair = ' ' + endsym + ' ' + beginningsym + ' '
		wordcount = 0
		transcount = 0
		candidates = []
		for pair in trainset:
			word = pair[0]
			trans = pair[1]
			if wordpair in word:
				wordcount += 1
				if transpair in trans:
					transcount += 1
					candidates.append(pair)
		if wordcount > 1 and wordcount == transcount:
			lefts = []
			rights = []
			for pair in candidates:
				word = pair[0]
				trans = pair[1]
				leftword = re.sub(end+beginning+'.*$',end,word)
				rightword = re.sub('^.*'+end+beginning,beginning,word)
				lefttrans = re.sub(endsym+' '+beginningsym+'.*$',endsym,trans)
				righttrans = re.sub(
					'^.*'+endsym+' '+beginningsym,
					beginningsym,
					trans
				)
				#print(leftword,rightword,lefttrans,righttrans)
				lefts.append((leftword,lefttrans))
				rights.append((rightword,righttrans))
			for left in lefts:
				newpair = (left[0],left[1])
				newpairs.append(newpair)
			for right in rights:
				newpair = (right[0],right[1])
				newpairs.append(newpair)

#add new items to trainset
maxnum = 0
for newpair in newpairs:
	word = newpair[0]
	if word not in settrain:
		maxnum += 1
		#if maxnum > 20: break
		trainset.append(newpair)
		settrain.add(word)

#training inputs
f = open('src-train.txt','w')
for pair in trainset:
	item = ' '.join(list(pair[0]))
	f.write(f'{item}\n')
f.close()
#training outputs
f = open('tgt-train.txt','w')
for pair in trainset:
	item = pair[1]
	f.write(f'{item}\n')
f.close()


#read test file
f = open(dirname+testfile,'r')
t = f.read()
f.close()

t = t.split('\n')
t = t[:-1]
pairs = t

#test inputs
f = open('src-test.txt','w')
for pair in pairs:
	item = ' '.join(list(pair))
	f.write(f'{item}\n')
f.close()

