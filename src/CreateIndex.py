import nltk
import mmap
import json
import glob
import datetime

#nltk.download('stopwords')

from Storage import Storage
from InvertedIndex import InvertedIndex
from FileReader import FileReader

def main():
    start = datetime.datetime.now()
    store = Storage()
    index = InvertedIndex(store)
   
    files = glob.glob("data/*")
    documents = []

    print(files)
    number_of_files = len(files)
    print(number_of_files)
    cut = int(number_of_files/32)
    print(cut)
    
    for file_path in files[:cut]:
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
    with open("posting_lists", "wb") as f:
        f.write(posting_lists)

    finish = datetime.datetime.now()
    print(finish - start)

main()