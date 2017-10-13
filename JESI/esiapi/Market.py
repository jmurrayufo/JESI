
from requests_futures.sessions import FuturesSession
import logging
import requests


class Market:
    """API Access to the /market/ endpoints
    """
    base_url = "https://esi.tech.ccp.is/latest"
    log = logging.getLogger("JESI").getChild(__module__)

    def __init__(self, cache=True, log_level=logging.DEBUG):
        Market.log.setLevel(log_level)
        pass

    def groups(self, market_group_id=None):
        """Not implemented
        """
        raise NotImplementedError


    def prices(self):
        """Check current market prices

        Returns:
        Dicts of prices, by type_id
        {
          "adjusted_price": 306988.09,
          "average_price": 306292.67,
          "type_id": 32772
        }
        """
        response = requests.get(self.base_url+f"/markets/prices/")
        response.raise_for_status()
        return response.json()


    def history(self, region_id,type_id):
        """Return a list of historical market statistics for the specified type in a region
        """
        params = {
            'region_id':region_id,
            'type_id':type_id
        }
        response = requests.get(self.base_url + f"/markets/{region_id}/history/", params=params)
        response.raise_for_status()
        return response.json()


    def historyIter(self, region_id,type_id):
        """Return an iterator of historical market statistics for the specified type in a region
        """
        params = {
            'region_id':region_id,
            'type_id':type_id
        }
        response = requests.get(self.base_url + f"/markets/{region_id}/history/", params=params)
        response.raise_for_status()
        for item in response.json():
            yield item
        return


    def orders(self, region_id,page=-1,type_id=None):
        """Return orders for a region

        Keyword arguments:
        region_id [REQUIRED] -- The numeric region_id to search
        page -- Page to retrieve. -1 for all of them
        type_id -- Specific item to look for. Overides page
        """
        if page == -1:
            retVal = []
            i = 1
            while 1:
                params = {'page':i}
                response = requests.get(self.base_url+f"/markets/{region_id}/orders/",params=params)
                data = response.json()
                if response.status_code == 200 and len(data):
                    retVal.append(data)
                i += 1
            return retVal

        elif type_id is not None:
            params = {'type_id':i}
            response = requests.get(self.base_url+f"/markets/{region_id}/orders/",params=params)
            data = response.json()
            if response.status_code == 200:
                return data
            else:
                raise IOError(f"Got status code {response.status_code}")

        elif page > 0:
            params = {'page':page}
            response = requests.get(self.base_url+f"/markets/{region_id}/orders/",params=params)
            data = response.json()
            if response.status_code == 200:
                return data
            else:
                raise IOError(f"Got status code {response.status_code}")
        else:
            raise AttributeError("Unknown argument combo")


    def ordersIter(self, region_id,type_id=None):
        """Return orders for a region

        Keyword Arguments:
        region_id [REQUIRED] -- The numeric region_id to search
        type_id -- Specific item to look for. Overides page
        """
        i = 1
        while 1:
            params = {'page':i}
            response = requests.get(self.base_url+f"/markets/{region_id}/orders/",params=params)
            response.raise_for_status()
            data = response.json()
            if len(data):
                for order in data:
                    yield order
            else:
                return
            i += 1


    def types(self, region_id,page=-1):
        """Return a list of type IDs that have active orders in the region, for efficient market indexing.
        """
        returnList = []
        page = 1
        while 1:
            params = {'page':page}
            response = requests.get(self.base_url+f"/markets/{region_id}/types/",params=params)
            response.raise_for_status()
            data = response.json()
            if len(data):
                returnList += response.json()
            else:
                return returnList
            page += 1


    def typesIter(self, region_id,page=-1):
        page = 1
        while 1:
            params = {'page':page}
            response = requests.get(self.base_url+f"/markets/{region_id}/types/",params=params)
            data = response.json()
            if response.status_code == 200 and len(data):
                for order in data:
                    yield order
            else:
                return
            page += 1