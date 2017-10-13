
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
    def __init__(self, cache=True, log_level=logging.DEBUG):
        """No arguements (yet)
        """
        self.Characters = Characters(cache=cache, log_level=log_level)
        self.Market = Market(cache=cache, log_level=log_level)
        self.Search = Search(cache=cache, log_level=log_level)
        self.Token = Token(cache=cache, log_level=log_level)
        self.Universe = Universe(cache=cache, log_level=log_level)


    def __str__(self):
        return "JESI()"