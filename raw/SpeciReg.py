import argparse
import pandas as pd
import logging
from regression import testRBFSVR


parser = argparse.ArgumentParser(description='Specificity Reg')

parser.add_argument('-training', type=str, default='testForAllFeatures_Check_label.csv', help='Name of training file')
parser.add_argument('-validation', type=str, default='testForAllFeatures_testSet.csv', help='Name of validation file')
parser.add_argument('-output', type=str, default='', help='Name of output file')
parser.add_argument('-model', type=str, default='RBFSVR', help='Regression model [LinearSVR, RBFSVR]')
parser.add_argument('-features', type=str, default='', help='Group of features to be used [All, Lexical, tweet, emotion,'
                                                            'demographics]')
parser.add_argument('-exclude', type=str, default='', help='Features to be excluded')

args = parser.parse_args()
logging.basicConfig(filename='.\\logs\\%s %s logger.log' % (args.model), level=logging.INFO)


