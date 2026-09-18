from client.game_client import GameClient
from utils.env_variables import load_environment_variables

load_environment_variables()

client = GameClient()
games = client.get_games()

print(f"{len(games)} games loaded:")
for g in games:
    print(f"- {g}")