class Document:
    """
    This class represent a document object
    DOCNO ex : BE100890-0140
    DOCID ex : 289774
    TEXT the body of the article.
    """
    
    def __init__(self, no = "", doc_id = "", text = ""):
        self.no = no
        self.doc_id = doc_id
        self.text = text

    def getFullText(self):
        return self.headline + self.by_line + self.text

    def getId(self):
        return self.id