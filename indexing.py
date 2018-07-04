"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
OPTIONS:
    -h : print this help message
    -s FILE : use stoplist file FILE
    -d FILE : read input file
------------------------------------------------------------
"""

import sys, re, getopt, glob
from read_documents import ReadDocuments
from nltk.stem import PorterStemmer
import nltk

class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:],'hs:d:')
        opts = dict(opts)
        self.argfiles = args
        self.stops = set()
        self.binary_weights = False
        self.docs_file = None

        if '-h' in opts:
            self.printHelp()
        
        if '-s' in opts:
            self.readStopList(opts['-s'])

        if '-d' in opts:
            self.docs_file = (opts['-d'])



    def printHelp(self):
        help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
        print(help, file=sys.stderr)
        sys.exit()

    def readStopList(self,file):
        f = open(file,'r')
        for line in f:
            self.stops.add(line.strip())




# function to print inverted index if needed:    
def print_inverted(index):
    for token in index.keys():
        print(token)
        for doc in index[token].keys():
            print("\t{} : {}".format(doc, index[token][doc]))



#function to create the inverted index text file, using the dictionary (d) created in main
def create_inverted_textfile(index):
    f = open("inverted_index.txt", "w")#name the text file as: "inverted_index.txt"
    for token in index.keys():
        f.write(token + "\n")
        for doc in index[token].keys():
            f.write("\t{} : {}\n".format(doc, index[token][doc]))



#MAIN:
if __name__ == '__main__':
    config = CommandLine()

    #VARIABLES:
    documents = ReadDocuments(config.docs_file)

    stemmer = PorterStemmer() #stemming function imported from ntlk





    #PREPROCESSING:

    #variables:
    d = dict()# 2 level dictionary to store terms (tokens) as KEYS in the 1st level; documents as KEYS & number of occurances of terms as VALUES in 2nd level.
    tokens = list() #list to store tokenise terms for each document line (before they are passed in dictionary)

    #tokenisation & stemming:
    for doc in documents:
        for line in doc.lines:
            tokens = nltk.word_tokenize(line) #tokenise each line
            for token in tokens:
                token = token.lower() #remove capitalisation
                if not (token.lower in config.stops) and token.isalpha():                    
                    token = stemmer.stem(token) #stemming 
                    if token in d.keys(): #store in dictionary - d
                        if doc.docid in d[token].keys():
                            d[token][doc.docid] += 1
                        else: 
                            d[token][doc.docid] = 1
                    else: 
                        d[token] = dict()
                        d[token][doc.docid] = 1

    #create inverted index text file by calling the function 'create_inverted_textfile':
    create_inverted_textfile(d)


