import re
from Appearance import Appearance


class InvertedIndex:
    """
    Inverted Index class.
    """

    def __init__(self, store):
        self.index = dict()
        self.store = store

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

        # TODO We use stemming before storing.
        # Dictionary with each term and the frequency it appears in the text.
        # TODO Update the Terme calculation for optimization. See PEP Diapo.
        for term in terms:
            term_frequency = (
                appearances_dict[term].frequency if term in appearances_dict else 0
            )
            appearances_dict[term] = Appearance(document["id"], term_frequency + 1)

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
        return {
            term: self.index[term] for term in query.split(" ") if term in self.index
        }
