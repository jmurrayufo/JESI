

from .Market import Market
from .Universe import Universe
from .Search import Search
from .Token import Token
from .Characters import Characters



class JESI:
    """Interface to the EVE ESI API
    """
    def __init__(self):
        """No arguements (yet)
        """
        self.Characters = Characters()
        self.Market = Market()
        self.Search = Search()
        self.Token = Token()
        self.Universe = Universe()


    def __str__(self):
        return "JESI()"