from nltk.tag import StanfordNERTagger
import pandas as pd

PRESENT = {}
FUTURE = {}
PAST = {}

temp_lexicon = pd.read_csv('temporalOrientationLexicon.csv')
print(temp_lexicon[temp_lexicon['category'] == 'PRESENT_OR_NOT'])
print(list(temp_lexicon[temp_lexicon['category'] == 'PRESENT_OR_NOT']['term']))
print(list(temp_lexicon[temp_lexicon['category'] == 'PRESENT_OR_NOT']['Norm_Weight']))

for ind, word in enumerate(list(temp_lexicon[temp_lexicon['category'] == 'PRESENT_OR_NOT']['term'])):
    PRESENT[word] = float(list(temp_lexicon[temp_lexicon['category'] == 'PRESENT_OR_NOT']['Norm_Weight'])[ind])
for ind, word in enumerate(list(temp_lexicon[temp_lexicon['category'] == 'FUTURE_OR_NOT']['term'])):
    FUTURE[word] = float(list(temp_lexicon[temp_lexicon['category'] == 'FUTURE_OR_NOT']['Norm_Weight'])[ind])
for ind, word in enumerate(list(temp_lexicon[temp_lexicon['category'] == 'PAST_OR_NOT']['term'])):
    PAST[word] = float(list(temp_lexicon[temp_lexicon['category'] == 'PAST_OR_NOT']['Norm_Weight'])[ind])

in_f = pd.read_csv('validation.tsv', sep='\t')
tweets = list(in_f['Tweet'])

tweet_temp = []
for tweet in tweets:
    count = [0] * 3
    for word in tweet:
        if word in PRESENT:
            count[0] += PRESENT[word]
        if word in FUTURE:
            count[1] += FUTURE[word]
        if word in PAST:
            count[2] += PAST[word]
    count = [i / len(tweet) for i in count]
    tweet_temp.append(count)
    print(count)


with open('validation_temp', 'w', encoding='utf-8') as out_put:
    out_put.write('PRESENT')
    out_put.write('\t')
    out_put.write('FUTURE')
    out_put.write('\t')
    out_put.write('PAST')
    out_put.write('\t')
    out_put.write('\n')
    for line in tweet_temp:
        for cat in line:
            out_put.write(str(cat))
            out_put.write('\t')
        out_put.write('\n')
'''
add_on = []
leng = len(tweets)
for ind, tweet in enumerate(tweets):
    count = [0] * 10
    tokens = tweet.split()
    tagger = st.tag(tokens)
    concrete = []
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


with open('testSet_f_add_on', 'w') as out_file:
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
        out_file.write('\n')'''