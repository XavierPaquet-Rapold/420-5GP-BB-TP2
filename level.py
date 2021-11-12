from network import NetMessage
from tile import Tile
from tile import TileType


class Level:
    """Niveau (grille) de jeu."""
    def __init__(self) -> None:
        self.__number = 0
        self.__tiles = []    # [[rangée],[rangée],[rangée],...]

        self.__width = self.__height = 0

    def __str__(self) -> str:
        level_string = str(self.__number).zfill(NetMessage.DATA_LVL_NUMBER_BYTES) + \
                       str(self.__width).zfill(NetMessage.DATA_LVL_WIDTH_BYTES)

        for row in self.__tiles:
            for tile in row:
                level_string += str(tile)

        return level_string

    def get_starting_positions(self) -> list:
        """Retourne les positions de départ de tous les joueurs (ninja et samouraïs)."""
        positions = [{'x': 0, 'y': 0} for _ in range(7)]
        index = 0
        for y, row in enumerate(self.__tiles):
            for x, tile in enumerate(row):

                starting_position = True
                if tile.tile_type == TileType.NINJA_START_POS:
                    index = 0
                elif tile.tile_type == TileType.SAMOURAI_START_POS_1:
                    index = 1
                elif tile.tile_type == TileType.SAMOURAI_START_POS_2:
                    index = 2
                elif tile.tile_type == TileType.SAMOURAI_START_POS_3:
                    index = 3
                elif tile.tile_type == TileType.SAMOURAI_START_POS_4:
                    index = 4
                elif tile.tile_type == TileType.SAMOURAI_START_POS_5:
                    index = 5
                elif tile.tile_type == TileType.SAMOURAI_START_POS_6:
                    index = 6
                else:
                    starting_position = False

                if starting_position:
                    positions[index]['x'] = x
                    positions[index]['y'] = y

        return positions

    def get_tile(self, x, y: int) -> Tile:
        return self.__tiles[y][x]

    def load(self, number: int) -> None:
        """Charge un niveau à partir d'un fichier texte."""

        self.__number = number
        filename = "levels/level" + str(self.__number) + ".txt"

        try:
            with open(filename, "r") as level_file:
                for line in level_file:
                    symbols = line.strip()
                    columns = []
                    for symbol in symbols:
                        tile = Tile.create_from_symbol(symbol)
                        columns.append(tile)
                    self.__tiles.append(columns)
        except FileNotFoundError:
            print("Fichier introuvable : " + filename)

        self.__width = len(self.__tiles[0])
        self.__height = len(self.__tiles)

    def setup_from_data(self, number, width, height: int, data: str) -> None:
        """Configure un niveau à partir d'une chaîne de caractères (data) descriptive."""
        self.__number = number
        self.__width = width
        self.__height = height

        while len(data):
            symbols = data[:width]
            columns = []
            for symbol in symbols:
                tile = Tile.create_from_symbol(symbol)
                columns.append(tile)
            self.__tiles.append(columns)
            data = data[width:]

    @property
    def height(self) -> int:
        return self.__height

    @property
    def number(self) -> int:
        return self.__number

    @property
    def width(self) -> int:
        return self.__width
