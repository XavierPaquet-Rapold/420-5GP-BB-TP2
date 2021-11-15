from enum import Enum
from enum import auto


class TileType(Enum):
    GROUND = auto(),
    STONE = auto(),
    WALL = auto(),
    NINJA_START_POS = auto(),
    SAMOURAI_START_POS_1 = auto(),
    SAMOURAI_START_POS_2 = auto(),
    SAMOURAI_START_POS_3 = auto(),
    SAMOURAI_START_POS_4 = auto(),
    SAMOURAI_START_POS_5 = auto(),
    SAMOURAI_START_POS_6 = auto(),
    EXIT = auto()


class Tile:

    TYPES_AND_COLORS = {TileType.GROUND: (64, 64, 64),
                        TileType.STONE: (96, 96, 96),
                        TileType.WALL: (84, 62, 0),
                        TileType.EXIT: (64, 64, 64)}

    TYPES_AND_SYMBOLS = {' ': [TileType.GROUND, True],
                         'S': [TileType.STONE, False],
                         'W': [TileType.WALL, False],
                         'N': [TileType.NINJA_START_POS, True],
                         '1': [TileType.SAMOURAI_START_POS_1, True],
                         '2': [TileType.SAMOURAI_START_POS_2,True],
                         '3': [TileType.SAMOURAI_START_POS_3,True], 
                         '4': [TileType.SAMOURAI_START_POS_4,True], 
                         '5': [TileType.SAMOURAI_START_POS_5,True],
                         '6': [TileType.SAMOURAI_START_POS_6,True],
                         'E': [TileType.EXIT,True]}


    def __init__(self, walkable: bool = True, tile_type: TileType = TileType.GROUND) -> None:
        self.__walkable = walkable
        self.__tile_type = tile_type

    def __str__(self) -> str:
        #return self.TYPES_AND_SYMBOLS[self.__tile_type] à enlever
        value_type = self.__tile_type
        value = self.__tile_type
        key_value = [key for key, value_type in self.TYPES_AND_SYMBOLS.items()
                        if value in value_type]
        return ''.join(key_value)

    @staticmethod
    def create_from_symbol(symbol: str):
        """Crée et configure une tuile en fonction du symbole."""
        if symbol == 'S':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['S'][0],
             walkable=Tile.TYPES_AND_SYMBOLS['S'][1])
        elif symbol == 'W':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['W'][0], 
            walkable=Tile.TYPES_AND_SYMBOLS['W'][1])
        elif symbol == 'N':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['N'][0], 
            walkable=Tile.TYPES_AND_SYMBOLS['N'][1])
        elif symbol == '1':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['1'][0], 
            walkable=Tile.TYPES_AND_SYMBOLS['1'][1])
        elif symbol == '2':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['2'][0], 
            walkable=Tile.TYPES_AND_SYMBOLS['2'][1])
        elif symbol == '3':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['3'][0], 
            walkable=Tile.TYPES_AND_SYMBOLS['3'][1])
        elif symbol == '4':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['4'][0], 
            walkable=Tile.TYPES_AND_SYMBOLS['4'][1])
        elif symbol == '5':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['5'][0], 
            walkable=Tile.TYPES_AND_SYMBOLS['5'][1])
        elif symbol == '6':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['6'][0], 
            walkable=Tile.TYPES_AND_SYMBOLS['6'][1])
        elif symbol == 'E':
            return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['E'][0], 
            walkable=Tile.TYPES_AND_SYMBOLS['E'][1])
        else:
            return Tile()

    @staticmethod
    def get_color_for(tile_type: TileType) -> tuple:
        """Retourne la couleur associée au type de tuile spécifié."""

    @property
    def tile_type(self) -> TileType:
        return self.__tile_type

    @property
    def walkable(self) -> bool:
        return self.__walkable
