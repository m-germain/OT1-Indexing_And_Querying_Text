import re
import ast
import mmap
import vbcode
import statistics
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

            for element in posting_list:
                current = element.getDocId()

                if(i > 0): 
                    diff = int(current)-int(previous)
                    element.updateDocID( vbcode.encode_number(diff) )
                    
                previous = current
                i = i+1               
                
            self.index.update({ term[0]: posting_list })

        ## print and build hmap
        s = ""
        startpos = 0

        for term in self.index.items():
            posting_list = term[1]
            q = "["

            for element in posting_list:
                q += str(element)+", "

            q = q[:-2] + "]\n"
            self.mmap.update({ term[0]: (vbcode.encode_number(startpos), vbcode.encode_number( len(q) )) })

            startpos = startpos + len(q) + 1
            s += q
    
        return s

    def index_document(self, document):
        """
        Process a given document, save it to the Store and update the index.
        """

        # Remove punctuation from the text.
        clean_text = re.sub(r"[^\w\s]", "", document["text"])
        # We remove the Stop Words.

        # We split each terms.
        terms = clean_text.split(" ")

        appearances_dict = dict()

        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            if term.lower() not in self.stop_words:
                stemmed_term = self.stemmer().stem(term)

                term_frequency = (
                    appearances_dict[stemmed_term].frequency
                    if stemmed_term in appearances_dict
                    else 0
                )
                appearances_dict[stemmed_term] = Appearance(
                    document["id"], term_frequency + 1
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

        query = re.sub(r"[^\w\s]", "", query)

        query = query.split(" ")
        query = map(lambda x: self.stemmer().stem(x), query)

        # open posting list
        with open(self.posting_lists_file, "r+b") as f:
            # memory-map the file, size 0 means whole file
            mm = mmap.mmap(f.fileno(), 0)
            dd = defaultdict(list)

            # find relevant documents
            for q in query:
                val = self.mmap.get(q, "")

                if( val != "" ): # key exists
                    startpos = vbcode.decode(val[0])[0]
                    endpos = startpos + vbcode.decode(val[1])[0]

                    posting_list = mm[startpos:(endpos-1)]
                    posting_list = ast.literal_eval(posting_list.decode("utf-8") )

                    i = 0
                    for element in posting_list:
                        if( i == 0 ): 
                            dd[ element[0] ].append( element[1] )
                            previousDocId = element[0]
                        else: 
                            docId = vbcode.decode(element[0])[0] +  previousDocId
                            dd[ docId ].append( element[1] )
                            previousDocId = docId

                        i = i+1
            
            # find the 3 top elements
            arr = []

            for key,value in dd.items(): 
                arr.append([key, statistics.mean(value)])
            
            arr = sorted(arr, key=lambda w: w[1])

            print(arr)
            mm.close()
