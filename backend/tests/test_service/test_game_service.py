from unittest.mock import MagicMock

from business_object.game import Game
from dao.game_dao import GameDao
from service.game_service import GameService


game_list = [
    MagicMock(spec=Game, game_mode="dice"),
    MagicMock(spec=Game, game_mode="coinflip"),
    MagicMock(spec=Game, game_mode="dice"),
]


def test_find_all_by_player():
    """List all games of a player"""

    # GIVEN
    GameDao().find_all_by_player = MagicMock(return_value=game_list)

    # WHEN
    res = GameService().find_all_by_player(4)

    # THEN
    assert len(res) == 3


def test_find_all_by_player_with_game_mode():
    """List games of a player with a specific game mode"""

    # GIVEN
    GameDao().find_all_by_player = MagicMock(return_value=game_list)

    # WHEN
    res = GameService().find_all_by_player(4, "dice")

    # THEN
    assert len(res) == 2
    assert all(game.game_mode == "dice" for game in res)