from nltk.tag import StanfordNERTagger
import pandas as pd

NER_title = {'ORGANIZATION':0, "PERCENT":1, 'PERSON':2, 'DATE':3, 'MONEY':4, 'TIME':5, 'LOCATION':6}
negative = []
positive = []
words = {}

with open('13428_2013_403_MOESM1_ESM.csv', encoding='utf-8') as in_file:
    in_file.readline()
    for line in in_file:
        l = line.split(',')
        if l[1] == '0':
            words[l[0]] = float(l[2])

with open('positive-words.txt', encoding='utf-8') as in_file:
    for line in in_file:
        word = line.strip()
        if len(word) == 0:
            continue
        if word[0] == ';':
            continue
        positive.append(word)

with open('negative-words.txt', encoding='gbk') as in_file:
    for line in in_file:
        word = line.strip()
        if len(word) == 0:
            continue
        if word[0] == ';':
            continue
        negative.append(word)

in_f = pd.read_csv('8_15_Depression', sep='\t')
tweets = list(in_f['Tweet'])



st = StanfordNERTagger('C:\\Users\\Yuan\\Desktop\\stanford-ner-2018-02-27\\classifiers\\english.muc.7class.distsim.crf.ser.gz',
                       'C:\\Users\\Yuan\\Desktop\\stanford-ner-2018-02-27\\stanford-ner.jar')

add_on = []
leng = len(tweets)
for ind, tweet in enumerate(tweets):
    count = [0] * 10
    tokens = tweet.split()

    concrete = []

    tagger = st.tag(tokens)
    for word, tag in tagger:
        if tag in NER_title:
            count[NER_title[tag]] += 1
    for token in tokens:
        if token in negative:
            count[7] += 1
        elif token in positive:
            count[8] += 1
        if token in words:
            concrete.append(words[token])
    if len(concrete) > 0:
        concrete_score = sum(concrete) / len(concrete)
    else:
        concrete_score = 0
    count = [i/len(tokens) for i in count]
    count[9] = concrete_score
    add_on.append(count)
    print('%d / %d' % (ind, leng))
    print(tweet)
    print(tagger)
    print(count)


with open('depression_f_add_on', 'w') as out_file:
    for title in NER_title:
        out_file.write(title)
        out_file.write('\t')
    for title in ['Negative', 'Positive', 'Concrete']:
        out_file.write(title)
        out_file.write('\t')
    out_file.write('\n')
    for tweet in add_on:
        for feature in tweet:
            out_file.write(str(feature))
            out_file.write('\t')
        out_file.write('\n')