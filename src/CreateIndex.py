import nltk
import mmap
import json

#nltk.download('stopwords')

from Storage import Storage
from InvertedIndex import InvertedIndex

def main():
    store = Storage()
    index = InvertedIndex(store)

    document1 = {
        "id": "1",
        "text": "In information retrieval, tf–idf or TFIDF, short for term frequency–inverse document frequency, is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus."
    }
    document2 = {
        "id": "20",
        "text": "China is a country located in East Asia bordering fourteen other countries, including Mongolia to the north; Kazakhstan, Kyrgyzstan, Tajikistan, Afghanistan, and Pakistan to the west; India, Nepal, and Bhutan to the southwest; Myanmar, Laos, and Vietnam to the south; "
    }
    document3 = {
        "id": "21",
        "text": "Water is an inorganic, transparent, tasteless, odorless, and nearly colorless chemical substance, which is the main constituent of Earth's hydrosphere and the fluids of all known living organisms. "
   }
   
    index.index_document(document1)
    index.index_document(document2)
    index.index_document(document3)

    posting_lists = index.prepareForPrint()
    mmap = index.getMMAP()

    # dump into a file
    with open("mmap", "w") as f:
        f.write(str(mmap))

    # export posting lists
    with open("posting_lists", "w") as f:
        f.write(posting_lists)

main()