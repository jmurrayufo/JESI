
from base64 import b64encode
from pathlib import Path
from requests import Request, Session, post
import datetime
import json
import logging
import re
import textwrap
import urllib.parse

class Token:
    # accessToken = None
    # refreshToken = None
    # expiresAt = None
    initilized = False
    token_file = Path("tokens.json")
    log = logging.getLogger("JESI").getChild(__module__)

    def __init__(self,log_level=logging.DEBUG):
        Token.log.setLevel(log_level)
        # Do we have a token file?
        if Token.initilized:
            return
        elif Token.token_file.is_file():
            with open(Token.token_file,'r') as fp:
                data = json.load(fp)
            Token.refreshToken = data['refresh_token']
            Token.expiresAt = datetime.datetime.now()
            self._refreshToken()
        else:
            self.authorize()
        Token.initilized = True


    def __str__(self):
        if datetime.datetime.now() > Token.expiresAt:
            self._refreshToken()
        return f"{Token.accessToken}"


    def myStr(self):
        retval = "token<"
        retval += f"{Token.accessToken[:5]}...{Token.accessToken[-5:]}"
        retval += f",{Token.expiresAt - datetime.datetime.now()}"
        retval += ">"
        return retval


    def _refreshToken(self):
        tokenUrl = "https://login.eveonline.com/oauth/token"
        headers = self.authHeaders()
        payload = {
            'grant_type':'refresh_token',
            'refresh_token':f"{Token.refreshToken}",
        }
        response = post(tokenUrl, data=payload, headers=headers)
        assert response.status_code == 200
        response = response.json()

        with open(Token.token_file,'w') as fp:
            json.dump(response,fp)
        Token.accessToken = response['access_token']
        Token.refreshToken = response['refresh_token']
        Token.expiresAt = datetime.datetime.now() + datetime.timedelta(seconds=response['expires_in'])


    def authHeaders(self):
        client_id = "408f4727dace4efe96b9d37b9f7644ef"
        client_secret = "KGgNYDpMQ4ExGMyeuXJP5KuWtSn6rtdeOtTpBf2j"
        authHeader = b64encode(f"{client_id}:{client_secret}".encode('ascii'))
        authHeader = f"Basic {str(authHeader.decode('ascii'))}"
        headers = {
            'Authorization': authHeader,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'login.eveonline.com',
        }
        return headers


    def authorize(self):
        """Get authoriziation to use the api.

        This should only need to be called once! EVER!
        """
        # TODO: client_id is hard coded here. FIX THAT
        authUrl = "https://login.eveonline.com/oauth/authorize"
        params = {
            'response_type': 'code',  # Must be set to “code”.
            'redirect_uri': 'https://localhost/callback',  # After authentication the user will be redirected to this URL on your website. It must match the definition on file in the developers site.
            'client_id': '408f4727dace4efe96b9d37b9f7644ef', #A string identifier for the client, provided by CCP.
            'scope': " ".join([
                "esi-calendar.respond_calendar_events.v1",
                "esi-calendar.read_calendar_events.v1",
                "esi-location.read_location.v1",
                "esi-location.read_ship_type.v1",
                "esi-mail.organize_mail.v1",
                "esi-mail.read_mail.v1",
                "esi-mail.send_mail.v1",
                "esi-skills.read_skills.v1",
                "esi-skills.read_skillqueue.v1",
                "esi-wallet.read_character_wallet.v1",
                "esi-wallet.read_corporation_wallet.v1",
                "esi-search.search_structures.v1",
                "esi-clones.read_clones.v1",
                "esi-characters.read_contacts.v1",
                "esi-universe.read_structures.v1",
                "esi-bookmarks.read_character_bookmarks.v1",
                "esi-killmails.read_killmails.v1",
                "esi-corporations.read_corporation_membership.v1",
                "esi-assets.read_assets.v1",
                "esi-planets.manage_planets.v1",
                "esi-fleets.read_fleet.v1",
                "esi-fleets.write_fleet.v1",
                "esi-ui.open_window.v1",
                "esi-ui.write_waypoint.v1",
                "esi-characters.write_contacts.v1",
                "esi-fittings.read_fittings.v1",
                "esi-fittings.write_fittings.v1",
                "esi-markets.structure_markets.v1",
                "esi-corporations.read_structures.v1",
                "esi-corporations.write_structures.v1",
                "esi-characters.read_loyalty.v1",
                "esi-characters.read_opportunities.v1",
                "esi-characters.read_chat_channels.v1",
                "esi-characters.read_medals.v1",
                "esi-characters.read_standings.v1",
                "esi-characters.read_agents_research.v1",
                "esi-industry.read_character_jobs.v1",
                "esi-markets.read_character_orders.v1",
                "esi-characters.read_blueprints.v1",
                "esi-characters.read_corporation_roles.v1",
                "esi-location.read_online.v1",
                "esi-contracts.read_character_contracts.v1",
                "esi-clones.read_implants.v1",
                "esi-characters.read_fatigue.v1",
                "esi-killmails.read_corporation_killmails.v1",
                "esi-corporations.track_members.v1",
                "esi-wallet.read_corporation_wallets.v1",
                "esi-characters.read_notifications.v1",
                "esi-corporations.read_divisions.v1",
                "esi-corporations.read_contacts.v1",
                "esi-assets.read_corporation_assets.v1",
                "esi-corporations.read_titles.v1",
                "esi-corporations.read_blueprints.v1",
            ]), #The requested scopes as a space delimited string.
            'state': 'myState', #An opaque value used by the client to maintain state between the request and callback. The SSO includes this value when redirecting back to the 3rd party website. While not required, it is important to use this for security reasons. http://www.thread-safe.com/2014/05/the-correct-use-of-state-parameter-in.html explains why the state parameter is needed.
        }
        req = Request('GET', authUrl, params=params) # headers=headers
        prepped = req.prepare()
        print("Please access SSO from the following link.")
        print("We only ever need to do this once.")
        print()
        print(prepped.url)
        print()
        print("""Once you authorized the SOO, paste the full url you were 
            redirected to. back in this application
            """)
        print("Be aware, this URL will fail to load on your browser. Thats ok! Just paste the URL.")

        retUrl = input("> ")

        authCode = re.search("code=(.*)&",retUrl)
        assert authCode, "Didn't find a valid URL to parse"
        authCode = authCode.groups()[0]

        tokenUrl = "https://login.eveonline.com/oauth/token"
        headers = self.authHeaders()
        payload = {
            'grant_type':'authorization_code',
            'code':f"{authCode}",
        }
        response = post(tokenUrl, data=payload, headers=headers)
        assert response.status_code == 200

        response = response.json()
        with open(Token.token_file,'w') as fp:
            json.dump(response,fp)
        Token.accessToken = response['access_token']
        Token.refreshToken = response['refresh_token']
        Token.expiresAt = datetime.datetime.now() + datetime.timedelta(seconds=response['expires_in'])