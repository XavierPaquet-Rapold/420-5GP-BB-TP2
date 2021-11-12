import arcade

from game import Game
from game import GameState
from game_client import GameClient
from players import Samourai
from tile import Tile
from tile import TileType


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = 'Ninja vs Samouraïs'

MOVING_PACE = 5 / 60


class NinjaVSSamourais(arcade.Window):
    """Fenêtre principale de l'application arcade."""
    def __init__(self, game: Game, game_client: GameClient,
                 width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT, title: str = SCREEN_TITLE):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.__game = game
        self.__game_client = game_client

        self.__tile_shapes = []
        self.__tiles = arcade.ShapeElementList()

        self.__time_since_last_move = 0.0
        self.__moving_east = self.__moving_west = self.__moving_north = self.__moving_south = False

    def __build_gui_from_game_level(self) -> None:
        """Construit la grille visuelle représentant le niveau courant."""
        for y in range(self.__game.level.height):
            for x in range(self.__game.level.width):
                tile = self.__game.level.get_tile(x, y)

                color = Tile.TYPES_AND_COLORS.get(tile.tile_type)
                if not color:
                    color = Tile.TYPES_AND_COLORS.get(TileType.GROUND)

                shape = arcade.create_rectangle_filled(5 + x * 10, SCREEN_HEIGHT - (5 + y * 10), 8, 8, color)
                self.__tile_shapes.append(shape)
                self.__tiles.append(shape)

    @staticmethod
    def __draw_ninja(game: Game) -> None:
        """Dessine le ninja."""
        ninja = game.get_ninja()
        arcade.draw_rectangle_filled(5 + ninja.position[0] * 10,
                                     SCREEN_HEIGHT - (5 + ninja.position[1] * 10), 8, 8, (0, 0, 0))

        if ninja.facing_north:
            pass
        elif ninja.facing_south:
            arcade.draw_rectangle_filled(5 + ninja.position[0] * 10,
                                         SCREEN_HEIGHT - (3 + ninja.position[1] * 10), 8, 1, (255, 192, 0))
        elif ninja.facing_east:
            arcade.draw_rectangle_filled(7 + ninja.position[0] * 10,
                                         SCREEN_HEIGHT - (3 + ninja.position[1] * 10), 6, 1, (255, 192, 0))
        else:
            arcade.draw_rectangle_filled(3 + ninja.position[0] * 10,
                                         SCREEN_HEIGHT - (3 + ninja.position[1] * 10), 6, 1, (255, 192, 0))

    @staticmethod
    def __draw_samourais(game: Game) -> None:
        """Dessine les samouraïs."""
        for i in range(1, 7):
            samourai = game.get_player(i)
            arcade.draw_rectangle_filled(5 + samourai.position[0] * 10,
                                         SCREEN_HEIGHT - (5 + samourai.position[1] * 10), 8, 8,
                                         Samourai.COLORS[i - 1])
            if samourai.facing_north:
                pass
            elif samourai.facing_south:
                arcade.draw_rectangle_filled(5 + samourai.position[0] * 10,
                                             SCREEN_HEIGHT - (3 + samourai.position[1] * 10), 8, 1, (0, 0, 0))
                arcade.draw_rectangle_filled(5 + samourai.position[0] * 10,
                                             SCREEN_HEIGHT - (4 + samourai.position[1] * 10), 2, 2, (0, 0, 0))
            elif samourai.facing_east:
                arcade.draw_rectangle_filled(7 + samourai.position[0] * 10,
                                             SCREEN_HEIGHT - (3 + samourai.position[1] * 10), 6, 1, (0, 0, 0))
                arcade.draw_rectangle_filled(8 + samourai.position[0] * 10,
                                             SCREEN_HEIGHT - (4 + samourai.position[1] * 10), 2, 2, (0, 0, 0))
            else:
                arcade.draw_rectangle_filled(3 + samourai.position[0] * 10,
                                             SCREEN_HEIGHT - (3 + samourai.position[1] * 10), 6, 1, (0, 0, 0))
                arcade.draw_rectangle_filled(2 + samourai.position[0] * 10,
                                             SCREEN_HEIGHT - (4 + samourai.position[1] * 10), 2, 2, (0, 0, 0))

    @staticmethod
    def __draw_viewing_region(game: Game) -> bool:
        """Dessine le champ de vision du joueur (si samouraï). Retourne True si le ninja s'y trouve."""
        ninja = game.get_ninja()
        ninja_in_viewing_region = False

        # Récupérer le champ de vision du samouraï
        samurai = game.get_current_player()
        viewing_region = samurai.get_viewing_region(50, 50)

        # Afficher les tuiles du champ de vision
        for pos in viewing_region:
            if ninja.position[0] == pos[0] and ninja.position[1] == pos[1]:
                ninja_in_viewing_region = True

            tile = game.level.get_tile(pos[0], pos[1])

            color = Tile.TYPES_AND_COLORS.get(tile.tile_type)
            if not color:
                color = Tile.TYPES_AND_COLORS.get(TileType.GROUND)

            arcade.draw_rectangle_filled(5 + pos[0] * 10,
                                         SCREEN_HEIGHT - (5 + pos[1] * 10), 8, 8, color)

        return ninja_in_viewing_region

    def on_draw(self) -> None:
        """Dessine l'écran sur une base régulière."""
        arcade.start_render()

        if self.__game.state == GameState.PLAYING_LEVEL:
            ninja_in_viewing_region = False

            if self.__game.i_am_the_ninja():
                self.__tiles.draw()    # le ninja voit tout le niveau
            else:
                ninja_in_viewing_region = self.__draw_viewing_region(self.__game)

            if self.__game.i_am_the_ninja() or ninja_in_viewing_region:
                self.__draw_ninja(self.__game)

            self.__draw_samourais(self.__game)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.__moving_north = True
        if symbol == arcade.key.DOWN:
            self.__moving_south = True
        if symbol == arcade.key.LEFT:
            self.__moving_west = True
        if symbol == arcade.key.RIGHT:
            self.__moving_east = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.__moving_north = False
        if symbol == arcade.key.DOWN:
            self.__moving_south = False
        if symbol == arcade.key.LEFT:
            self.__moving_west = False
        if symbol == arcade.key.RIGHT:
            self.__moving_east = False

    def on_update(self, delta_time: float):
        self.__game_client.handle_messages(self.__game)

        if self.__game.state == GameState.STARTED:
            self.__game.player_id = self.__game_client.who_am_i()
            self.__game.state = GameState.WAITING_LEVEL
            self.__game_client.send_level_query()
        elif self.__game.state == GameState.LEVEL_RECEIVED:
            self.__build_gui_from_game_level()
            self.__game.state = GameState.PLAYING_LEVEL
        elif self.__game.state == GameState.PLAYING_LEVEL:
            self.__time_since_last_move += delta_time

            if self.__time_since_last_move >= MOVING_PACE:
                self.__time_since_last_move = 0.0
                dispatch_position = False
                player_index = self.__game_client.who_am_i()
                myself = self.__game.get_player(player_index)
                if self.__moving_north:
                    dispatch_position = myself.move_north(self.__game.level)
                if self.__moving_south:
                    dispatch_position = myself.move_south(self.__game.level)
                if self.__moving_west:
                    dispatch_position = myself.move_west(self.__game.level)
                if self.__moving_east:
                    dispatch_position = myself.move_east(self.__game.level)

                if dispatch_position:
                    self.__game_client.send_position(myself.position)
