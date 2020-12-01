import xml.etree.ElementTree as ET
from Document import Document

class FileReader:
    """
    This class let us read an XML File.
    """

    def __init__(self, path):
        self.path = path
        self.listDoc = []
        
        # Open the data file
        f = open(self.path, "r").read()

        # Fake a root XML balise and save all in a string.
        xml_string = f"<dummy_root>{f}</dummy_root>"

        try:
            print(self.path)

            # Open the xml string with ET
            root = ET.fromstring(xml_string)

            # We iterrate on all the doc that we found
            for doc in root.iter("DOC"):
                document = Document()

                # Here we dont check if we found DOCID
                # It would be better but we have a bug and can't see the id if we do this...
                document.doc_id = doc.find("DOCID").text
                document.no = doc.find("DOCNO").text

                # When we get the Text we iterrate on all the <P> To create the document text.
                if doc.find("TEXT"):
                    body = doc.find("TEXT")
                    for p in body.iter("P"):
                        document.text += p.text

                self.listDoc.append(document)
        except:
            print("File not parsed ! "+self.path)