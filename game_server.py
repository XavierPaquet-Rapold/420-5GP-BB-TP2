from game import Game
from network import NetMessage
from network import NetServer
from network import NetSettings


class GameServer:
    """Côté serveur de la couche application de la communication réseau."""

    def __init__(self, host: str = NetSettings.SERVER_HOST, port: int = NetSettings.SERVER_PORT) -> None:
        self.__network_server = NetServer(host, port)
        self.__is_possible_to_win = False
        self.__players = []

    def __send(self, message: NetMessage) -> None:
        """Envoie un message à tous les clients."""
        self.__network_server.send(message)

    def __send_to_all_but_source(self, message: NetMessage) -> None:
        """Envoie un message à tous les clients sauf celui identifié comme la source du message."""
        self.__network_server.send_to_all_but_one(message, message.source)

    def handle_messages(self, game: Game) -> None:
        """Traite les messages reçus par le serveur réseau."""
        messages = self.__network_server.receive()
        for message in messages:
            if message.is_position():
                net_msg = NetMessage(
                    message.command, message.source, NetMessage.DEST_ALL, message.data)
                self.__send_to_all_but_source(net_msg)
            elif message.is_level():
                self.send_level_to(message.source, str(game.level))
            elif message.is_active():
                self.__players.append(message.source)
                self.send_players_list_to(
                    message.source, ",".join(self.__players))
                self.send_new_player_active(message.source)
                self.send_query_position(message.source)
            elif message.is_session_close():
                if message.source in self.__players:
                    self.__players.remove(message.source)
                net_msg = NetMessage(
                    message.command, message.source, NetMessage.DEST_ALL, message.data)
                self.__send_to_all_but_source(net_msg)
                if message.source in self.__players:
                    self.__players.remove(message.source)
                self.__network_server.close_session_controller(message.source)
                self.check_for_end_game(message.source)
            elif message.is_hit():
                net_msg = NetMessage(
                    message.command, message.source, message.destination, message.data)
                self.__send(net_msg)

    def get_ip(self) -> str:
        return self.__network_server.get_ip()

    def get_port(self) -> int:
        return self.__network_server.get_port()

    def send_level(self, level: str) -> None:
        """Envoie un niveau de jeu à tous les clients."""
        net_msg = NetMessage(
            NetMessage.CMD['level'], NetMessage.SRC_SERVER, NetMessage.DEST_ALL, level)
        self.__send(net_msg)

    def send_level_to(self, destination: str, level: str) -> None:
        """Envoie un niveau de jeu à un client (destination)."""
        net_msg = NetMessage(
            NetMessage.CMD['level'], NetMessage.SRC_SERVER, destination, level)
        self.__send(net_msg)

    def send_players_list_to(self, destination: str, players: str) -> None:
        """Envoie une liste de tout les joueurs deja present dans le jeu à un client (destination)."""
        net_msg = NetMessage(NetMessage.CMD['players'],
                             NetMessage.SRC_SERVER, destination, players)
        self.__send(net_msg)

        if destination == '00':
            self.__is_possible_to_win = True

    def check_for_end_game(self, close_source: str):
        """Verifie si la partie est finie et envoie que la partie est finie aux clients dans le cas echeant"""
        if self.__is_possible_to_win:
            if len(self.__players) <= 0:
                print('No players left in the game!')
                pass
            if close_source == '00' and len(self.__players) > 0:
                print('The samourais have won!')
                self.send_end_game(NetMessage.VICTORY_TYPE[1])
                pass
            if '00' in self.__players and len(self.__players) == 1:
                print('The ninja won!')
                self.send_end_game(NetMessage.VICTORY_TYPE[0])
                pass

    def send_new_player_active(self, source) -> None:
        """Averti qu'un nouveau joueur s'est ajoute a la partie"""
        net_msg = NetMessage(
            NetMessage.CMD['active'], source, NetMessage.DEST_ALL, '1')
        self.__send(net_msg)

    def send_query_position(self, source):
        """Demande a tous les clients d'envoyer leur position"""
        net_msg = NetMessage(
            NetMessage.CMD['queryPosition'], source, NetMessage.DEST_ALL, '')
        self.__send(net_msg)

    def send_end_game(self, data: str):
        """Envoie a tous les clients que la partie est terminee"""
        net_msg = NetMessage(
            NetMessage.CMD['endGame'], NetMessage.SRC_SERVER, NetMessage.DEST_ALL, data)
        self.__send(net_msg)

    def start(self) -> None:
        self.__network_server.start()

    def stop(self) -> None:
        self.__network_server.stop()
