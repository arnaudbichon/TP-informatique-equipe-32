import requests
from datetime import datetime

from business_object.game import Game
from business_object.player import Player
from dao.player_dao import PlayerDao


class GameClient:
    """Client for retrieving games from an external API."""

    def __init__(self):
        self.url = "http://localhost:5555/"

    def get_games(self) -> list[Game]:
        """Retrieve games from the external API and convert them to Game objects."""

        r = requests.get(self.url)
        r.raise_for_status()

        data = r.json()

        games = []

        for game_data in data:
            players = game_data["players_list"]

            player1 = self._find_player(players[0])
            player2 = self._find_player(players[1])

            winner = None
            if game_data["winner_name"]:
                winner = self._find_player(game_data["winner_name"])

            if player1 is None or player2 is None:
                continue

            game = Game(
                player1=player1,
                player2=player2,
                game_mode=game_data["mode_type"],
                winner=winner,
                description=(
                    f"Game at {game_data['location_name']} - "
                    f"{game_data['duration_seconds']} seconds"
                ),
                timestamp=datetime.now(),
                id_game=int(game_data["id"]),
            )

            games.append(game)

        return games

    def _find_player(self, username: str) -> Player | None:
        """Find a player by username."""

        players = PlayerDao().find_all()

        for player in players:
            if player.username.lower() == username.lower():
                return player

        return None