import asyncio
import json
import websockets
from colorama import Fore, Style
from random import randint

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

class Battle:
    wins = 0
    loses = 0
    rewardWins = 0
    rewardLoses = 0
    winRate = 0

    def __init__(self):
        with open('config.json', 'r') as file:
            config = json.load(file)

        self.initData = config['initData']
        self.secret = config['secret']
        self.tgId = config['tgId']
        self.websocket: websockets.WebSocketClientProtocol = None
        self.battleId = ""
        self.superHit = False
        self.strike = {
            "defense": False,
            "attack": False
        }
        self.stop_event = asyncio.Event()

    async def sendHit(self):
        while not self.stop_event.is_set():
            if self.superHit:
                await asyncio.sleep(0.4)
                continue

            content = [
                "HIT",
                {
                    "battleId": self.battleId
                }
            ]

            try:
                await self.websocket.send(f"42{json.dumps(content)}")
            except:
                return
            await asyncio.sleep(0.11)

    async def listenerMsg(self):
        while not self.stop_event.is_set():
            try:
                data = await self.websocket.recv()
            except Exception:
                self.stop_event.set()
                return

            if data.startswith('42'):
                data = json.loads(data[2:])
                if data[0] == "HIT":
                    print(f"🤬 {Fore.CYAN+Style.BRIGHT}[ {self.player1['name']} ] ({data[1]['player1']['energy']}) 👀 ({data[1]['player2']['energy']}) [ {self.player2['name']} ]")
                elif data[0] == "SET_SUPER_HIT_PREPARE":
                    self.superHit = True
                elif data[0] == "SET_SUPER_HIT_ATTACK_ZONE":
                    content = [
                        "SET_SUPER_HIT_ATTACK_ZONE",
                        {
                            "battleId": self.battleId,
                            "zone": randint(1, 4)
                        }
                    ]

                    await self.websocket.send(f"42{json.dumps(content)}")
                    self.strike['attack'] = True
                elif data[0] == "SET_SUPER_HIT_DEFEND_ZONE":
                    content = [
                        "SET_SUPER_HIT_DEFEND_ZONE",
                        {
                            "battleId": self.battleId,
                            "zone": randint(1, 4)
                        }
                    ]

                    await self.websocket.send(f"42{json.dumps(content)}")
                    self.strike['defense'] = True
                elif data[0] == "ENEMY_LEAVED":
                    await self.websocket.recv()
                    self.stop_event.set()
                    return
                elif data[0] == "END":
                    if data[1]['result'] == "WIN":
                        Battle.wins += 1
                        Battle.rewardWins += data[1]['reward']
                    else:
                        Battle.loses += 1
                        Battle.rewardLoses -= data[1]['reward']
                    Battle.winRate = (Battle.wins / (Battle.wins + Battle.loses)) * 100

                    await self.websocket.recv()
                    self.stop_event.set()
                    return

                try:
                    if ( self.strike['attack'] and not self.strike['defense'] ) or ( self.strike['defense'] and not self.strike['attack'] ):
                        await self.websocket.recv()
                        await self.websocket.recv()
                    if self.strike['attack'] and self.strike['defense']:
                        await self.websocket.recv()
                        await self.websocket.send("3")
                        await self.websocket.recv()
                        self.superHit = False
                except:
                    pass

    async def connect(self):
        uri = "wss://api-clicker.pixelverse.xyz/socket.io/?EIO=4&transport=websocket"
        async with websockets.connect(uri) as websocket:
            self.websocket = websocket
            data = await websocket.recv()
            content = {
                "initData": self.initData,
                "secret": self.secret,
                "tg-id": self.tgId
            }

            await websocket.send(f"40{json.dumps(content)}")
            await websocket.recv()

            data = await websocket.recv()
            data = json.loads(data[2:])
            self.battleId = data[1]['battleId']
            self.player1 = {
                "name": data[1]['player1']['username']
            }
            self.player2 = {
                "name": data[1]['player2']['username']
            }

            print(f"🤪 {Fore.RED+Style.BRIGHT}[ {data[1]['player1']['username']} ] "
                  f"{Fore.WHITE+Style.BRIGHT}| "
                  f"{Fore.BLUE+Style.BRIGHT}[ {split_chunk(str(int(data[1]['player1']['balance'])))} Coins ]"
                  f"{Fore.WHITE+Style.BRIGHT} | "
                  f"{Fore.GREEN+Style.BRIGHT}[ Level {data[1]['player1']['level']} ]"
                  f"{Fore.WHITE+Style.BRIGHT} | "
                  f"{Fore.CYAN+Style.BRIGHT}[ Energy {split_chunk(str(int(data[1]['player1']['energy'])))} ]"
                  f"{Fore.WHITE+Style.BRIGHT} | "
                  f"{Fore.MAGENTA+Style.BRIGHT}[ Damage {split_chunk(str(int(data[1]['player1']['damage'])))} ]")
            print(f"🤪 {Fore.RED+Style.BRIGHT}[ {data[1]['player2']['username']} ]"
                  f"{Fore.WHITE+Style.BRIGHT} | "
                  f"{Fore.BLUE+Style.BRIGHT}[ {split_chunk(str(int(data[1]['player2']['balance'])))} Coins ]"
                  f"{Fore.WHITE+Style.BRIGHT} | "
                  f"{Fore.GREEN+Style.BRIGHT}[ Level {data[1]['player2']['level']} ]"
                  f"{Fore.WHITE+Style.BRIGHT} | "
                  f"{Fore.CYAN+Style.BRIGHT}[ Energy {split_chunk(str(int(data[1]['player2']['energy'])))} ]"
                  f"{Fore.WHITE+Style.BRIGHT} | "
                  f"{Fore.MAGENTA+Style.BRIGHT}[ Damage {split_chunk(str(int(data[1]['player2']['damage'])))} ]")

            for i in range(5, 0, -1):
                print(f"\r⏰ {Fore.YELLOW+Style.BRIGHT}[ Pertarungan Dimulai Dalam {i} Detik ]", end="\r", flush=True)
                await asyncio.sleep(1)

            print('')

            listenerMsgTask = asyncio.create_task(self.listenerMsg())
            hitTask = asyncio.create_task(self.sendHit())

            await asyncio.gather(listenerMsgTask, hitTask)