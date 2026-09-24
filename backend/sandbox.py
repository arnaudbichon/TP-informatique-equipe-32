from client.game_client import GameClient

client = GameClient()
games = client.get_games()
print(f"{len(games)} games loaded:")
for g in games:
    print(f"- {g}")