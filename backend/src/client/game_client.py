import json
from datetime import datetime

import requests

from business_object.game import Game, Player


class GameClient:
    def get_games(self) -> list[Game]:
        r = requests.get(url="http://localhost:5555/")
        if r.status_code != 200:
            raise Exception(f"Cannot reach (HTTP {r.status_code}): {r.text}")
        else:
            raw_json = r.json()
            print(json.dumps(raw_json, indent=2))  # Pretty print

        games = []

        for ligne in raw_json:
            player1 = Player(ligne["players_list"][0], 1300, "toto@liberte.fr")

            player2 = Player(ligne["players_list"][1], 1301, "tato@liberte.fr")

            if ligne["winner_name"] == ligne["players_list"][0]:
                winner = player1
            else:
                winner = player2

            # Create an object
            game = Game(
                player1=player1,
                player2=player2,
                game_mode=ligne["mode_type"],
                winner=winner,
                description=ligne["details"],
                timestamp=datetime.now(),
                id_game=ligne["id"],
            )

            # If it succeed, add to the list
            if game:
                games.append(game)
        return games
