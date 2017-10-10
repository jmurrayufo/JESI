


class assets:
    baseUrl = "https://esi.tech.ccp.is/latest"
    token = token()

    # Should we move these into an assets class?
    def __call__(self,character_id,page=-1):
        raise NotImplementedError
        #:/


    # Should we move these into an assets class?
    def locations(self,character_id):
        """Return locations for a set of item ids, which you can get from character assets endpoint. Coordinates for items in hangars or stations are set to (0,0,0)
        """
        raise NotImplementedError
        #:/locations/


    # Should we move these into an assets class?
    def assetsNames(self,character_id):
        """Return names for a set of item ids, which you can get from character assets endpoint. Typically used for items that can customize names, like containers or ships.
        """
        raise NotImplementedError
        #:/names/