from game import Game
from game import GameState
from level import Level
from network import NetClient
from network import NetMessage
from network import NetSettings


class GameClient:
    """Côté client de la couche application de la communication réseau."""
    def __init__(self, host: str, port: int = NetSettings.SERVER_PORT) -> None:
        self.__network_client = NetClient(host, port)
        self.__session_id = '99'

    def handle_messages(self, game: Game) -> None:
        """Traite les messages reçus par le client réseau."""
        messages = self.__network_client.receive()
        for message in messages:
            if message.is_position():
                x = message.data[0:NetMessage.DATA_POS_BYTES]
                y = message.data[NetMessage.DATA_POS_BYTES:]
                player_id = int(message.source)
                game.update_player_position(player_id, (int(x), int(y)))
            elif message.is_session_id():
                if message.data.isdigit():
                    self.__session_id = message.data.zfill(NetMessage.SRC_BYTES)
                    player_id = int(self.__session_id)
                    if player_id == 0:
                        game.declare_ninja()
                    game.state = GameState.STARTED
            elif message.is_level():
                game.set_level(self.__unserialize_level(message.data))
                game.state = GameState.LEVEL_RECEIVED

    def __send(self, message: NetMessage) -> None:
        """Envoie un message au serveur."""
        self.__network_client.send(message)

    def send_level_query(self) -> None:
        """Envoie une demande de niveau."""
        net_msg = NetMessage(NetMessage.CMD_LVL, self.__session_id, NetMessage.DEST_ALL, '')
        self.__send(net_msg)

    def send_position(self, position: tuple) -> None:
        """Envoie la position du joueur au serveur."""
        x_str = str(position[0]).zfill(NetMessage.DATA_POS_BYTES)
        y_str = str(position[1]).zfill(NetMessage.DATA_POS_BYTES)
        net_msg = NetMessage(NetMessage.CMD_POS, self.__session_id, NetMessage.DEST_ALL, x_str + y_str)
        self.__send(net_msg)

    @staticmethod
    def __unserialize_level(level_string: str) -> Level or None:
        """Crée un niveau à partir d'une chaîne de caractères représentant un niveau."""
        number_string = level_string[0:NetMessage.DATA_LVL_NUMBER_BYTES]
        if not number_string.isdigit():
            return None
        number = int(number_string)

        width_offset = NetMessage.DATA_LVL_NUMBER_BYTES
        tiles_offset = width_offset + NetMessage.DATA_LVL_WIDTH_BYTES

        width_string = level_string[width_offset:tiles_offset]
        if not width_string.isdigit():
            return None
        width = int(width_string)

        tiles = level_string[tiles_offset:]

        level = Level()
        level.setup_from_data(number, width, len(tiles) // width, tiles)

        return level

    def who_am_i(self) -> int:
        return int(self.__session_id)

    def start(self) -> None:
        self.__network_client.start()

    def stop(self) -> None:
        self.__network_client.stop()
