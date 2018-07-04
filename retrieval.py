"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
OPTIONS:
    -h : print this help message
    -s FILE : use stoplist file FILE
    -i FILE : read inverted index text file
    -d FILE : read documents.txt file
    -q FILE : read queries.txt file
    -A : Enter a query
------------------------------------------------------------
"""
import sys, re, getopt, glob, nltk, operator, math, os, time
from read_documents import ReadDocuments
from nltk.stem import PorterStemmer



class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:],'hs:i:d:q:A')
        opts = dict(opts)
        self.opts2 = opts
        self.argfiles = args
        self.stops = set()
        self.binary_weights = False
        self.index_file = None
        self.queries_file = None
        self.docs_file = None
        self.custom_query = None

        if '-h' in opts:
            self.printHelp()
        
        if '-s' in opts:
            self.readStopList(opts['-s'])

        if '-i' in opts:
            self.index_file = (opts['-i'])

        if '-d' in opts:
            self.docs_file = (opts['-d'])

        if '-q' in opts:
            self.queries_file = (opts['-q'])

        if '-A' in opts:
            self.custom_query = input('Enter a query: ')
            

    def printHelp(self):
        help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
        print(help, file=sys.stderr)
        sys.exit()

    def readStopList(self,file):
        f = open(file,'r')
        for line in f:
            self.stops.add(line.strip())




#fucntion to print inverted index if needed:
def print_inverted(index):
    for token in index.keys():
        print(token)
        for doc in index[token].keys():
            print("\t{} : {}".format(doc, index[token][doc]))



#function to read inverted index text file that was created in indexing.py script:
def read_inverted (file):
    index = dict()# 2 -  level dictionary to store the inverted index
    f = open(file, 'r')
    token = ""
    for line in f:
        splitted_line = line.split() #use splitted line (empty space) to extract the required information from each line.

        if len(splitted_line) == 1:
            index[splitted_line[0]] = dict()
            token = splitted_line[0]
        
        else:
            docid = splitted_line[0]
            counter = splitted_line[2]
            index[token][docid] = counter
    return index


#calculate the total number of documents in the collection:
def total_docs (document_collection):
    all_docs = 0
    for document_collection.docid in document_collection:
            all_docs += 1

    return all_docs



#calculate the document frequency of each term w (number of documents containing w):
def document_frequency (inverted, token):
    if token in inverted.keys():
        freq = len(inverted[token].keys())
        return freq
    else:
        return 0


#calculate the term frequency of each term w (number of times w appears in a document d):
def term_frequency(inverted, token, document):
    if (token in inverted.keys()):
        if document in inverted[token].keys():
            tf = int(inverted[token][document])
            return tf
        else:
            return 0
    else:
        return 0



#calculate the inverse doc frequency for each term w:
def inverse_doc_frequency(document_collection, inverted, token, collection_length):
    dfw = document_frequency(inverted, token)
    if dfw > 0:
        return math.log10(collection_length / dfw)
    else:
        return 0



#calculate size of each document vecotr:
#first calculate IDF, then TF.IDF and finally size of each document vector:
def size (document_collection, inverted):
    collection_length = total_docs(document_collection)
    size_dictionary = dict ()#dictionary to store documents and the relevant size similarity.

    for term in inverted.keys():
        idf = inverse_doc_frequency(document_collection, inverted, term, collection_length)
    
        for doc in inverted[term].keys():
            tf = inverted[term][doc]
            tf_idf = float(tf)*idf

            tf_idf_squared = tf_idf**2

            if doc in size_dictionary.keys():
                size_dictionary[doc] += tf_idf_squared
            else:
                size_dictionary[doc] = tf_idf_squared

    for doc in size_dictionary.keys():
        size_dictionary[doc] = math.sqrt(size_dictionary[doc])
    return size_dictionary


#function to create a text file with the similarities calculated:
def create_similarities_textfile(sorted_similarities, q_id):
    f = open("similarities_results.txt", "a")
    for i in range(10):
        f.write("{} {}\n".format(q_id, sorted_similarities[i][0]))





#MAIN:
if __name__ == '__main__':
    config = CommandLine() 

    #Variables: 
    queries = ReadDocuments(config.queries_file)
    documents = ReadDocuments(config.docs_file)
    inverted = read_inverted(config.index_file)

    collection_length = total_docs(documents) #find total number of documents using the total_docs function created above
    size_doc_vector = size(documents, inverted) #find the size of each document vector using the size function created above
    
    stemmer = PorterStemmer()



    #Measure execution time:   
    start = time.time()




    #Checks if the user has passed a new query.
    if ('-A' not in config.opts2):




        #BOOLEAN RETRIEVAL:

        # #PREPROCESSING: tokenise, stemming queries.txt:
        #Uncomment lines 201 to 220 for Boolean retrieval.
        # for query in queries:
        #     query_tokens = []
        #     for line in query.lines:
        #         tokens = nltk.word_tokenize(line)
        #         for token in tokens:
        #             token = token.lower()
        #             if not (token.lower in config.stops) and token.isalpha():                    
        #                 token = stemmer.stem(token)
        #                 query_tokens.append(token)
                    
        
        #     docs = [] # list of lists
        #     for token in query_tokens:
        #         if token in inverted.keys():
        #             docs.append(inverted[token].keys())
        #     #Boolean:
        #     intersec = docs[0]
        #     for doc in range(1, len(docs)):
        #        intersec = set(intersec).intersection(docs[doc])
        #     print ("Query ID {}: {}".format(query.docid, intersec))     





        #RANKED RETRIEVAL:

        os.remove("similarities_results.txt") #delete similarity results text file before creating the new file, so that only new results are present in the file.

        #Preprocess queries:
        #For each query in queries text file:
        for query in queries:

            #Variables
            q = dict() #QUERY DICTIONARY: store tokens as KEY, token frequency as VALUE
            tokens = list() #store all the tokens in the query
            similarities = dict() #dictionary to store cosine angle that will be calculated
            initial_documents = []#store all the documents that contain each token of the query

            for line in query.lines:
                tokens = nltk.word_tokenize(line)
                for token in tokens:
                    token = token.lower()
                    if not (token in config.stops) and token.isalpha():                    
                        token = stemmer.stem(token)

                        if token in q.keys():
                            q[token] += 1
                        else:
                            q[token] = 1

            for term in q.keys():
                if term in inverted.keys():
                    for docid in inverted[term].keys():
                        initial_documents.append(docid)
            initial_documents = list(set(initial_documents))

            for doc in initial_documents:
                total = 0
                for term in q.keys():

                    query_tf = float(q[term])
                    query_idf = inverse_doc_frequency(documents, inverted, term, collection_length)
                    query_tfidf = query_tf * query_idf

                    document_tf = term_frequency(inverted, term, doc)
                    document_idf = inverse_doc_frequency(documents, inverted, term, collection_length)
                    document_tfidf = document_tf * document_idf

                    total += document_tfidf * query_tfidf

                if size_doc_vector[doc] > 0: #only consider the sizes of non-zero document vectors
                    similarities[doc] = total / size_doc_vector[doc]

            similarities = sorted(similarities.items(), key = operator.itemgetter(1), reverse = True)

            #create text file containing the 10 highest ranked documents:
            create_similarities_textfile(similarities, query.docid)




    #Enter this loop when the user has passed a NEW QUERY:
    else:


        #Preprocess query:

        
        #Variables
        query = config.custom_query

        q = dict() #QUERY DICTIONARY: store tokens as KEY, token frequency as VALUE
        tokens = list() #store all the tokens in the query
        similarities = dict() #dictionary to store cosine angle that will be calculated
        initial_documents = []#store all the documents that contain each token of the query

        tokens = nltk.word_tokenize(query)
        for token in tokens:
            token = token.lower()
            if not (token in config.stops) and token.isalpha():                    
                token = stemmer.stem(token)

                if token in q.keys():
                    q[token] += 1
                else:
                    q[token] = 1

        for term in q.keys():
            if term in inverted.keys():
                for docid in inverted[term].keys():
                    initial_documents.append(docid)
        initial_documents = list(set(initial_documents))

        for doc in initial_documents:
            total = 0
            for term in q.keys():

                query_tf = float(q[term])
                query_idf = inverse_doc_frequency(documents, inverted, term, collection_length)
                query_tfidf = query_tf * query_idf

                document_tf = term_frequency(inverted, term, doc)
                document_idf = inverse_doc_frequency(documents, inverted, term, collection_length)
                document_tfidf = document_tf * document_idf

                total += document_tfidf * query_tfidf

            if size_doc_vector[doc] > 0: #only consider the sizes of non-zero document vectors
                similarities[doc] = total / size_doc_vector[doc]

        similarities = sorted(similarities.items(), key = operator.itemgetter(1), reverse = True)

        print("Matched documents for query: ", query)
        for i in range (1, 10):
            print("{}.: doc ID = {}".format(i, similarities[i][0]))

    
    #Print execution time:              
    end = time.time()
    print("\nExecution time is: ", end - start)

    



