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

    def load(self, number: int) -> bool:
        """Charge un niveau à partir d'un fichier texte."""

        self.__number = number
        filename = "levels/level" + str(self.__number) + ".txt"

        try:
            with open(filename, "r") as level_file:
                level_str = level_file.read()
                valid_characters = self.__validate_level_characters(level_str)
                if valid_characters:
                    level_lines = level_str.splitlines()
                    line_length = len(level_lines[0])
                    for line in level_lines:
                        if line_length != len(line):
                            print("The lines in the level file are not the same length")
                            return False
                        line_length = len(line)
                        symbols = line.strip()
                        columns = []
                        for symbol in symbols:
                            tile = Tile.create_from_symbol(symbol)
                            columns.append(tile)
                        self.__tiles.append(columns)
                else:
                    print("The level contains invalid characters")
                    return False
        except FileNotFoundError:
            print("File not found : " + filename)
            return False

        self.__width = len(self.__tiles[0])
        self.__height = len(self.__tiles)
        return True
    
    def __validate_level_characters(self, level_file: str) -> bool:
        """Valider que seulement les caracteres permis sont dans le fichier de niveau"""
        types_and_symbols = Tile.TYPES_AND_SYMBOLS
        allowed = set(types_and_symbols.keys())
        allowed.add('\n')
        return set(level_file) <= allowed

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
