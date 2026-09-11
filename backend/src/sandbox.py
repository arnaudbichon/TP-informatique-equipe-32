# uv run --project backend python backend/src/sandbox.py
from datetime import datetime
from business_object.game import Game
from business_object.player import Player
from dao.game_dao import GameDao
from utils.env_variables import load_environment_variables

load_environment_variables()   # Required to load the variables needed (env) to connect to the database 

p1 = Player(username='batricia', elo=1500, email='bat@project.io', password='zut', id_player=4)
p2 = Player(username='gilbert', elo=1100, email='gilbert@project.io', password='zut', id_player=6)
game = Game(player1=p1, player2=p2, game_mode='Dice', winner=p1, description="batricia contre gilbert", timestamp=datetime.now())

id = GameDao().create(game)
print(id)
game2 = GameDao().find_by_id(5)