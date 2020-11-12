import nltk
import mmap
import json
import glob

#nltk.download('stopwords')

from Storage import Storage
from InvertedIndex import InvertedIndex
from FileReader import FileReader
from Document import Document

def main():
    store = Storage()
    index = InvertedIndex(store)

    # files = glob.glob("data/*")
    # documents = []
    
    # for file_path in files[:1]:
    #     file_reader = FileReader(file_path)
    #     documents += file_reader.listDoc
   
    # for document in documents:
    #     index.index_document(document)


    document2 = Document(
         "21AE",
         "22",
        "China is a country located in East Asia bordering fourteen other countries, including Mongolia to the north; Kazakhstan, Kyrgyzstan, Tajikistan, Afghanistan, and Pakistan to the west; India, Nepal, and Bhutan to the southwest; Myanmar, Laos, and Vietnam to the south; "
    )

    document1 = Document(
         "21AE",
         "1",
        "Water colorless chemical substance, which is the main constituent of Earth's hydrosphere and the fluids of all known living organisms. "
    )
    
    document3 = Document(
         "21AE",
         "21",
        "Water is an inorganic, transparent, tasteless, odorless, and nearly colorless chemical substance, which is the main constituent of Earth's hydrosphere and the fluids of all known living organisms. "
    )
   
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