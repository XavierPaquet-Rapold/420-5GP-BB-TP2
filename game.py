from enum import Enum
from enum import auto

from level import Level
from players import Ninja, Player
from players import Samourai
from tile import TileType


class GameState(Enum):
    STARTING = auto(),
    STARTED = auto(),
    WAITING_LEVEL = auto(),
    LEVEL_RECEIVED = auto(),
    WAITING_PLAYERS_LIST = auto(),
    PLAYERS_LIST_RECEIVED = auto(),
    PLAYING_LEVEL = auto()


class Game:
    """Données relatives à la partie en cours."""

    def __init__(self) -> None:
        self.__level_number = 0
        self.__number_of_samourais = 6
        self.__level = None

        self.player_id = -1
        self.__player_is_ninja = False
        self.__players = []

        self.state = GameState.STARTING

    def __create_ninja_and_samourais(self):
        """Instancie le ninja et les samouraïs."""
        player_positions = self.level.get_starting_positions()
        self.__players.append(Ninja(player_positions[0]['x'], player_positions[0]['y']))
        for i in range(self.__number_of_samourais):
            self.__players.append(Samourai(player_positions[i + 1]['x'], player_positions[i + 1]['y']))

    def i_am_the_ninja(self) -> bool:
        return self.__player_is_ninja

    def declare_ninja(self) -> None:
        self.__player_is_ninja = True

    def get_current_player(self) -> Player:
        return self.__players[self.player_id]

    def get_ninja(self) -> Ninja:
        return self.__players[0]

    def get_player(self, player_id: int):
        return self.__players[player_id]

    def get_all_players(self) -> list:
        return self.__players

    def next_level(self) -> bool:
        self.__level_number += 1
        self.__level = Level()
        load_success = self.level.load(self.__level_number)
        if not load_success:
            return load_success
        self.__create_ninja_and_samourais()
        return load_success

    def set_level(self, level) -> None:
        self.__level = level
        self.__create_ninja_and_samourais()

    def update_players_list(self, current_players: str) -> None:
        """Modifie la liste de joueur a partir d'une liste d'id separee par des virgules"""
        if current_players:
            current_players = list(current_players.split(","))
            for id in current_players:
                player = self.__players[int(id)]
                player.player_active = True

    def update_player_position(self, player_id: int, position: tuple) -> None:
        player = self.__players[player_id]
        player.position = position

    def update_is_active(self, player_id: int, is_active: bool) -> None:
        player = self.__players[player_id]
        player.player_active = is_active

    def check_for_ennemy(self, position: list) -> int:
        """verifier si un samourai se trouve sur une case en avant du ninja, sinon, verifie la prochaine case"""
        for samourai in self.__players:
            if tuple(position) == samourai.position and samourai.player_active:
                id_samourai = self.get_all_players().index(samourai)
                return id_samourai

    def check_for_wall(self, position: list) -> bool:
        """verifier si un mur se trouve sur une case en avant du ninja, sinon, verifie la prochaine case"""
        tile = self.level.get_tile(position[0], position[1])
        return tile.tile_type == TileType.WALL

    def update_player_facing(self, player_id: int, facing: str) -> None:
        """Met a jour la direction du joueur"""
        player = self.__players[player_id]
        if facing == 'n':
            player.face_north()
        elif facing == 's':
            player.face_south()
        elif facing == 'e':
            player.face_east()
        elif facing == 'w':
            player.face_west()

    @property
    def level(self) -> Level or None:
        return self.__level

    @property
    def player_id(self) -> int:
        return self.__player_id

    @property
    def state(self) -> GameState:
        return self.__state

    @player_id.setter
    def player_id(self, player_id) -> None:
        self.__player_id = player_id

    @state.setter
    def state(self, state) -> None:
        self.__state = state
