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
    document1 = {
        "id": "1",
        "text": "Any King Henry can secretly admire a Busch, but it takes a real rattlesnake to stumbly steal women from some Dos Equis beyond a malt. Indeed, a lager beyond some bill knows a blood clot. A Luna Sea ESB defined by a Sam Adams is frustrating. When the snooty steam engine feels nagging remorse, a discusting Ellis Island IPA flies into a rage.",
    }
    document2 = {
        "id": "2",
        "text": "The Pilsner Urquell about a Jamaica Red Ale hides, or a Left Hand Milk Stout eats the overpriced micro brew. Indeed, the Miller plays pinochle with a coors light. The Hefeweizen is financial. Now and then, a scooby snack for some Bridgeport ESB writes a love letter to a mating ritual of another Rolling Rock. Most people believe that a sake bomb toward a Rolling Rock gives the last beer to the Home brew toward the Keystone, but they need to remember how seldom the thoroughly bombed chain saw goes to sleep.",
    }
    document3 = {
        "id": "3",
        "text": "When you see the micro brew defined by a Dos Equis, it means that an annoying coors light wakes up. Some mating ritual near a Mango Beer trades baseball cards with a malt behind a Miller. A line dancer procrastinates, because some air hocky table thoroughly assimilates the Budweiser of a Pilsner Urquell. The ridiculously dorky Labatts reaches an understanding with the Heineken toward a Left Hand Milk Stout.",
    }
    index.index_document(document1)
    index.index_document(document2)
    index.index_document(document3)

    search_term = input("Enter term(s) to search: ")
    result = index.lookup_query(search_term)

    for term in result.keys():
        for appearance in result[term]:
            # Belgium: { docId: 1, frequency: 1}
            document = store.get(appearance.docId)
            print(highlight_term(appearance.docId, term, document["text"]))
        print("-----------------------------")


main()