NOTE: both programs require NLTK package.


------------------------------------------------------------
program: indexing.py
------------------------------------------------------------
					DESCRIPTION
indexing.py program is responsible for the construction 
of the inverted index, based on a collection of documents
provided (documents.txt) and a stop list of words (stop_list.txt)
The program also outputs the inverted index in a text file. 


					USAGE OPTIONS
-h : print this help message
-s FILE : use stoplist file FILE
-d FILE : read input file


					EXAMPLE USAGE
In order to run the program the user has to pass 2 parameters in the command line,
which are document file and stop list:

python indexing.py -d documents.txt -s stop_list.txt

------------------------------------------------------------





------------------------------------------------------------
program: retrieval.py
------------------------------------------------------------
					DESCRIPTION
retrieval.py program is responsible for the retrieval of relevant
documents based on the queries. Both Boolean and Ranked retrival are
available. The retrieval process is performed based on the inverted index
created in indexing.py program. 


					USAGE OPTIONS
-h : print this help message
-s FILE : use stoplist file FILE
-i FILE : read inverted index text file
-d FILE : read documents.txt file
-q FILE : read queries.txt file
-A : Enter a query


					EXAMPLE USAGE:
There are 4 parameters the user has to pass in the command line, which are the
document file, the inverted index text file, the stop list text file and the 
queries text file:


python retrieval.py -d documents.txt -i inverted_index.txt -s stop_list.txt -q queries.txt


> Ranked retrieval is the default option.

> In order to use Boolean retrieval the lines 201 - 220 must be commented out.



> In order for the user to pass a new query in the program a 5th option is included, which is: -A.
 Instead of passing -q queries.txt as the last parameter, the user must type the following:

	python retrieval.py -d documents.txt -i inverted_index.txt -s stop_list.txt -A

------------------------------------------------------------





------------------------------------------------------------
eval_ir.py
------------------------------------------------------------

The text file generated from retrieval.py program that contains the results is:
similarities_results.txt


					EXAMPLE USAGE:
	python eval_ir.py cacm_gold_std.txt similarities_results.txt

	
------------------------------------------------------------







