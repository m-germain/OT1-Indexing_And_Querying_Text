import nltk
import mmap
import json
import glob

#nltk.download('stopwords')

from Storage import Storage
from InvertedIndex import InvertedIndex
from FileReader import FileReader

def main():
    store = Storage()
    index = InvertedIndex(store)

    files = glob.glob("data/*")
    documents = []
    
    for file_path in files[:2]:
        file_reader = FileReader(file_path)
        documents += file_reader.listDoc
   
    for document in documents:
        index.index_document(document)

    posting_lists = index.prepareForPrint()
    mmap = index.getMMAP()

    # dump into a file
    with open("mmap", "w") as f:
        f.write(str(mmap))

    # export posting lists
    with open("posting_lists", "w") as f:
        f.write(posting_lists)

main()