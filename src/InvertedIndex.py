import re
import ast
import mmap
import vbcode
import statistics
from datetime import datetime

from collections import defaultdict
from math import log10
from Appearance import Appearance
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer


class InvertedIndex:
    """
    Inverted Index class.
    """

    def __init__(self, store):
        self.index = dict()
        self.mmap = dict()
        self.store = store
        self.stop_words = set(stopwords.words("english"))
        self.stemmer = EnglishStemmer

    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.index)

    def getMMAP(self):
        return self.mmap

    def loadInvertedIndex(self, mmap, posting_lists):
        file = open(mmap, "r")

        contents = file.read()
        self.mmap = ast.literal_eval(contents)

        file.close()

        self.posting_lists_file = posting_lists

    def prepareForPrint(self):
        """
        Prepare the PL to be printed in a file
        """
        n_doc = self.store.count()

        # foreach term
        for term in self.index.items():
            posting_list = term[1]
            n_doc_found = len(posting_list) # number of documents where the term has been found

            idf = log10(n_doc/(1.0+n_doc_found))

            # compute TF-IDF
            for element in posting_list:
                f = element.getFrequency()
                element.updateFrequency( max(0,(1.0+log10(f)) * idf) )

            # sort by docID
            i=0
            posting_list = sorted(posting_list, key=lambda w: w.getDocId())
                
            self.index.update({ term[0]: posting_list })

        ## print and build hmap
        s = bytearray()
        startpos = 0

        for term in self.index.items():

            my_posting_list = bytearray()

            for element in term[1]:
                doc = vbcode.encode_number(element.getDocFreq()[0])
                frequency = element.getDocFreq()[1].to_bytes(2, byteorder='big')

                my_posting_list  += frequency + len(doc).to_bytes(1, byteorder='big') + doc
           
            self.mmap.update({ term[0]: (startpos, len(my_posting_list)) })
            startpos = startpos + len(my_posting_list) 

            s += my_posting_list
            
        return s

    def index_document(self, document):
        """
        Process a given document, save it to the Store and update the index.
        """

        # Remove punctuation from the text.
        clean_text = re.sub(r"[^\w\s]", "", document.text)
        # We remove the Stop Words.

        # We split each terms.
        terms = clean_text.split(" ")

        appearances_dict = dict()

        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            if term.lower() not in self.stop_words:

                # Here you can activate the stemming.
                # stemmed_term = self.stemmer().stem(term).lower()
                stemmed_term = term.strip().lower()

                term_frequency = (
                    appearances_dict[stemmed_term].frequency
                    if stemmed_term in appearances_dict
                    else 0
                )
                appearances_dict[stemmed_term] = Appearance(
                    document.doc_id, term_frequency + 1
                )

        # Update the inverted index
        update_dict = {
            key: [appearance]
            if key not in self.index
            else self.index[key] + [appearance]
            for (key, appearance) in appearances_dict.items()
        }

        self.index.update(update_dict)
        
        # Add the document into the database
        self.store.add(document)
        return document

    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances.
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        # TODO More advanced search engine W/ word 2 vect, similarity and better treatment of more then 1 word in query.
        # we could use some steming when reading the query

        begin = datetime.now()
        
        query = re.sub(r"[^\w\s]", "", query)

        query = query.split(" ")
        # query = map(lambda x: self.stemmer().stem(x), query)

        # open posting list
        with open(self.posting_lists_file, "r+b") as f:
            # memory-map the file, size 0 means whole file
            mm = mmap.mmap(f.fileno(), 0)
            dd = defaultdict(list)

            # find relevant documents
            for q in query:
                val = self.mmap.get(q, "")

                if( val != "" ): # key exists
                    startpos = val[0]
                    endpos = startpos + val[1]

                    posting_list = mm[startpos:endpos+1]

                    a = bytearray(posting_list)

                    start = 0                    
                   # previousDocId = 0
                                        
                    while start < len(a) :

                        if(len(a[start:start+2]) < 2):
                            break

                        frequency = int.from_bytes(a[start:start+2], byteorder='big')/100
                        docId_length = int.from_bytes(a[start+2:start+3], byteorder='big')
                        

                        docId = int(vbcode.decode(a[start+3:start+3+docId_length])[0]) #+  previousDocId

                        dd[ docId ].append( frequency )

                        start = start + 3 + docId_length

                
            # find the 3 top elements
            arr = []

            for key,value in dd.items(): 
                arr.append([key, sum(value)])
            
            arr = sorted(arr, key=lambda w: -w[1]) # sort desc
            mm.close()

            finish = datetime.now()

            return arr, (finish - begin)
