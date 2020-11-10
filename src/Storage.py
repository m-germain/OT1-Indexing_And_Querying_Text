class Storage:
    """
    In memory store representing the already indexed documents.
    """

    def __init__(self):
        self.store = dict()

    def __repr__(self):
        """
        String representation of the Dict object
        """
        return str(self.__dict__)

    def get(self, id):
        return self.store.get(id, None)

    def add(self, document):
        """
        Adds a document to the Store.
        """
        return self.store.update({document["id"]: document})

    def count(self):
        return len(self.store)

    def remove(self, document):
        """
        Removes document from the Store.
        """
        return self.store.pop(document["id"], None)
