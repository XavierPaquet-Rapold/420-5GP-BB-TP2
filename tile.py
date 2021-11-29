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
                        TileType.WALL: (255, 255, 255),
                        TileType.EXIT: (64, 64, 64)}

    TYPES_AND_SYMBOLS = {' ': {'tileType': TileType.GROUND, 'walkable': True},
                         'S': {'tileType': TileType.STONE, 'walkable': False},
                         'W': {'tileType': TileType.WALL, 'walkable': False},
                         'N': {'tileType': TileType.NINJA_START_POS, 'walkable': True},
                         '1': {'tileType': TileType.SAMOURAI_START_POS_1, 'walkable': True},
                         '2': {'tileType': TileType.SAMOURAI_START_POS_2, 'walkable': True},
                         '3': {'tileType': TileType.SAMOURAI_START_POS_3, 'walkable': True}, 
                         '4': {'tileType': TileType.SAMOURAI_START_POS_4, 'walkable': True}, 
                         '5': {'tileType': TileType.SAMOURAI_START_POS_5, 'walkable': True},
                         '6': {'tileType': TileType.SAMOURAI_START_POS_6, 'walkable': True},
                         'E': {'tileType': TileType.EXIT, 'walkable': True}
                        }


    def __init__(self, walkable: bool = True, tile_type: TileType = TileType.GROUND) -> None:
        self.__walkable = walkable
        self.__tile_type = tile_type

    def __str__(self) -> str:
        tile_type = self.__tile_type
        symbol = ''
        for key, value in self.TYPES_AND_SYMBOLS.items():
            if tile_type == value['tileType']:
                symbol = key
        return symbol

    @staticmethod
    def create_from_symbol(symbol: str):
        """Crée et configure une tuile en fonction du symbole."""
        type_and_symbol = Tile.TYPES_AND_SYMBOLS
        tile = Tile()
        value = type_and_symbol.get(symbol)
        if value:
            tile = Tile(tile_type= value['tileType'], walkable= value['walkable'])
        return tile

    @staticmethod
    def get_color_for(tile_type: TileType) -> tuple:
        """Retourne la couleur associée au type de tuile spécifié."""

    @property
    def tile_type(self) -> TileType:
        return self.__tile_type

    @property
    def walkable(self) -> bool:
        return self.__walkable
