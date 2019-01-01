from collections import namedtuple, defaultdict
from numpy import mean, zeros
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import subprocess
import re
import emoji 
import os
import os.path
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import pickle 
import utils

RT = "./"
BROWNCLUSFILE = RT+"model/resources/browncluster.txt"
STOPWORDS = stopwords
POSITIVE = RT + "model/resources/positive-words.txt"
NEGATIVE =RT + "model/resources/negative-words.txt"

# default name entities.
NER_title = {'ORGANIZATION':0, "PERCENT":1, 'PERSON':2, 'DATE':3, 'MONEY':4, 'TIME':5, 'LOCATION':6}

class RawSent:

	def __init__(self, senttxt):
		## tokenized sentence format
		self.tokens = senttxt.split()

	def getNumTokens(self):
		return len(self.tokens)

	def getTokens(self):
		return self.tokens

	def getStr(self):
		return " ".join(self.tokens)

	def __repr__(self):
		return self.getStr()

## round the decimal numbers to fit in classfication.

def extractPOS(sentlst):
####### Used to convert sentlst to tags.
	
	# if not os.path.exists("/Users/yangzhong/Desktop/NLPparser/mturk_specificity/input.txt"):

	with open("input.txt","w", encoding = "utf-8") as f:

		print("Reading the original sentences ....")
		for line in sentlst:
			f.write(line.getStr()+"\n")
	f.close()
	print("Done Reading sentences ...")

	print("already has the file, start tagging ...")

	subprocess.call(['./extractPostag.sh'])
	print("Successfully covert pos-tags")

	with open("sample-tagged.txt","r",encoding = "utf-8" ) as f:
		f = f.readlines()
		f = [x.strip() for x in f]
		f = [y.split() for y in f]
		all_tags = []
		tag_with_Number = {}

		for line in f:
			tag_list = []

			for word_tag in line:
				word_tag = word_tag.split("_")
				tag =  word_tag[1]
				tag_list.append(tag)
				if tag not in tag_with_Number:
					tag_with_Number[tag] = 1
				else:
					tag_with_Number[tag] += 1

			all_tags.append(tag_list)
		# Set default useful_tag.
		Useful_Tag = ['DT', 'NN', "VB", 'JJ', 'IN', '.', 'PRP', 'NNP','WP']
		big_matrix = []
		tag_2_index = {}
		for index,tag in enumerate(Useful_Tag):
			tag_2_index[tag] = index

		for line in all_tags:
			count = [0] * len(tag_2_index)
			for item in line:
				if item in Useful_Tag:
					count[tag_2_index[item]] += 1
				elif re.match("VB",item):
					count[tag_2_index["VB"]] += 1
				elif re.match("NN",item):
					count[tag_2_index["NN"]] += 1
			
			big_matrix.append(count)
		df = pd.DataFrame()
		df["Tweet"] = [sent for sent in sentlst]
	
		for fid,fname in enumerate(Useful_Tag):
			df[fname] = [big_matrix[j][fid] for j in range(len(big_matrix))]
		df.to_csv("USEFUL_TAG.csv")
		return df

# Create features on name_entities.
def NE_Concrete_Emo(sentlst):
	print("Start doing name_entities extraction and concrete extraction")
	positive = []
	negative = []
	words = {}

	# Initialize concrete dictionaries, possitive and negative words list.
	with open('./model/resources/concrete.csv', encoding='utf-8') as in_file:
	    in_file.readline()
	    for line in in_file:
	        l = line.split(',')
	        if l[1] == '0':
	            words[l[0]] = float(l[2])
	
	with open(POSITIVE, encoding = 'utf-8') as in_file:
	    for line in in_file:
	        word = line.strip()
	        if len(word) == 0:
	            continue
	        if word[0] == ';':
	            continue
	        positive.append(word)

	with open(NEGATIVE, encoding = 'gbk') as in_file:
	    for line in in_file:
	        word = line.strip()
	        if len(word) == 0:
	            continue
	        if word[0] == ';':
	            continue
	        negative.append(word)

	st = StanfordNERTagger("./model/resources/english.muc.7class.distsim.crf.ser.gz", "./model/resources/stanford-ner.jar",encoding='utf-8')

	big_matrix = []
	for index, line in enumerate(sentlst):

		tokens = word_tokenize(line.getStr())
		count = [0] * 10
		concrete = []
		tagger = st.tag(tokens)
		
		# Do the concrete count.
		for word, tag in tagger:
			if tag in NER_title:
				count[NER_title[tag]] += 1
		for token in tokens:
			if token in negative:
				count[8] += 1
			elif token in positive:
				count[9] += 1
			if token in words:
				concrete.append(words[token])
		if len(concrete) > 0:
			concrete_score = sum(concrete) / len(concrete)
		else:
			concrete_score = 0
		count = [i/len(tokens) for i in count]
		count[7] = concrete_score
		big_matrix.append(count)

	df = pd.DataFrame()
	df["Tweet"] = [sent for sent in sentlst]
	
	Useful_Tag = list(NER_title.keys())
	Useful_Tag += ["Concrete", "Negative", "Positive"]
	for fid,fname in enumerate(Useful_Tag):
		df[fname] = [big_matrix[j][fid] for j in range(len(big_matrix))]
	
	df.to_csv("NE_Concrete_Emo.csv")
	return df

def convertNum(floatNum):
	integer = floatNum // 1
	decimal = floatNum % 1
	if  decimal < 0.5:
		return integer
	elif decimal > 0.5:
		return integer + 1
	else:
		if integer == 1 or integer == 3:
			return integer + 1
		else:
			return integer

# initialize word_embedding dictionary.
def init_embeding(file = RT + "model/resources/glove.twitter.27B.100d.txt", word_2_idx=[], encoding="utf-8"):

	word_embedding_dict = {}
	with open(file,encoding = encoding) as f:
		for line in f:
			line = line.strip().split()
			word_embedding_dict[line[0].lower()] = np.asarray(line[1:])
	print("Successfully save embeddingfile")
	return word_embedding_dict

### Check the place of @user. 
def checkReply(string):
	if string.startswith("'<USER>") or string.startswith("<USER>"):
		return 0
	elif string.count("<USER>") >= 1:
		return 1
	else:
		return 2

def user_begin_or_else(sentlst):

	tweet_user_begin = []
	tweet_user_else = []

	sentlist = [r.getStr() for r in sentlst]
	for tweet in sentlist:
		
		if checkReply(tweet) == 0:  # this is a reply to former users.
			tweet_user_begin.append(1)
			tweet_user_else.append(0)
		elif checkReply(tweet) == 1:
			tweet_user_begin.append(0)
			tweet_user_else.append(1)
		else:
			tweet_user_begin.append(0)
			tweet_user_else.append(0)
	return tweet_user_begin, tweet_user_else

#############################################3
# get the embeddling list.
def word_2_weights(sentlst, embeding_dict):

	# initial word_embedding_Dict
	embeddingList = []
	word_embedding_dict = init_embeding()
	embedding_dim = len(word_embedding_dict["for"])
	for sent in sentlst:
		embedding_matrix = np.zeros((sent.getNumTokens(), embedding_dim))

		for index in range(sent.getNumTokens()):
			word = sent.getTokens()[index].lower()
			if word in word_embedding_dict.keys():
				embedding_matrix[index] = word_embedding_dict[word]
			else:
				new_vector = np.random.random(embedding_dim) * -2 + 1
				embedding_matrix[index] = new_vector
				embeding_dict[word] = new_vector

		embeddingList.append((np.mean(embedding_matrix,axis = 0)))
	return embeddingList

# count number of URLs.
def numUrl(sentlst):
	return [t.getTokens().count("<URL>") for t in sentlst]

# messure Sentence's length.
def sentLen(sentlst):
	return [t.getNumTokens() for t in sentlst]

# Count the number of Capital Letters.
def numCapLetters(sentlst, normalize=True):
	ret = []
	for t in sentlst:
		v = len([x for x in t.getStr() if x.isupper()])
		ret.append((v+0.0)/t.getNumTokens() if normalize else v)
	return ret

def numUsers(sentlst):
	return [t.getTokens().count("<USER>") for t in sentlst]

# count the number of #s.
def numNumbers(sentlst, normalize):
	ret = []
	for t in sentlst:
		v = len([x for x in t.getTokens() if _is_num(x)])
		ret.append((v+0.0)/t.getNumTokens() if normalize else v)
	return ret

def checkEmoji(string):
	emojis = [c for c in string if c in emoji.UNICODE_EMOJI]
	if len(emojis) > 0:
		return True
	else:
		return False

# Count the number of Symbols.
def numSymbols(sentlst, normalize):
	ret = []
	for t in sentlst:
		v = len([x for x in t.getStr() if not x.isalnum() and x!=" " and not checkEmoji(x)])
		ret.append((v+0.0)/ t.getNumTokens() if normalize else v)
	return ret


# Count the number of emoji in each line.
def countEmoji(sentlst, normalize=False):
	emoji_list = []
	recs = [t.getStr() for t in sentlst]
	for line in recs:
		emojis = [c for c in line if c in emoji.UNICODE_EMOJI]
		v = len(emojis)
		
		emoji_list.append((v+0.0)/len(line.split()) if normalize else v)
	return emoji_list

# Count the average word length in each sentence.
def avgWordLen(sentlst):
	ret = []
	for t in sentlst:
		v = [len(x) for x in t.getTokens()]
		ret.append(mean(v))
	return ret

# Count the number of stopwords.
def fracStopwords(sentlst):
	ret = []
	for t in sentlst:
		v = len([x for x in t.getTokens() if x.lower() in STOPWORDS])
		ret.append((v+0.0)/t.getNumTokens())
	return ret

def _is_num(s): ## s:string
	try:
		float(s)
		return True
	except ValueError:
		pass
	except TypeError:
		pass
	return False

################################################
# Brown Cluster.
def brownCluster(sentlst, brnclst, cluster_2_index, number):
	lines = []
	for instance in sentlst:
		count = [0]*number
		rs = getBrownClusNgram(instance,1,brnclst)
		rs = ["_".join(x) for x in rs]
		for item in rs:

			# If the word does not exist in the cluster, ignore it.
			if item  == "UNK":
				pass
			else:
				count[cluster_2_index[item]] += 1
		for i in range(len(count)):
			count[i] = count[i] / len(rs)
		lines.append(count)
	return lines

def getBrownClusNgram(t,n,brnclst):
	ls = []
	txts = t.getTokens()
	for nodetxt in txts:
		nodetxt = nodetxt.lower()
		if (nodetxt) in brnclst:
			ls.append(brnclst[nodetxt])

		else: ## if not in cluster file, then use OOV symbol
			ls.append("UNK")
	return _sliding_window(ls, n)

def _sliding_window(l, n):
	return [tuple(l[i:i+n]) for i in range(len(l)-n+1)]

def ParseText(string):
	string = re.sub(r"\'s", " \'s", string)
	string = re.sub(r"\'ve", " \'ve", string)
	string = re.sub(r"n\'t", " n\'t", string)
	string = re.sub(r"\'re", " \'re", string)
	string = re.sub(r"\'d", " \'d", string)
	string = re.sub(r"\'ll", " \'ll", string)
	string = re.sub(r",", " , ", string)
	string = re.sub(r"!", " ! ", string)
	string = re.sub(r"\?", " ? ", string)
	string = re.sub(r"\!"," ! ",string)
	string = re.sub("\.", " . ", string)
	string = re.sub(r"\(", " ( ", string)
	string = re.sub(r"\)", " ) ", string)
	string = re.sub(r"\?", " ? ", string)
	string = re.sub(r"\:", " : ", string)
	string = re.sub(r"\s{2,}", " ", string) 
	try:
	# Wide UCS-4 build
		oRes = re.compile(u'(['
		u'\U0001F300-\U0001F64F'
		u'\U0001F680-\U0001F6FF'
		u'\u2600-\u26FF\u2700-\u27BF]+)', 
	re.UNICODE)
	except re.error:
	# Narrow UCS-2 build
		oRes = re.compile(u'(('
	u'\ud83c[\udf00-\udfff]|'
	u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
	u'[\u2600-\u26FF\u2700-\u27BF])+)', 
	re.UNICODE)
	string = oRes.sub(r' \1 ', string)      

	return string


