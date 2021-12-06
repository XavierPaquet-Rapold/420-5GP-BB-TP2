from abc import abstractmethod
from level import Level
from network import NetMessage


class Player:
    """Représente la base d'un personnage du jeu (ce qui est commun au ninja et aux samouraïs)."""
    __HP_MAX = 10

    def __init__(self, x: int, y: int, damages=0) -> None:
        self.position = (x, y)

        self.__facing_south = True
        self.__facing_north = self.__facing_east = self.__facing_west = False

        self.__is_active = False  # représente la présence d'un joueur

        self.__damages = damages
        self.__hp_current = self.__HP_MAX

    def __move(self, level: Level, delta_x, delta_y: int) -> bool:
        tile = level.get_tile(
            self.position[0] + delta_x, self.position[1] + delta_y)
        if tile.walkable:
            self.position = (self.position[0] +
                             delta_x, self.position[1] + delta_y)
            return True
        return False

    def face_east(self) -> None:
        self.__facing_east = True
        self.__facing_west = self.__facing_north = self.__facing_south = False

    def face_north(self) -> None:
        self.__facing_north = True
        self.__facing_south = self.__facing_east = self.__facing_west = False

    def face_south(self) -> None:
        self.__facing_south = True
        self.__facing_north = self.__facing_east = self.__facing_west = False

    def face_west(self) -> None:
        self.__facing_west = True
        self.__facing_east = self.__facing_north = self.__facing_south = False

    def move_east(self, level: Level) -> bool:
        """Déplace le personnage vers l'Est."""
        self.face_east()
        return self.__move(level, 1, 0)

    def move_north(self, level: Level) -> bool:
        """Déplace le personnage vers le Nord."""
        self.face_north()
        return self.__move(level, 0, -1)

    def move_south(self, level: Level) -> bool:
        """Déplace le personnage vers le Sud."""
        self.face_south()
        return self.__move(level, 0, 1)

    def move_west(self, level: Level) -> bool:
        """Déplace le personnage vers l'Ouest'."""
        self.face_west()
        return self.__move(level, -1, 0)

    def hit(self, damage: int) -> int:
        """Fais subir les dégats au personnage"""
        if self.__hp_current > 0:
            self.__hp_current -= damage
            return self.__hp_current
        else:
            return 0
    
    def get_facing(self) -> str:
        if self.__facing_east:
            return 'e'
        if self.__facing_north:
            return 'n'
        if self.__facing_south:
            return 's'
        if self.__facing_west:
            return 'w'

    @property
    def facing_east(self) -> bool:
        return self.__facing_east

    @property
    def facing_north(self) -> bool:
        return self.__facing_north

    @property
    def facing_south(self) -> bool:
        return self.__facing_south

    @property
    def facing_west(self) -> bool:
        return self.__facing_west

    @property
    def position(self) -> tuple:
        return self.__position

    @property
    def player_active(self) -> bool:
        return self.__is_active

    @property
    def hp_current(self) -> int:
        return self.__hp_current

    @property
    def hp_max(self) -> int:
        return self.__HP_MAX

    @property
    def damages(self) -> int:
        return self.__damages

    @position.setter
    def position(self, position: tuple) -> None:
        self.__position = position

    @player_active.setter
    def player_active(self, is_active: bool) -> None:
        self.__is_active = is_active
    
    @damages.setter
    def damages(self, damages: int) -> None:
        self.__damages = damages

class Ninja(Player):
    """Représente les spécificités du personnage ninja (éventuellement)."""

    __NINJA_DAMAGES = 1

    def __init__(self, x, y: int) -> None:
        super().__init__(x, y, self.__NINJA_DAMAGES)

class Samourai(Player):
    """Représente les spécificités des personnages samouraïs."""

    COLORS = [(91, 155, 213),  # samourai 1
              (112, 173, 71),  # samourai 2
              (255, 192, 0),  # samourai 3
              (255, 153, 51),  # samourai 4
              (255, 102, 153),  # samourai 5
              (153, 0, 255)]  # samourai 6

    __SAMOURAI_DAMAGES = 2

    __VIEWING_REGION_DELTAS = [
        [(0, -1), (0, -2), (-1, -3), (-1, -4)],
        [(0, -1), (0, -2), (0, -3), (0, -4)],
        [(0, -1), (0, -2), (1, -3), (1, -4)],
        [(0, -1), (1, -2), (1, -3)],
        [(1, -1), (1, -2), (2, -3)],
        [(1, -1), (2, -2), (3, -3)],
        [(1, -1), (2, -1), (3, -2)],
        [(1, 0), (2, -1), (3, -1)],
        [(1, 0), (2, 0), (3, -1), (4, -1)],
        [(1, 0), (2, 0), (3, 0), (4, 0)],
        [(1, 0), (2, 0), (3, 1), (4, 1)],
        [(1, 0), (2, 1), (3, 1)],
        [(1, 1), (2, 1), (3, 2)],
        [(1, 1), (2, 2), (3, 3)],
        [(1, 1), (1, 2), (2, 3)],
        [(0, 1), (1, 2), (1, 3)],
        [(0, 1), (0, 2), (1, 3), (1, 4)],
        [(0, 1), (0, 2), (0, 3), (0, 4)],
        [(0, 1), (0, 2), (-1, 3), (-1, 4)],
        [(0, 1), (-1, 2), (-1, 3)],
        [(-1, 1), (-1, 2), (-2, 3)],
        [(-1, 1), (-2, 2), (-3, 3)],
        [(-1, 1), (-2, 1), (-3, 2)],
        [(-1, 0), (-2, 1), (-3, 1)],
        [(-1, 0), (-2, 0), (-3, 1), (-4, 1)],
        [(-1, 0), (-2, 0), (-3, 0), (-4, 0)],
        [(-1, 0), (-2, 0), (-3, -1), (-4, -1)],
        [(-1, 0), (-2, -1), (-3, -1)],
        [(-1, -1), (-2, -1), (-3, -2)],
        [(-1, -1), (-2, -2), (-3, -3)],
        [(-1, -1), (-1, -2), (-2, -3)],
        [(0, -1), (-1, -2), (-1, -3)],
    ]

    def __init__(self, x, y: int) -> None:
        super().__init__(x, y, self.__SAMOURAI_DAMAGES)
        self.last_drawn_postition = None
        self.tiles = []

    def get_viewing_region(self, width: int, height: int) -> list:
        """Retourne le champ de vision du samouraï."""

        if not (self.position == self.last_drawn_postition) or not self.last_drawn_postition:
            self.last_drawn_postition = self.position
            self.tiles.clear()
            for path in self.__VIEWING_REGION_DELTAS:
                correct_path = []
                for delta in path:
                    x = self.position[0] + delta[0]
                    y = self.position[1] + delta[1]

                    if (0 <= x < width) and (0 <= y < height):
                        correct_path.append((x, y))
                    else:
                        break

                self.tiles.append(correct_path)

        return self.tiles
