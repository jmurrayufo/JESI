
import logging

from .Market import Market
from .Universe import Universe
from .Search import Search
from .Token import Token
from .Characters import Characters



class ESI:
    """Interface to the EVE ESI API
    """
    log = logging.getLogger("JESI").getChild(__module__)
    def __init__(self,log_level=logging.DEBUG):
        """No arguements (yet)
        """
        self.Characters = Characters(log_level=log_level)
        self.Market = Market(log_level=log_level)
        self.Search = Search(log_level=log_level)
        self.Token = Token(log_level=log_level)
        self.Universe = Universe(log_level=log_level)


    def __str__(self):
        return "JESI()"