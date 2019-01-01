# SpecificityTwitter

# SpecificityTwitter is a tool to predict sentence specificity of social media posts.

The dataset and models in this package are obtained using co-training as described in , AAAI 2019.

## Dependencies

Speciteller is implemented using Python 3.6+. It depends on the following packages:
- pandas
- nltk
- pickle
- sklearn
- emoji
- numpy
- Stanford CoreNLP

## Data and resources

Word lexicons for the models are available for download [here]{underConstruction}. Please note that these resources come with license(s). Decompress the tar ball under the model directory.


## Running Speciteller

Call:
```
$ python parser.py --inputfile inputfile --outputfile predfile
```

- `<inputfile>` should consists of *word-tokenized* sentences, one sentence per line;
- `<predfile>` will be the destination file which Speciteller will write the specificity scores to, one score per line in the same order as sentences in `<inputfile>`.

The scores are float numbers ranging from 1 to 5, with 1.0 being most general and 5.0 being most specific.

## Practical notes
- It is best that you word-tokenize your sentences. 

- Note that the word embedding file is a 1.2 GB file and should be downloaded from the above link. Each run of parser.py will load the file to generate features. Thus it is best to avoid loading it multiple times, or modify predict.py and tailor it for your data loading purpose.

## Citation and contact

Please cite the following paper:

TODO
