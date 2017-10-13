
from requests_futures.sessions import FuturesSession
import collections
import requests
import time


"""TODO Update me
"""

class Universe:
    """API Access to the /universe/ endpoints
    """
    base_url = "https://esi.tech.ccp.is/latest"


    def bloodlines(self):
        """Not implemented
        """
        raise NotImplementedError


    def categories(self,category_id=None):
        """Not implemented
        """
        raise NotImplementedError


    def constellations(self,constellation_id):
        """Get a list of constellations or Get information on a constellation

        Returns:
        {
            "constellation_id": 20000009,
            "name": "Mekashtad",
            "position": {
                "x": 67796138757472320,
                "y": -70591121348560960,
                "z": -59587016159270070
            },
            "region_id": 10000001,
            "systems": [
                20000302,
                20000303
            ]
        }        
        """
        if constellation_id is None:
            response = requests.get(self.base_url+f"/universe/constellations/")
        else:
            response = requests.get(self.base_url+f"/universe/constellations/{constellation_id}")
        response.raise_for_status()
        return response.json()


    def factions(self):
        """Not implemented
        """
        raise NotImplementedError


    def graphics(self,graphic_id=None):
        """Not implemented
        """
        raise NotImplementedError


    def groups(self,group_id=None):
        """Not implemented
        """
        raise NotImplementedError


    def moons(self,moon_id):
        """Not implemented
        """
        raise NotImplementedError


    def names(self,names):
        """Not implemented
        """
        raise NotImplementedError


    def planets(self,planet_id):
        """Not implemented
        """
        raise NotImplementedError


    def races(self):
        """Not implemented
        """
        raise NotImplementedError


    def regions(self,region_id=None):
        """Get a list of regions or Get information on a region

        Returns:
        List of region ids, or
        {
            "constellations": [
                20000302,
                20000303
            ],
            "description": "It has long been an established fact of civilization...",
            "name": "Metropolis",
            "region_id": 10000042
        }
        """
        if region_id is None:
            response = requests.get(self.base_url+f"/universe/regions/")
        else:
            response = requests.get(self.base_url+f"/universe/regions/{region_id}")
        response.raise_for_status()
        return response.json()



    def schematics(self,schematic_id):
        """Not implemented
        """
        raise NotImplementedError


    def stargates(self,stargate_id):
        """Get information on a stargate
        """
        response = requests.get(self.base_url+f"/universe/stargates/{stargate_id}")
        response.raise_for_status()
        return response.json()


    def stars(self,star_id):
        """Not implemented
        """
        raise NotImplementedError


    def stations(self,station_id):
        """Get information on a station
        """
        response = requests.get(self.base_url+f"/universe/stations/{station_id}")
        response.raise_for_status()
        return response.json()


    def structures(self,structure_id):
        """Not implemented
        """
        raise NotImplementedError


    def system_jumps(self):
        """Not implemented
        """
        raise NotImplementedError


    def system_kills(self):
        """Not implemented
        """
        raise NotImplementedError


    def systems(self,system_id=None):
        """Get a list of solar systems or Get information on a specific system
        """
        if system_id is None:
            response = requests.get(self.base_url+f"/universe/systems/")
        else:
            response = requests.get(self.base_url+f"/universe/systems/{system_id}")
        response.raise_for_status()
        return response.json()


    def types(self, type_id=None):
        """Return completed list of request

        Keyword Arguments:
        type_id -- None to scan id's only, a single type to lookup details or a 
        list/tuple to lookup details.

        Returns:
        Depending on the arguments given, will return a list (for type_id being 
        None or a list/tuple), or a single element if only asked for a single 
        item.
        """
        if type_id is None:
            type_ids = []
            with FuturesSession(max_workers=10) as session:
                futureQueue = []
                page = 0
                for i in range(1,11):
                    page = i
                    params = {"page": page}
                    future = session.get(self.base_url+f"/universe/types/",params=params)
                    futureQueue.append(future)

                while 1:
                    # print(list(map(lambda x:x.done(),futureQueue)))
                    # TODO: This could just sweep the list looking for a completed response, and not hang
                    future = futureQueue.pop(0)
                    response = future.result()
                    response.raise_for_status()
                    data = response.json()
                    if len(data) == 0:
                        break
                    type_ids += response.json()

                    # Queue up our next page (This is really 10 pages in the future)
                    params = {"page": page}
                    future = session.get(self.base_url+f"/universe/types/",params=params)
                    futureQueue.append(future)

                    page += 1
            return type_ids

        elif type(type_id) in [int,str]:
            params = {"type_id": type_id}
            response = requests.get(self.base_url+f"/universe/types/{type_id}/",params=params)
            response.raise_for_status()
            return response.json()

        elif isinstance(type_id, collections.Iterable):
            session = FuturesSession(max_workers=10)
            request_list = []
            for next_type_id in type_id:
                params = {"type_id": next_type_id}
                response = session.get(self.base_url+f"/universe/types/{next_type_id}/",params=params)
                request_list.append(response)

            retVal = []
            for response in request_list:
                result = response.result()
                result.raise_for_status()
                retVal.append(result.json())
            return retVal


    def typesIter(self,type_id=None):
        """As with types, but return an iterator
        """
        if type_id is None:
            type_ids = []
            with FuturesSession(max_workers=10) as session:
                # We keep a Q of 10 requests going
                futureQueue = []
                page = 0
                for i in range(1,11):
                    page = i
                    params = {"page": page}
                    future = session.get(self.base_url+f"/universe/types/",params=params)
                    futureQueue.append(future)

                while 1:
                    # print(list(map(lambda x:x.done(),futureQueue)))
                    # TODO: This could just sweep the list looking for a completed response, and not hang
                    future = futureQueue.pop(0)
                    response = future.result()
                    response.raise_for_status()
                    data = response.json()
                    if len(data) == 0:
                        return
                    for t in data:
                        yield t

                    # Queue up our next page (This is really 10 pages in the future)
                    params = {"page": page}
                    future = session.get(self.base_url+f"/universe/types/",params=params)
                    futureQueue.append(future)

                    page += 1

        elif type(type_id) in [int,str]:
            params = {"type_id": type_id}
            response = requests.get(self.base_url+f"/universe/types/{type_id}/",params=params)
            response.raise_for_status()
            yield response.json()
            return

        elif isinstance(type_id, collections.Iterable):
            future_list = []
            with FuturesSession(max_workers=16) as session:
                for next_type_id in type_id:
                    # print('q')
                    params = {"type_id": next_type_id}
                    response = session.get(self.base_url+f"/universe/types/{next_type_id}/",params=params)
                    future_list.append(response)
                    idx = 0
                    while len(future_list) > 10:
                        if future_list[idx%len(future_list)].done():
                            future = future_list.pop(idx)
                            result = future.result()
                            result.raise_for_status()
                            # help(result)
                            print(dir(result))
                            print(result.headers)
                            exit()
                            yield result.json()

                for future in request_list:
                    result = future.result()
                    result.raise_for_status()
                    yield result.json()
            return
