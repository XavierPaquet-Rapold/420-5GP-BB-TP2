from game import Game
from network import NetMessage
from network import NetServer
from network import NetSettings


class GameServer:
    """Côté serveur de la couche application de la communication réseau."""
    def __init__(self, host: str = NetSettings.SERVER_HOST, port: int = NetSettings.SERVER_PORT) -> None:
        self.__network_server = NetServer(host, port)

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
                net_msg = NetMessage(message.command, message.source, NetMessage.DEST_ALL, message.data)
                self.__send_to_all_but_source(net_msg)
            elif message.is_level():
                self.send_level_to(message.source, str(game.level))

    def get_ip(self) -> str:
        return self.__network_server.get_ip()

    def get_port(self) -> int:
        return self.__network_server.get_port()

    def send_level(self, level: str) -> None:
        """Envoie un niveau de jeu à tous les clients."""
        net_msg = NetMessage(NetMessage.CMD_LVL, NetMessage.SRC_SERVER, NetMessage.DEST_ALL, level)
        self.__send(net_msg)

    def send_level_to(self, destination, level: str) -> None:
        """Envoie un niveau de jeu à un client (destination)."""
        net_msg = NetMessage(NetMessage.CMD_LVL, NetMessage.SRC_SERVER, destination, level)
        self.__send(net_msg)

    def start(self) -> None:
        self.__network_server.start()

    def stop(self) -> None:
        self.__network_server.stop()
