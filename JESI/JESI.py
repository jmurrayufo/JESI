

from .market import market
from .universe import universe
from .search import search
from .token import token
from .characters import characters



class JESI:
    """Interface to the EVE ESI API
    """
    def __init__(self):
        """No arguements (yet)
        """
        self.characters = characters()
        self.market = market()
        self.search = search()
        self.token = token()
        self.universe = universe()


    def __str__(self):
        return "JESI()"