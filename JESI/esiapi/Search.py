
from requests_futures.sessions import FuturesSession
import logging
import requests



class Search:
    """API Access to the /universe/ endpoints
    """
    base_url = "https://esi.tech.ccp.is/latest"
    log = logging.getLogger("JESI").getChild(__module__)

    def __init__(self, cache=True, log_level=logging.DEBUG):
        Search.log.setLevel(log_level)
        pass

    def search(self, search,categories=None,strict=False):
        """Search for ID's that match the search
        Response Example:
        {
            "solarsystem": [
                30002510
            ],
            "station": [
                60004588,
                60004594,
                60005725,
                60009106,
                60012721,
                60012724,
                60012727
            ]
        }
        """

        valid_cats = ["agent",
                      "alliance",
                      "character",
                      "constellation",
                      "corporation",
                      "faction",
                      "inventorytype",
                      "region",
                      "solarsystem",
                      "station",
                      "wormhole",]

        for category in categories:
            if category not in valid_cats:
                raise ValueError(f"Given invalid category {category}")

        params = {"categories": categories,
                  "strict": strict,
                  "search": search}
        response = requests.get(self.base_url+f"/search/",params=params)
        response.raise_for_status()
        return response.json()


