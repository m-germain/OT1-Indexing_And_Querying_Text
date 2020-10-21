class Appearance:
    """
    Appearance is : {docId , frequency}
    Represents the appearance of a term in a given document, along with the
    frequency of appearances in the same one.
    """

    # TODO later the frequency will be something like 𝑠𝑐𝑜𝑟𝑒(𝑡_𝑖,𝑑_𝑗 )=𝑡𝑓(𝑡_𝑖,𝑑_𝑗 )  × 𝑖𝑑𝑓(𝑡_𝑖)

    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency

    def __repr__(self):
        """
        String representation of Appearance object
        """
        return str(self.__dict__)