import argparse
import pickle
import sys
import os
from createFeatures import *


MODELFILE = "./model/best_model.pkl"
# Load the model with best performance.

def getFeatures(fin):
	## main function to run specifictTwitter parser and return predictions
    ## sentlist should be a list of sentence strings, tokenized;
	print("Start initialize word_embedding ...")
	embeddings = features.init_embeding()
	print("finished word_embedding ...")
	a = ModelNewText(embeddings = embeddings)

	## When use our data.
	# a.loadFromCSV(fin)

	a.loadFromFile(fin)
	a.transLexical()
	a.transEmbedding()
	a.transEmotionFeature()
	a.transform_features()

def predict(model = MODELFILE):
	with open(model, 'rb') as file:  
		pickle_model = pickle.load(file)
		print("successfully laod")
	f = pd.read_csv("./output/test.csv", sep = "\t")
	feature = f.iloc[:, 3:]
	output = pickle_model.predict(feature)
	return output

def writeSpecificity(preds, outf):
	with open(outf,"w") as f:
		for x in preds:
			f.write("%f\n"%x)
		f.close()
	print("output to " + outf+" done")
	clean()

def run(identifier, sentlist):
    ## main function to run the parser and return predictions
    ## sentlist should be a list of sentence strings, tokenized;
    ## identifier is a string serving as the header of this sentlst
	print("Start initialize word_embedding ...")
	embeddings = features.init_embeding()
	print("finished word_embedding ...")
	a = ModelNewText(embeddings = embeddings)
	a.loadFromFile(fin)
	a.transLexical()
	a.transEmbedding()
	a.transEmotionFeature()
	a.transform_features()
	return predict(model = MODELFILE)

def clean():
	# clean the intermediate files.
	os.remove("NE_Concrete_Emo.csv")
	os.remove("sample-tagged.txt")
	os.remove("USEFUL_TAG.csv")

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--inputfile", help="input raw text file, one sentence per line, tokenized", required=True)
	argparser.add_argument("--outputfile", help="output file to save the specificity scores", required=True)
	sys.stderr.write("Predictor: please make sure that your input sentences are WORD-TOKENIZED for better prediction.\n")
	args = argparser.parse_args()
	getFeatures(args.inputfile)
	preds = predict(model = MODELFILE)
	writeSpecificity(preds,args.outputfile)


