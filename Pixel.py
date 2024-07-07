import json
import requests
from colorama import Fore, Style


class Pixel:
    def __init__(self):
        with open('config.json', 'r') as file:
            config = json.load(file)

        self.headers = {
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "api-clicker.pixelverse.xyz",
            "If-None-Match": 'W/"29b-JPcgLG/Nvfd8KEVQN/lMKfPaHpQ"',
            "initData": config['initData'],
            "Origin": "https://sexyzbot.pxlvrs.io",
            "Priority": "u=3, i",
            "Referer": "https://sexyzbot.pxlvrs.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "secret": config['secret'],
            "tg-id": config['tgId'],
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
        }

    def getUsers(self):
        url = "https://api-clicker.pixelverse.xyz/api/users"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except (json.JSONDecodeError, requests.RequestException) as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ {e} ]")