import re
from Appearance import Appearance
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer


class InvertedIndex:
    """
    Inverted Index class.
    """

    def __init__(self, store):
        self.index = dict()
        self.store = store
        self.stop_words = set(stopwords.words("english"))
        self.stemmer = EnglishStemmer

    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.index)

    def index_document(self, document):
        """
        Process a given document, save it to the Store and update the index.
        """

        # Remove punctuation from the text.
        clean_text = re.sub(r"[^\w\s]", "", document["text"])
        # TODO We remove the Stop Words.
        # We split each terms.
        terms = clean_text.split(" ")

        appearances_dict = dict()

        # Dictionary with each term and the frequency it appears in the text.
        # TODO Update the Terme calculation for optimization. See PEP Diapo.

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

        query = query.split(" ")
        query = map(lambda x: self.stemmer().stem(x), query)

        return {
            term: self.index[term] for term in query if term in self.index
        }