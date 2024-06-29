import asyncio
import os
import sys
from Battle import Battle
from Pixel import Pixel
from colorama import Fore, Style, init

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

async def main():
    init()
    battle = Battle()
    user = Pixel()
    users = user.getUsers()

    print(f"👻 {Fore.CYAN+Style.BRIGHT}[ {users.get('username', 'Unknown')} ]")
    print(f"💰 {Fore.YELLOW+Style.BRIGHT}[ {split_chunk(str(int(users['clicksCount'])))} Coins ]")
    print(f"🍏 {Fore.GREEN+Style.BRIGHT}[ {split_chunk(str(int(battle.wins)))} Wins ]"
          f"{Fore.WHITE+Style.BRIGHT} | "
          f"🍎 {Fore.RED+Style.BRIGHT}[ {split_chunk(str(int(battle.loses)))} Loses ]"
          f"{Fore.WHITE+Style.BRIGHT} | "
          f"⚽️ {Fore.YELLOW+Style.BRIGHT}[ Winrate ] {battle.winRate:.2f}%")
    print(f"🍏 {Fore.GREEN+Style.BRIGHT}[ {split_chunk(str(int(battle.rewardWins)))} Wins Reward ]"
          f"{Fore.WHITE+Style.BRIGHT} | "
          f"🍎 {Fore.RED+Style.BRIGHT}[ {split_chunk(str(int(battle.rewardLoses)))} Loses Reward ]"
          f"{Fore.WHITE+Style.BRIGHT} | "
          f"💰 {Fore.YELLOW+Style.BRIGHT}[ {split_chunk(str(int(battle.rewardWins + battle.rewardLoses)))} Total Earned ]")

    await battle.connect()
    del battle

if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error ]\t\t: {type(e).__name__} {e}")
        clear()