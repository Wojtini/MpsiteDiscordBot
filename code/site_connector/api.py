import requests
import os


class User:
    def __init__(self, username, email=None):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"Username: {self.username}: Email: {self.email}"


class TankExpectation:
    def __init__(self, url):
        data = requests.get(url).json()
        self.tank_name = data['tank_name']
        self.exp_Def = data['exp_Def']
        self.exp_Frag = data['exp_Frag']
        self.exp_Spot = data['exp_Spot']
        self.exp_Damage = data['exp_Damage']
        self.exp_WinRate = data['exp_WinRate']

    def __repr__(self):
        return f"TankExpectation: {self.tank_name}"


class UserTankRating:
    def __init__(self, json_data):
        self.wot_username = json_data['wot_username']
        self.tank = TankExpectation(json_data['tank'])
        self.wn8 = json_data['wn8']
        self.lastUpdate = json_data['lastUpdate']
        self.dmgPerGame = json_data['dmgPerGame']
        self.winRate = json_data['winRate']

    def __repr__(self):
        return f"{self.tank}"


class MpsiteApi:
    def __init__(self, api_url=os.environ.get('API_URL')):
        self.url = api_url

    def get_guild_id(self):
        return None

    def get_text_channel_id(self):
        return None

    def get_wn8(self):
        url = f"{self.url}tankratings/"
        data = requests.get(url).json()
        # print(url)
        # print(data)
        result = {}
        for entry in data:
            result[entry['wot_username']] = []
        for entry in data:
            result[entry['wot_username']].append(UserTankRating(entry))
        return result


    def get_all_users(self):
        url = f"{self.url}users/"
        data = requests.get(url)
        data = data.json()
        result = []
        for i in data['results']:
            result.append(User(i['username']))
        return result


mpsite_api = MpsiteApi()