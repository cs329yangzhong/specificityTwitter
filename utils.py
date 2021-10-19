from collections import namedtuple, Counter
from math import log
import os
import gzip
import numpy as np

RT = "./"

BROWNCLUSFILE_100 = RT + "model/resources/MetaOptimize/BrownWC/brown-rcv1.clean.tokenized-CoNLL03.txt-c100-freq1.txt"
BROWNCLUSFILE = RT + "model/resources/MetaOptimize/BrownWC/bronwn-rcv1-1000-freq1.txt"

STOPWORDFILE = RT + "model/resources/nltkstopwords.txt"

def readMetaOptimizeBrownCluster_100():
    print ("loading brown clusters...")
    word_cluster_d = {}
    cluster_2_index = {}
    with open(BROWNCLUSFILE_100, "r", encoding='utf-8') as f:
        for line in f:
            bitstr, word, numocc = line.strip().split("\t")
            word_cluster_d[word] = bitstr
            if bitstr not in cluster_2_index:
                cluster_2_index[bitstr] = len(cluster_2_index)

    print ("done; # words: ,", len(word_cluster_d))
    return word_cluster_d, cluster_2_index


def readMetaOptimizeBrownCluster():
    print ("loading brown clusters...")
    word_cluster_d = {}
    cluster_2_index = {}
    with open(BROWNCLUSFILE, "r", encoding='utf-8') as f:
        for line in f:
            bitstr, word, numocc = line.strip().split("\t")
            word_cluster_d[word] = bitstr
            if bitstr not in cluster_2_index:
                cluster_2_index[bitstr] = len(cluster_2_index)

    print ("done; # words: ,", len(word_cluster_d))
    return word_cluster_d, cluster_2_index


def readStopwords():
    ret = set()
    with open(STOPWORDFILE) as f:
        for line in f:
            l = line.strip()
            if len(l) > 0:
                ret.add(l)
        f.close()
    return ret
