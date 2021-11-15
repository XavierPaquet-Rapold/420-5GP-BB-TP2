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

    # TYPES_AND_SYMBOLS = {' ': {TileType : TileType.GROUND, 'walkable': True},
    #                      'S': {TileType : TileType.STONE, 'walkable' : False},
    #                      'W': {TileType: TileType.WALL, 'walkable' :False},
    #                      'N': {TileType: TileType.NINJA_START_POS, 'walkable' :True},
    #                      '1': {TileType: TileType.SAMOURAI_START_POS_1, 'walkable' :True},
    #                      '2': {TileType: TileType.SAMOURAI_START_POS_2, 'walkable' :True},
    #                      '3': {TileType: TileType.SAMOURAI_START_POS_3, 'walkable' :True},
    #                      '4': {TileType: TileType.SAMOURAI_START_POS_4, 'walkable' :True},
    #                      '5': {TileType: TileType.SAMOURAI_START_POS_5, 'walkable' :True},
    #                      '6': {TileType: TileType.SAMOURAI_START_POS_6, 'walkable' :True},
    #                      'E': {TileType: TileType.EXIT, 'walkable': True}}
    TYPES_AND_SYMBOLS = {' ': TileType.GROUND,
                         'S': TileType.STONE,
                         'W': TileType.WALL,
                         'N': TileType.NINJA_START_POS,
                         '1': TileType.SAMOURAI_START_POS_1,
                         '2': TileType.SAMOURAI_START_POS_2,
                         '3': TileType.SAMOURAI_START_POS_3, 
                         '4': TileType.SAMOURAI_START_POS_4, 
                         '5': TileType.SAMOURAI_START_POS_5,
                         '6': TileType.SAMOURAI_START_POS_6,
                         'E': TileType.EXIT}


    def __init__(self, walkable: bool = True, tile_type: TileType = TileType.GROUND) -> None:
        self.__walkable = walkable
        self.__tile_type = tile_type

    def __str__(self) -> str:
        #return self.TYPES_AND_SYMBOLS[self.__tile_type]
        return str(list(self.TYPES_AND_SYMBOLS.keys())[list(self.TYPES_AND_SYMBOLS.values()).index(self.__tile_type)])

    @staticmethod
    def create_from_symbol(symbol: str):
        """Crée et configure une tuile en fonction du symbole."""
        if symbol == 'S':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['S'][TileType],
            #  walkable=Tile.TYPES_AND_SYMBOLS['S']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['S'], walkable=False)
        elif symbol == 'W':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['W'][TileType], 
            # walkable=Tile.TYPES_AND_SYMBOLS['W']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['W'], walkable=False)
        elif symbol == 'N':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['N'][TileType], 
            # walkable=Tile.TYPES_AND_SYMBOLS['N']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['N'])
        elif symbol == '1':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['1'][TileType], 
            # walkable=Tile.TYPES_AND_SYMBOLS['1']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['1'])
        elif symbol == '2':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['2'][TileType], 
            # walkable=Tile.TYPES_AND_SYMBOLS['2']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['2'])
        elif symbol == '3':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['3'][TileType], 
            # walkable=Tile.TYPES_AND_SYMBOLS['3']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['3'])
        elif symbol == '4':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['4'][TileType], 
            # walkable=Tile.TYPES_AND_SYMBOLS['4']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['4'])
        elif symbol == '5':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['5'][TileType], 
            # walkable=Tile.TYPES_AND_SYMBOLS['5']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['5'])
        elif symbol == '6':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['6'][TileType], 
            # walkable=Tile.TYPES_AND_SYMBOLS['6']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['6'])
        elif symbol == 'E':
            # return Tile(tile_type= Tile.TYPES_AND_SYMBOLS['E'][TileType], 
            # walkable=Tile.TYPES_AND_SYMBOLS['E']['walkable'])
            return Tile(tile_type=Tile.TYPES_AND_SYMBOLS['E'])
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
