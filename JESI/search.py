import requests
from requests_futures.sessions import FuturesSession



class search:
    """API Access to the /universe/ endpoints
    """
    base_url = "https://esi.tech.ccp.is/latest"

    def search(self,search,catagory=None,strict=False):
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
        raise NotImplementedError
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
