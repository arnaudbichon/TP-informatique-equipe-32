from business_object.game import Game
from dao.db_connection import DBConnection
from dao.player_dao import PlayerDao
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class GameDao(metaclass=Singleton):
    """Class containing methods to access Games in the database."""

    @log
    def create(self, game: Game) -> bool:
        """Create a game in the database.

        Args:
            game: Game to create

        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO game("
                        "id_player1, id_player2, game_mode, id_winner, detail, timestamp"
                        ") VALUES ("
                        "%(id_player1)s, %(id_player2)s, %(game_mode)s, "
                        "%(id_winner)s, %(detail)s, %(timestamp)s"
                        ") RETURNING id_game;",
                        {
                            "id_player1": game.player1.id_player,
                            "id_player2": game.player2.id_player,
                            "game_mode": game.game_mode,
                            "id_winner": (
                                game.winner.id_player
                                if game.winner
                                else None
                            ),
                            "detail": game.description,
                            "timestamp": game.timestamp,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False

        if res:
            game.id_game = res["id_game"]
            created = True

        return created

    @log
    def find_by_id(self, id_game: int) -> Game:
        """Find a game by its ID.

        Args:
            id_game: ID of the game to find

        Returns:
            Game matching the given ID, or None.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * "
                        "FROM game "
                        "WHERE id_game = %(id_game)s;",
                        {"id_game": id_game},
                    )
                    row = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        if row:
            player1 = PlayerDao().find_by_id(row["id_player1"])
            player2 = PlayerDao().find_by_id(row["id_player2"])
            winner = (
                PlayerDao().find_by_id(row["id_winner"])
                if row["id_winner"] is not None
                else None
            )

            return Game(
                id_game=row["id_game"],
                player1=player1,
                player2=player2,
                game_mode=row["game_mode"],
                winner=winner,
                description=row["detail"],
                timestamp=row["timestamp"],
            )

        return None

    @log
    def find_all_by_player(self, id_player: int) -> list[Game]:
        """Find all games involving a specific player.

        Args:
            id_player: ID of the player

        Returns:
            List of games involving the player
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * "
                        "FROM game "
                        "WHERE id_player1 = %(id_player)s "
                        "   OR id_player2 = %(id_player)s "
                        "ORDER BY timestamp;",
                        {"id_player": id_player},
                    )
                    rows = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        games = []

        if rows:
            for row in rows:
                player1 = PlayerDao().find_by_id(row["id_player1"])
                player2 = PlayerDao().find_by_id(row["id_player2"])

                winner = None
                if row["id_winner"] is not None:
                    winner = PlayerDao().find_by_id(row["id_winner"])

                game = Game(
                    id_game=row["id_game"],
                    player1=player1,
                    player2=player2,
                    game_mode=row["game_mode"],
                    winner=winner,
                    description=row["detail"],
                    timestamp=row["timestamp"],
                )

                games.append(game)

        return games