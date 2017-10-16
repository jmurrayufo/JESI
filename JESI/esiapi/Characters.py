
import logging
import requests

from .Token import Token



class Characters:
    """API to the /characters/ endpoints
    """
    base_url = "https://esi.tech.ccp.is/latest"
    log = logging.getLogger("JESI").getChild(__module__)


    def __init__(self, cache=True, log_level=logging.DEBUG):
        Characters.log.setLevel(log_level)
        self.token = Token()
        pass


    def characterID(self):
        """Return the character ID active on the account
        """
        baseURL = "https://login.eveonline.com/oauth/verify"

        headers = {
            "User-Agent":"JESI",
            "Authorization": f"Bearer {self.token}",
            "Host": "login.eveonline.com"
        }
        response = requests.get(baseURL,headers=headers)
        response.raise_for_status()
        return response.json()['CharacterID']


    """OFFICAL API ENDPOINTS"""

    def affiliation(self):
        """Not implemented
        """
        raise NotImplementedError


    def names(self, character_ids):
        """List of id/name associations
        """
        assert type(character_ids) in [list,tuple] # Will become a comma separated list of character IDs
        character_ids = [str(x) for x in character_ids]
        params = {
            "character_ids": ",".join(character_ids),
        }
        response = requests.get(self.base_url+"/characters/names/",params=params)
        response.raise_for_status()
        return response.json()


    def characters(self, character_id):
        """Not implemented
        """
        raise NotImplementedError


    def agents_research(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def attributes(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def blueprints(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def bookmarks(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def bookmarks(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/folders/


    def calendar(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def calendar(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/{event_id}/


    def calendar(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/{event_id}/attendees/


    def chat_channels(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def clones(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def contacts(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def contacts(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/labels/


    def contracts(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def contracts(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/{contract_id}/bids/


    def contracts(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/{contract_id}/items/


    def corporationhistory(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def cspa(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def fatigue(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def fittings(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def fittings(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/{fitting_id}/


    def implants(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def industry(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/jobs/


    def killmails(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/recent/


    def location(self, character_id):
        """Information about the characters current location. Returns the current solar system id, and also the current station or structure ID if applicable.
        """
        params = {
            "character_id": character_id,
            "token": f"{self.token}"
        }
        response = requests.get(self.base_url+f"/characters/{character_id}/location/",params=params)
        response.raise_for_status()
        return response.json()
        #:/


    def loyalty(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/points/


    def mail(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def mail(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/labels/


    def mail(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/labels/{label_id}/


    def mail(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/lists/


    def mail(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/{mail_id}/


    def medals(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def notifications(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def notifications(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/contacts/


    def online(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def opportunities(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def orders(self, character_id):
        """List market orders placed by a character
        """
        params = {
            "character_id": character_id,
            "token": f"{self.token}"
        }
        response = requests.get(self.base_url+f"/characters/{character_id}/orders/",params=params)
        response.raise_for_status()
        return response.json()


    def planets(self, character_id, planet_id=None):
        """Returns a list of all planetary colonies owned by a character or 
        Returns full details on the layout of a single planetary colony, 
        including links, pins and routes. Note: Planetary information is only 
        recalculated when the colony is viewed through the client. Information 
        will not update until this criteria is met.
        """
        if planet_id is None:

            params = {
                "character_id": character_id,
                "token": f"{self.token}"
            }
            response = requests.get(self.base_url+f"/characters/{character_id}/planets/",params=params)
            response.raise_for_status()
            return response.json()
        
        # else:

        params = {
            "character_id": character_id,
            "planet_id": planet_id,
            "token": f"{self.token}"
        }
        response = requests.get(self.base_url+f"/characters/{character_id}/planets/{planet_id}",params=params)
        response.raise_for_status()
        return response.json()


    def portrait(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def roles(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def search(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def ship(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def skillqueue(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def skills(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    def standings(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/

    #TODO: Move this to the wallet class
    def wallet(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/


    #TODO: Move this to the wallet class
    def wallet(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/journal/


    #TODO: Move this to the wallet class
    def wallet(self, character_id):
        """Not implemented
        """
        raise NotImplementedError
        #:/transactions/

