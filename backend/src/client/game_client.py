import json
from datetime import datetime

import requests

from business_object.game import Game
from business_object.player import Player


class GameClient():
    def get_games(self) -> list[Game]:
        r = requests.get(url="http://127.0.0.1:5555")
        if r.status_code != 200:
            raise Exception(f"Cannot reach (HTTP {r.status_code}): {r.text}")
        else:
            raw_json = r.json()
            print(json.dumps(raw_json, indent=2))  # Pretty print
        games = []

        for elt in raw_json:
            # Create an object
            g = Game(
                player1=Player(username=elt["players_list"][0],email=f"{elt["players_list"][0]}@xx.com", elo=0),
                player2=Player(username=elt["players_list"][1],email=f"{elt["players_list"][1]}@xx.com", elo=0),
                game_mode=elt["mode_type"],
                winner=Player(username=elt["winner_name"],email=f"{elt["winner_name"]}@xx.com", elo=0),
                description=elt["details"],
                timestamp=datetime.now(),
                id_game=elt["id"]
            )

            # If it succeed, add to the list
            if g:
                games.append(g)
        return games
