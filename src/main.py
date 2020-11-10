import nltk
#nltk.download('stopwords')

from Storage import Storage
from InvertedIndex import InvertedIndex


def highlight_term(id, term, text):
    # TODO Not good for the performances bcs we need to go throw the document to change the color.

    replaced_text = text.replace(
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

    index = InvertedIndex(store)
    index.loadInvertedIndex("mmap", "posting_lists")
   
    search_term = input("Enter term(s) to search: ")
    result = index.lookup_query(search_term)  


main()