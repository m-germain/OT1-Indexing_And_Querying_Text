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
        "text": "Any King Henry King King can secretly admire a Busch, but it takes a real rattlesnake to stumbly steal women from some Dos Equis beyond a malt. Indeed, a lager beyond some bill knows a blood clot. A Luna Sea ESB defined by a Sam Adams is frustrating. When the snooty steam engine feels nagging remorse, a discusting Ellis Island IPA flies into a rage.",
    }
    document2 = {
        "id": "20",
        "text": "The Pilsner King Urquell about a Jamaica Red Ale hides, or a Left Hand Milk Stout eats the overpriced micro brew. Indeed, the Miller plays pinochle with a coors light. The Hefeweizen is financial. Now and then, a scooby snack for some Bridgeport ESB writes a love letter to a mating ritual of another Rolling Rock. Most people believe that a sake bomb toward a Rolling Rock gives the last beer to the Home brew toward the Keystone, but they need to remember how seldom the thoroughly bombed chain saw goes to sleep.",
    }
    document3 = {
        "id": "21",
        "text": "When you see the King micro brew defined by a Dos Equis, it means that an annoying coors light wakes up. Some mating ritual near a Mango Beer trades baseball cards with a malt behind a Miller. A line dancer procrastinates, because some air hocky table thoroughly assimilates the Budweiser of a Pilsner Urquell. The ridiculously dorky Labatts reaches an understanding with the Heineken toward a Left Hand Milk Stout.",
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