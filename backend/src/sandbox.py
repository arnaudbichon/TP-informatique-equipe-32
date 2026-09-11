from dao.game_dao import GameDao
from utils.env_variables import load_environment_variables

load_environment_variables()

games = GameDao().find_all_by_player(4)

for game in games:
    print(game)