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
                y = message.data[3:NetMessage.DATA_POS_BYTES + 3]
                facing = message.data[-1]
                player_id = int(message.source)
                game.update_player_position(player_id, (int(x), int(y)))
                game.update_player_facing(player_id, facing)
            elif message.is_session_id():
                if message.data.isdigit():
                    self.__session_id = message.data.zfill(
                        NetMessage.SRC_BYTES)
                    player_id = int(self.__session_id)
                    if player_id == 0:
                        game.declare_ninja()
                    game.state = GameState.STARTED
            elif message.is_level():
                game.set_level(self.__unserialize_level(message.data))
                game.state = GameState.LEVEL_RECEIVED
            elif message.is_players_list():
                game.update_players_list(message.data)
                game.state = GameState.PLAYERS_LIST_RECEIVED
            elif message.is_active() or message.is_session_close():
                msg_Active = message.data
                player_id = int(message.source)
                is_active = bool(int(msg_Active))
                game.update_is_active(player_id, is_active)
            elif message.is_query_position():
                player = game.get_current_player()
                self.send_position(player.position, player.get_facing())
            elif message.is_hit():
                damage = int(message.data)
                player = game.get_current_player()
                if player.hit(damage) == 0:
                    print('You are dead')
                    self.stop()
            elif message.is_end_game():
                if message.data == NetMessage.VICTORY_TYPE[0]:
                    print('The ninja won!')
                elif message.data == NetMessage.VICTORY_TYPE[1]:
                    print('The samourais won!')
            elif message.is_end_game():
                print(message.data)
                self.stop()

    def __send(self, message: NetMessage) -> None:
        """Envoie un message au serveur."""
        self.__network_client.send(message)

    def send_level_query(self) -> None:
        """Envoie une demande de niveau."""
        net_msg = NetMessage(
            NetMessage.CMD['level'], self.__session_id, NetMessage.DEST_ALL, '')
        self.__send(net_msg)

    def send_players_list_query(self) -> None:
        """Envoie une demande de la liste des joueurs deja present dans le jeu."""
        net_msg = NetMessage(
            NetMessage.CMD['active'], self.__session_id, NetMessage.DEST_ALL, '')
        self.__send(net_msg)

    def send_position(self, position: tuple, facing: str) -> None:
        """Envoie la position du joueur au serveur."""
        x_str = str(position[0]).zfill(NetMessage.DATA_POS_BYTES)
        y_str = str(position[1]).zfill(NetMessage.DATA_POS_BYTES)
        net_msg = NetMessage(
            NetMessage.CMD['position'], self.__session_id, NetMessage.DEST_ALL, x_str + y_str + facing)
        self.__send(net_msg)

    def send_attack(self, damages: int, target: int) -> None:
        """Envoie les degats infliges par un joueur a la cible"""
        damages_str = str(damages).zfill(NetMessage.DATA_ATK_BYTES)
        target_str = str(target).zfill(NetMessage.DATA_TARGET_BYTES)
        net_msg = NetMessage(
            NetMessage.CMD['hit'], self.__session_id, target_str, damages_str)
        self.__send(net_msg)

    def send_dead(self):
        """Envoie que le joueur n'a plus de points de vie"""
        net_msg = NetMessage(
            NetMessage.CMD['playerDead', self.__session_id, NetMessage.DEST_ALL, ''])
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
        message = NetMessage(NetMessage.CMD['close'],
                             self.__session_id, NetMessage.DEST_ALL, '0')
        self.__send(message)
        self.__network_client.stop()
