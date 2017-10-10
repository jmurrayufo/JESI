import requests
from .token import token



class characters:
    base_url = "https://esi.tech.ccp.is/latest"

    def __init__(self):
        self.token = token()
        pass

    def characterIDs(self):
        baseURL = "https://login.eveonline.com/oauth/verify"

        headers = {
            "User-Agent":"JESI",
            "Authorization": f"Bearer {self.token}",
            "Host": "login.eveonline.com"
        }
        response = requests.get(baseURL,headers=headers)
        response.raise_for_status()
        # print(response)
        # print(response.json())
        return response.json()['CharacterID']


    """OFFICAL API ENDPOINTS"""

    def affiliation(self):
        raise NotImplementedError


    def names(self,character_ids):
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

    def characters(self,character_id):
        raise NotImplementedError


    def agents_research(self,character_id):
        raise NotImplementedError
        #:/


    def attributes(self,character_id):
        raise NotImplementedError
        #:/


    def blueprints(self,character_id):
        raise NotImplementedError
        #:/


    def bookmarks(self,character_id):
        raise NotImplementedError
        #:/


    def bookmarks(self,character_id):
        raise NotImplementedError
        #:/folders/


    def calendar(self,character_id):
        raise NotImplementedError
        #:/


    def calendar(self,character_id):
        raise NotImplementedError
        #:/{event_id}/


    def calendar(self,character_id):
        raise NotImplementedError
        #:/{event_id}/attendees/


    def chat_channels(self,character_id):
        raise NotImplementedError
        #:/


    def clones(self,character_id):
        raise NotImplementedError
        #:/


    def contacts(self,character_id):
        raise NotImplementedError
        #:/


    def contacts(self,character_id):
        raise NotImplementedError
        #:/labels/


    def contracts(self,character_id):
        raise NotImplementedError
        #:/


    def contracts(self,character_id):
        raise NotImplementedError
        #:/{contract_id}/bids/


    def contracts(self,character_id):
        raise NotImplementedError
        #:/{contract_id}/items/


    def corporationhistory(self,character_id):
        raise NotImplementedError
        #:/


    def cspa(self,character_id):
        raise NotImplementedError
        #:/


    def fatigue(self,character_id):
        raise NotImplementedError
        #:/


    def fittings(self,character_id):
        raise NotImplementedError
        #:/


    def fittings(self,character_id):
        raise NotImplementedError
        #:/{fitting_id}/


    def implants(self,character_id):
        raise NotImplementedError
        #:/


    def industry(self,character_id):
        raise NotImplementedError
        #:/jobs/


    def killmails(self,character_id):
        raise NotImplementedError
        #:/recent/


    def location(self,character_id):
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


    def loyalty(self,character_id):
        raise NotImplementedError
        #:/points/


    def mail(self,character_id):
        raise NotImplementedError
        #:/


    def mail(self,character_id):
        raise NotImplementedError
        #:/labels/


    def mail(self,character_id):
        raise NotImplementedError
        #:/labels/{label_id}/


    def mail(self,character_id):
        raise NotImplementedError
        #:/lists/


    def mail(self,character_id):
        raise NotImplementedError
        #:/{mail_id}/


    def medals(self,character_id):
        raise NotImplementedError
        #:/


    def notifications(self,character_id):
        raise NotImplementedError
        #:/


    def notifications(self,character_id):
        raise NotImplementedError
        #:/contacts/


    def online(self,character_id):
        raise NotImplementedError
        #:/


    def opportunities(self,character_id):
        raise NotImplementedError
        #:/


    def orders(self,character_id):
        """List market orders placed by a character
        """
        params = {
            "character_id": character_id,
            "token": f"{self.token}"
        }
        response = requests.get(self.base_url+f"/characters/{character_id}/orders/",params=params)
        response.raise_for_status()
        return response.json()


    def planets(self,character_id,planet_id=None):
        raise NotImplementedError
        #:/{planet_id}/


    def portrait(self,character_id):
        raise NotImplementedError
        #:/


    def roles(self,character_id):
        raise NotImplementedError
        #:/


    def search(self,character_id):
        raise NotImplementedError
        #:/


    def ship(self,character_id):
        raise NotImplementedError
        #:/


    def skillqueue(self,character_id):
        raise NotImplementedError
        #:/


    def skills(self,character_id):
        raise NotImplementedError
        #:/


    def standings(self,character_id):
        raise NotImplementedError
        #:/

    #TODO: Move this to the wallet class
    def wallet(self,character_id):
        raise NotImplementedError
        #:/


    #TODO: Move this to the wallet class
    def wallet(self,character_id):
        raise NotImplementedError
        #:/journal/


    #TODO: Move this to the wallet class
    def wallet(self,character_id):
        raise NotImplementedError
        #:/transactions/

