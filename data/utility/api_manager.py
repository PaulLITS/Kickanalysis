import time
from datetime import datetime
import requests

from kickbase_api.kickbase import Kickbase

from utility.constants import TIMEZONE_DE

login_url = "https://api.kickbase.com/v4/user/login"

import datetime


def parse_date(timestamp) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(timestamp)

class ApiManager:
    def __init__(self):
        self.users = None
        self.throttle = None
        self.cache = None
        self.league = None
        self.api = None
        self.start = None

    def init(self, options):
        # Kickbase login
        login_payload = {
        "em": options.mail,
        "loy": "false",
        "pass": options.pw,
        "rep": {}
        }
        
        session = requests.Session()
        response = session.post(login_url, json=login_payload)
        if response.status_code == 200:
            j = response.json()
            self.token = j["tkn"]
            self.token_expire = parse_date(j["tknex"])

            self._username = options.mail
            self._password = options.pw

            user = Kickbase.User(j["u"])
            leagues = [Kickbase.LeagueData(d) for d in j["srvl"]]

        elif response.status_code == 401:
            raise Exception()
        else:
            raise Exception()

        # Setup league
        if options.league:
            self.league = None
            for league in leagues:
                if league.name == options.league:
                    self.league = league

            if self.league is None:
                raise Exception(f'League "{options.league}" not found.')
        else:
            self.league = leagues[0]

        self.cache = {}
        self.throttle = 0.01

        # Setup user list
        self.users = [user for user in self.api.league_users(self.league)
                      if user.name not in options.ignore]

        self.start = TIMEZONE_DE.localize(datetime.strptime(options.start, '%d.%m.%Y'))

    def get(self, url: str):
        if url not in self.cache.keys():
            time.sleep(self.throttle)

            delay = time.time()
            self.cache[url] = self.api._do_get(url, True).json()
            delay = time.time() - delay

            self.throttle = (self.throttle + delay) / 2

            if self.throttle > 1:
                self.throttle = 1

        return self.cache[url]

    def get_transfers_raw(self, user_id):
        transfers_raw = []
        offset = 0

        response = self.get(f'/leagues/{self.league.id}/users/{user_id}/feed?filter=12&start={offset}')

        while response['items']:
            transfers_raw = transfers_raw + response['items']
            response = self.get(f'/leagues/{self.league.id}/users/{user_id}/feed?filter=12&start={offset}')
            offset += 25

        return transfers_raw


manager = ApiManager()
