import arcade

from game import Game
from game import GameState
from game_client import GameClient
from players import Ninja, Samourai
from tile import Tile
from tile import TileType

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 520
HEALTH_BAR_POSITION_X = 70
HEALTH_BAR_POSITION_Y = 10
HEALTH_BAR_HEIGHT = 10
HEALTH_BAR_MULTIPLICATOR = 10
HUD_WIDTH = 1000
HUD_HEIGHT = 40

SCREEN_TITLE = 'Ninja vs Samouraïs'

MOVING_PACE = 5 / 60
BLOCK_UNIT = 10
SAMURAI_VIEW_RANGE_X = SAMURAI_VIEW_RANGE_Y = 50


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
        LEVEL = self.__game.level
        for y in range(LEVEL.height):
            for x in range(LEVEL.width):
                tile = LEVEL.get_tile(x, y)
                TYPES_AND_COLORS = Tile.TYPES_AND_COLORS
                color = TYPES_AND_COLORS.get(tile.tile_type)
                if not color:
                    color = TYPES_AND_COLORS.get(TileType.GROUND)

                shape = arcade.create_rectangle_filled(
                    5 + x * BLOCK_UNIT, SCREEN_HEIGHT - (5 + y * BLOCK_UNIT), 8, 8, color)
                self.__tile_shapes.append(shape)
                self.__tiles.append(shape)

    @staticmethod
    def __draw_ninja(game: Game) -> None:
        """Dessine le ninja."""
        ninja = game.get_ninja()
        drawing_settings = {
            "offset_x": 5,
            "offset_y": 5,
            "body_width": 8,
            "body_height": 8,
            "body_color": (0, 0, 0),
            "bandanna_center_x": 0,
            "bandanna_center_y": 3,
            "bandanna_width": 0,
            "bandanna_height": 1,
            "bandanna_color": (255, 192, 0)
        }

        arcade.draw_rectangle_filled(drawing_settings["offset_x"] + ninja.position[0] * BLOCK_UNIT,
                                     SCREEN_HEIGHT -
                                     (drawing_settings["offset_y"] +
                                      ninja.position[1] * BLOCK_UNIT),
                                     drawing_settings["body_width"], drawing_settings["body_height"],
                                     drawing_settings["body_color"])

        if ninja.facing_south:
            drawing_settings.update({
                "bandanna_center_x": 5,
                "bandanna_width": 8
            })
        elif ninja.facing_east:
            drawing_settings.update({
                "bandanna_center_x": 7,
                "bandanna_width": 6
            })
        else:
            drawing_settings.update({
                "bandanna_center_x": 3,
                "bandanna_width": 6
            })

        if not ninja.facing_north:
            arcade.draw_rectangle_filled(drawing_settings["bandanna_center_x"] + ninja.position[0] * BLOCK_UNIT,
                                         SCREEN_HEIGHT -
                                         (drawing_settings["bandanna_center_y"] +
                                          ninja.position[1] * BLOCK_UNIT),
                                         drawing_settings["bandanna_width"], drawing_settings["bandanna_height"],
                                         drawing_settings["bandanna_color"])

    @staticmethod
    def __draw_samourais(game: Game) -> None:
        """Dessine les samouraïs."""
        list_of_players = game.get_all_players()
        for player in list_of_players:  
            if type(player) != Ninja and player.player_active:  # si le joueur n'est pas un ninja et il est actif
                index = list_of_players.index(player)
                drawing_settings = {
                    "offset_x": 5,
                    "offset_y": 5,
                    "body_width": 8,
                    "body_height": 8,
                    "body_color": Samourai.COLORS[index - 1],
                    "bandanna_1_center_x": 0,
                    "bandanna_1_center_y": 3,
                    "bandanna_1_width": 0,
                    "bandanna_1_height": 1,
                    "bandanna_2_center_x": 0,
                    "bandanna_2_center_y": 4,
                    "bandanna_2_width": 2,
                    "bandanna_2_height": 2,
                    "bandanna_color": (0, 0, 0)
                }
                arcade.draw_rectangle_filled(drawing_settings["offset_x"] + player.position[0] * BLOCK_UNIT,
                                             SCREEN_HEIGHT -
                                             (drawing_settings["offset_y"] +
                                             player.position[1] * BLOCK_UNIT),
                                             drawing_settings["body_width"], drawing_settings["body_height"], drawing_settings["body_color"])

                if player.facing_south:
                    drawing_settings.update({
                        "bandanna_1_center_x": 5,
                        "bandanna_1_width": 8,
                        "bandanna_2_center_x": 5
                    })
                elif player.facing_east:
                    drawing_settings.update({
                        "bandanna_1_center_x": 7,
                        "bandanna_1_width": 6,
                        "bandanna_2_center_x": 8
                    })
                else:
                    drawing_settings.update({
                        "bandanna_1_center_x": 3,
                        "bandanna_1_width": 6,
                        "bandanna_2_center_x": 2
                    })

                if not player.facing_north:
                    arcade.draw_rectangle_filled(drawing_settings["bandanna_1_center_x"] + player.position[0] * BLOCK_UNIT,
                                                 SCREEN_HEIGHT -
                                                 (drawing_settings["bandanna_1_center_y"] +
                                                 player.position[1] * BLOCK_UNIT),
                                                 drawing_settings["bandanna_1_width"], drawing_settings["bandanna_1_height"], drawing_settings["bandanna_color"])

                    arcade.draw_rectangle_filled(drawing_settings["bandanna_2_center_x"] + player.position[0] * BLOCK_UNIT,
                                                 SCREEN_HEIGHT -
                                                 (drawing_settings["bandanna_2_center_y"] +
                                                 player.position[1] * BLOCK_UNIT),
                                                 drawing_settings["bandanna_2_width"], drawing_settings["bandanna_2_height"], drawing_settings["bandanna_color"])

    @staticmethod
    def __draw_viewing_region(game: Game) -> bool:
        """Dessine le champ de vision du joueur (si samouraï). Retourne True si le ninja s'y trouve."""
        ninja = game.get_ninja()
        ninja_in_viewing_region = False

        # Récupérer le champ de vision du samouraï
        samurai = game.get_current_player()
        viewing_region = samurai.get_viewing_region(
            SAMURAI_VIEW_RANGE_X, SAMURAI_VIEW_RANGE_Y)

        # Afficher les tuiles du champ de vision
        for path in viewing_region:
            for pos in path:
                if ninja.position[0] == pos[0] and ninja.position[1] == pos[1]:
                    ninja_in_viewing_region = True

                tile = game.level.get_tile(pos[0], pos[1])
                color = Tile.TYPES_AND_COLORS.get(tile.tile_type)

                if not color:
                    color = Tile.TYPES_AND_COLORS.get(TileType.GROUND)

                arcade.draw_rectangle_filled(5 + pos[0] * BLOCK_UNIT,
                                             SCREEN_HEIGHT - (5 + pos[1] * BLOCK_UNIT), 8, 8, color)

                if color == Tile.TYPES_AND_COLORS.get(TileType.WALL):
                    break

        return ninja_in_viewing_region

    @staticmethod
    def __health_bar(game: Game) -> None:
        player = game.get_current_player()
        hp_max = player.hp_max
        hp_current = player.hp_current
        arcade.draw_rectangle_filled(
            0, 0, HUD_WIDTH, HUD_HEIGHT, arcade.color.JAPANESE_VIOLET)

        arcade.draw_rectangle_outline(HEALTH_BAR_POSITION_X, HEALTH_BAR_POSITION_Y, hp_max * HEALTH_BAR_MULTIPLICATOR,
                                      HEALTH_BAR_HEIGHT, arcade.color.RED)
        arcade.draw_rectangle_filled(HEALTH_BAR_POSITION_X, HEALTH_BAR_POSITION_Y, hp_current * HEALTH_BAR_MULTIPLICATOR,
                                     HEALTH_BAR_HEIGHT, arcade.color.RED)

    def on_draw(self) -> None:
        """Dessine l'écran sur une base régulière."""
        arcade.start_render()
        if self.__game.state == GameState.PLAYING_LEVEL:
            ninja_in_viewing_region = False

            if self.__game.i_am_the_ninja():
                self.__tiles.draw()  # le ninja voit tout le niveau
                self.__health_bar(self.__game)
            else:
                ninja_in_viewing_region = self.__draw_viewing_region(
                    self.__game)
                self.__health_bar(self.__game)

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
            self.__game.state = GameState.WAITING_PLAYERS_LIST
            self.__game_client.send_players_list_query()
        elif self.__game.state == GameState.PLAYERS_LIST_RECEIVED:
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
