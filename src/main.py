import nltk
import glob
#nltk.download('stopwords')

from Storage import Storage
from InvertedIndex import InvertedIndex
from FileReader import FileReader


def highlight_term(id, terms, text):
    # TODO Not good for the performances bcs we need to go throw the document to change the color.
    replaced_text = text

    for term in terms:
        replaced_text = replaced_text.replace(
            # Bold High Intensty Yellow {term} Then Text Reset
            # More info on https://gist.github.com/vratiu/9780109
            term,
            "\033[1;93m {term} \033[0;0m".format(term=term),
        )
    return "--- document {id}: {replaced}".format(id=id, replaced=replaced_text)


def shrink_text(text):
    """
    Atm we have small sentences. So its ok but when we will have larger words it will be necessary to shrink the text.
    Should extract a part of the text with the given term in it..
    We may need to store the word position in the text in order to do this.
    """
    # TODO
    return text


def main():
    store = Storage()

    files = glob.glob("../data/*")
    documents = []

    number_of_files = len(files)

    # Change here the faction of the files you want to read.
    # Use the same number as the one used in Create Index.py
    cut = int(number_of_files/32)

    for file_path in files[:cut]:
        file_reader = FileReader(file_path)
        documents += file_reader.listDoc

    # We create an empty index
    index = InvertedIndex(store)

    # We give it the access of the mmap and PL files
    index.loadInvertedIndex("mmap", "posting_lists")


    search_term = input("Enter term(s) to search: ")

    # We query the index and retrive the sorted list of results
    result,dtime = index.lookup_query(search_term) 

    # We keep and display only the top K results.
    res = result[:3]
    for r in res:
        print("Score: "+ str(r[1]))
        doc = list(filter(lambda x: x.getId() == r[0], documents))[0]

        print( highlight_term(doc.getId(), search_term.split(), doc.getFullText() ) )
        print("\n")

    print(dtime)


main()