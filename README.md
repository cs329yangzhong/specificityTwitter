# SpecificityTwitter is a tool to predict sentence specificity of social media posts.

The dataset and models in this package are obtained using co-training as described in , AAAI 2019.

## Citation and contact

Please cite the following paper:

TODO

## Dependencies

SpecificityTwitter is implemented using Python 3.6+. It depends on the following packages:
- numpy
- pandas
- pickle
- scikit-learn
- [emoji](https://gate.ac.uk/wiki/twitter-postagger.html)
- [GATE Twitter part-of-speech tagger](https://gate.ac.uk/wiki/twitter-postagger.html), please download the twitie-tagger and unzip it in current directory.

Our model was trained on a support vector regression model intergraded with scikit-learn. The last three packages together with the StanfordCoreNLP toolkit are required to generate features to be used in prediction. 

## Data and resources

Word lexicons for the models are available for download [here](https://utexas.box.com/shared/static/9smjk9q5kxrci1whdehk5zpdgjx7gisq.zip). Please note that these resources come with license(s). Decompress the tar ball under the model directory.

### Resources
There are several files in the resource folder.
- **browncluster.txt**    (Browncluster)
- **concrete.csv** (Concrete level)
 
- **Word Embedding from [GloVe](https://nlp.stanford.edu/projects/glove/)**
-- glove.twitter.27B.100d.txt

- **Sentiment words from (Hu and Liu, 2004)**
-- negatie-words.txt
-- positive-words.txt

- **Stanford NER tagger (Finkel et al., 2005)**
-- stanford-ner.jar
-- english.muc.7class.distsim.crf.ser.gz



## Running SpecificityTwitter

Call:
```
$ python specificity.py --inputfile inputfile --outputfile predfile
```

- `<inputfile>` should consists of *word-tokenized* sentences, one sentence per line;
- `<predfile>` will be the destination file which SpecicifityTwitter will write the specificity scores to, one score per line in the same order as sentences in `<inputfile>`.

The scores are decimal numbers ranging from 1 to 5, with 1.0 being most general and 5.0 being most specific.

## Practical notes
- It is best that you word-tokenize your sentences. 

- Note that the word embedding file is a 1.2 GB file and should be downloaded from the above link. Each run of specificity.py will load the file to generate features. Thus it is best to avoid loading it multiple times, or modify feature.py and tailor it for your data loading purpose.

