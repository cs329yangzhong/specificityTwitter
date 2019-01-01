import numpy as np
from sklearn import linear_model
import pandas as pd
from collections import namedtuple
import os.path
import features
import utils


class ModelNewText(object):

    def __init__(self, brnspace=None, brnclst=None, embeddings=None):
        self.featurestest = {}  ## <name, flist>
        self.test = []
        self.brnclst = brnclst
        self.brnspace = brnspace
        self.embeddings = embeddings
        self.fileid = None
        self.testLabels = []
        self.userid = []
        self.time = []
        self.tweetid = []

    def loadFromCSV(self, filename):

        original_df = pd.read_csv(filename, encoding='utf-8')

        ### given userID. Will be deleted in the final version.
        self.userid = list(original_df.loc[:, 'USERID'])
        try:
            self.time = list(original_df.loc[:, 'TweetTime'])
            self.tweetid = list(original_df.loc[:, 'TweetID'])
            self.testLabels = list(original_df.loc[:, 'Score'])
        except KeyError:
            pass

        self.test = [features.ParseText(y) for y in
                     list(original_df.loc[:, 'Tweet'])]
        print(len(self.test))

    def loadFromTSV(self, filename):

        original_df = pd.read_csv(filename, encoding='utf-8', sep="\t")
        print(original_df.shape)

        ### given userID. Will be deleted in the final version.
        self.userid = list(original_df.loc[:, 'user_id'])

        try:
            self.time = [int(y.split()[-1]) for y in
                         list(original_df.loc[:, 'time'])]
            self.tweetid = list(original_df.loc[:, 'tweet_id'])
            self.testLabels = list(original_df.loc[:, 'Score'])
        except KeyError:
            pass

        self.test = [features.ParseText(y) for y in
                     list(original_df.loc[:, 'text'])]

    def loadFromFile(self, filename):
        self.test = []
        self.fileid = os.path.basename(filename)
        i = 0
        with open(filename) as f:
            for line in f:
                if len(line.strip()) == 0: continue
                self.test.append(features.ParseText(line))
                i += 1
        print(len(self.test))
        f.close()

    def loadSentences(self, identifier, sentlist):
        ## sentlist should be a list of sentence strings, tokenized;
        ## identifier is a string serving as the header of this sentlst
        self.test = []
        self.fileid = identifier
        for i, sent in enumerate(sentlist):
            self.test.append(
                Instance(identifier + "." + str(i), 0, features.RawSent(sent)))

    def _add_feature(self, key, values):
        if key in self.featurestest: return
        self.featurestest[key] = values

    def numEmoji(self):
        df = pd.DataFrame()

        recs = [features.RawSent(r) for r in self.test]
        df["numsymbols"] = features.numSymbols(recs, normalize=True)
        df["numemoji"] = features.countEmoji(recs, normalize=True)
        df.to_csv("symbol&emoji.csv", encoding="utf-8")

    # Genereate word embeddings.
    def fNeuralVec(self):

        sentlst = [features.RawSent(r) for r in self.test]
        keys = ["word_embed-" + str(i) for i in range(100)]

        if keys[0] not in self.featurestest:
            embeddingList = features.word_2_weights(sentlst, self.embeddings)
            for fid, fname in enumerate(keys):
                self.featurestest[fname] = [embeddingList[j][fid] for j in
                                            range(len(embeddingList))]

            print("Successfully generate word_embdding features")

    # POS_Tags.
    def fPostag(self):
        sentlst = [features.RawSent(r) for r in self.test]
        pos_tag = features.extractPOS(sentlst)
        Useful_Tag = ['DT', 'NN', "VB", 'JJ', 'IN', '.', 'PRP', 'NNP', 'WP']
        for i in Useful_Tag:
            self._add_feature(i, pos_tag.loc[:, i])

    # Brown CLuster, short 100 vectors.

    def fBrownCluster_100(self):
        sentlst = [features.RawSent(r) for r in self.test]
        keys = ["brnclst_100-" + str(i) for i in range(100)]

        if keys[0] not in self.featurestest:
            print("Start initialize Browncluster ....")

            brownClus, cluster_2_index = utils.readMetaOptimizeBrownCluster_100()
            print("finished generating brownClusterlist !")

            self.brnclst = brownClus

            brownClusterList = features.brownCluster(sentlst, brownClus,
                                                     cluster_2_index, 100)
            for fid, fname in enumerate(keys):
                self.featurestest[fname] = [brownClusterList[j][fid] for j in
                                            range(len(brownClusterList))]

    # NE and Concrete words.
    def NE_Concrete(self):
        sentlst = [features.RawSent(r) for r in self.test]
        pos_tag = features.NE_Concrete_Emo(sentlst)
        Useful_Tag = ['ORGANIZATION', "PERCENT", 'PERSON', 'DATE', 'MONEY',
                      'TIME', 'LOCATION', 'Concrete']
        for i in Useful_Tag:
            self._add_feature(i, pos_tag.loc[:, i])

    def transformEmoji(self):
        recs = [features.RawSent(r) for r in self.test]
        self._add_feature("numemoji", features.countEmoji(recs, normalize=True))

    def fShallow(self):
        normalize = True
        recs = [features.RawSent(r) for r in self.test]
        self._add_feature("avgwordlen", features.avgWordLen(recs))
        self._add_feature("sentlen", features.sentLen(recs))
        self._add_feature("numsymbols", features.numSymbols(recs, normalize))
        self._add_feature("numcapltrs", features.numCapLetters(recs, normalize))
        self._add_feature("numnumbers", features.numNumbers(recs, normalize))

    ################## 4 main feature groups. #########################
    ### Notice, in our best model, we did not use the transormTweet feature.

    # Surface and Lexical features,
    def transLexical(self):
        self.fShallow()
        self.fPostag()
        self.NE_Concrete()

    # Distributional word representations
    def transEmbedding(self):
        self.fNeuralVec()
        self.fBrownCluster_100()

    # Emotion features
    def transEmotionFeature(self):
        self.transformEmoji()
        try:
            f = pd.read_csv("NE_Concrete_Emo.csv")
            self._add_feature("Negative", f.loc[:, 'Negative'])
            self._add_feature("Positive", f.loc[:, 'Positive'])
        except IOError:
            sentlst = [features.RawSent(r) for r in self.test]
            file = features.NE_Concrete_Emo(sentlst)
            self._add_feature("Negative", file.loc[:, 'Negative'])
            self._add_feature("Positive", file.loc[:, 'Positive'])

    # def transformTweet(self):
    # 	recs = [features.RawSent(r) for r in self.test]
    # 	self._add_feature("numurl",features.numUrl(recs))
    # 	tweet_begin, tweet_else = features.user_begin_or_else(recs)

    # 	self._add_feature("user_beginning",tweet_begin)
    # 	self._add_feature("user_else",tweet_else)

    def transform_features(self):
        df = pd.DataFrame()
        df["userID"] = self.userid
        df["Tweet"] = self.test

        for feature in self.featurestest.keys():
            df[feature] = self.featurestest[feature]
        # print(len(self.feature))
        df.to_csv("./output/test.csv", sep='\t')
        print("DOne")
