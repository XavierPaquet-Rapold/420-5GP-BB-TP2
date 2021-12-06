import select
import socket
import sys
import threading

from queue import Empty, Queue
from typing import Dict

from arcade.color import NEON_GREEN


MAX_RX_QSIZE = 10
MAX_TX_QSIZE = 10
LISTEN_QUEUE = 5


class NetSettings:
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 20000


class NetMessage:
    """
        Messages échangés entre les clients et le serveur.
        Format: commande|source|destination|longueur des données|données

        Données pour...
            CMD_SID: identifiant de session(2)
            CMD_POS: x(3)|y(3)
            CMD_LVL: numéro de niveau(2)|largeur(3)|chaîne de niveau(n)
    """
    CMD_BYTES = 3
    SRC_BYTES = 2
    DEST_BYTES = 2
    DATA_LENGTH_BYTES = 5

    HEADER_BYTES = CMD_BYTES + SRC_BYTES + DEST_BYTES + DATA_LENGTH_BYTES

    CMD_OFFSET = 0
    SRC_OFFSET = CMD_BYTES
    DEST_OFFSET = SRC_OFFSET + SRC_BYTES
    DATA_LENGTH_OFFSET = DEST_OFFSET + DEST_BYTES
    DATA_OFFSET = HEADER_BYTES

    CMD = {'sessionID': 'SID', 'position': 'POS', 'level': 'LVL',
           'active': 'ACT', 'players': 'PLL', 'close': 'CLO', 'hit': 'HIT', 'queryPosition': 'QPO',
           'endGame': 'END'}

    DATA_POS_BYTES = 3
    DATA_ATK_BYTES = 2
    DATA_TARGET_BYTES = 2

    DATA_LVL_NUMBER_BYTES = 2
    DATA_LVL_WIDTH_BYTES = 3

    SRC_UNDEFINED = '98'
    SRC_SERVER = '99'
    DEST_ALL = '99'

    VICTORY_TYPE = ('ninja', 'samourais')

    def __init__(self, command, source, destination, data: str) -> None:
        self.__command = command
        self.__source = source
        self.__destination = destination
        self.__data = data

    def copy(self):
        """Retourne une copie du message."""
        return NetMessage(self.command, self.source, self.destination, self.data)

    def is_level(self) -> bool:
        return self.__command == self.CMD['level']

    def is_players_list(self) -> bool:
        return self.__command == self.CMD['players']

    def is_active(self) -> bool:
        return self.__command == self.CMD['active']

    def is_position(self) -> bool:
        return self.__command == self.CMD['position']

    def is_session_id(self) -> bool:
        return self.__command == self.CMD['sessionID']

    def is_session_close(self) -> bool:
        return self.__command == self.CMD['close']

    def is_hit(self) -> bool:
        return self.__command == self.CMD['hit']

    def is_query_position(self) -> bool:
        return self.__command == self.CMD['queryPosition']

    def is_end_game(self) -> bool:
        return self.__command == self.CMD['endGame']

    def is_player_dead(self) -> bool:
        return self.__command == self.CMD['playerDead']

    @property
    def command(self) -> str:
        return self.__command

    @property
    def data(self) -> str:
        return self.__data

    @property
    def destination(self) -> str:
        return self.__destination

    @property
    def source(self) -> str:
        return self.__source


def message2data(message: NetMessage) -> str:
    """Transforme un message en une chaîne de caractères (COMMAND|DATA LENGTH|DATA) à transmettre sur le réseau."""
    return message.command + message.source + \
        message.destination + \
        str(len(message.data)).zfill(
            NetMessage.DATA_LENGTH_BYTES) + message.data


def data2message(string: str) -> NetMessage or int or None:
    """Transforme une chaîne de caractères (COMMAND|DATA LENGTH|DATA) reçue du réseau en message."""
    if len(string) < NetMessage.HEADER_BYTES:
        return

    src = string[NetMessage.SRC_OFFSET:NetMessage.SRC_OFFSET +
                 NetMessage.SRC_BYTES]
    if not src.isdigit():
        return len(string)

    dest = string[NetMessage.DEST_OFFSET:NetMessage.DEST_OFFSET +
                  NetMessage.DEST_BYTES]
    if not dest.isdigit():
        return len(string)

    data_length_str = string[NetMessage.DATA_LENGTH_OFFSET:
                             NetMessage.DATA_LENGTH_OFFSET+NetMessage.DATA_LENGTH_BYTES]
    if not data_length_str.isdigit():
        return len(string)
    data_length = int(data_length_str)

    if len(string) < NetMessage.HEADER_BYTES + data_length:
        return

    cmd = string[NetMessage.CMD_OFFSET:NetMessage.CMD_OFFSET +
                 NetMessage.CMD_BYTES]

    net_command = NetMessage.CMD
    if not cmd in net_command.values():
        return len(string)

    data = string[NetMessage.DATA_OFFSET:NetMessage.DATA_OFFSET+data_length]

    return NetMessage(cmd, src, dest, data)


class NetSessionController:
    """Gère les tâches RX et TX d'une session TCP/IP."""

    def __init__(self, client_socket: socket.socket) -> None:
        self.tx_queue = Queue(maxsize=MAX_TX_QSIZE)
        self.rx_queue = Queue(maxsize=MAX_RX_QSIZE)

        self.tx = NetTX(client_socket, self)
        self.rx = NetRX(client_socket, self)

    def read(self) -> NetMessage or None:
        if not self.rx_queue.empty():
            return self.rx_queue.get()

        return None

    def start(self) -> None:
        self.tx.start()
        self.rx.start()

    def stop(self) -> None:
        self.tx.stop()
        self.tx.join()
        self.rx.stop()
        self.rx.join()

    def write(self, message: NetMessage) -> None:
        if not self.tx_queue.full():
            self.tx_queue.put(message)


class NetClient:
    """Client d'une session TCP/IP. Couche présentation de la communication réseau."""

    def __init__(self, host: str = NetSettings.SERVER_HOST, port: int = NetSettings.SERVER_PORT) -> None:

        print(f"Connecting to {host} on port {port}...")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((host, port))
        except socket.error:
            print("ERROR: Failed to connect to server!")
            sys.exit()

        print("Connected!")

        self.session_ctrl = NetSessionController(client_socket)

    def receive(self) -> list:
        messages = []

        while True:
            message = self.session_ctrl.read()
            if message:
                messages.append(message)
            else:
                break

        return messages

    def send(self, message: NetMessage) -> None:
        self.session_ctrl.write(message)

    def start(self) -> None:
        self.session_ctrl.start()

    def stop(self) -> None:
        self.session_ctrl.stop()
        print("Client diconnected from server")


class NetListener(threading.Thread):
    """Écoute pour de nouvelles connexions au serveur. Crée les sessions."""

    def __init__(self, server_socket: socket.socket,
                 host: str = NetSettings.SERVER_HOST, port: int = NetSettings.SERVER_PORT) -> None:
        super().__init__()

        self.server_socket = server_socket
        self.host = host
        self.port = port

        # Dictionnaire sous le format {session_id: isUsed}
        self.sessions_ids = {0: False, 1: False, 2: False,
                             3: False, 4: False, 5: False, 6: False}

        self.session_controllers = []

        self.running = False

    @staticmethod
    def __send_session_id(ctrl: NetSessionController, session_id: int) -> None:
        ctrl.write(NetMessage(NetMessage.CMD['sessionID'],
                              NetMessage.SRC_SERVER,
                              str(session_id).zfill(NetMessage.SRC_BYTES),
                              str(session_id)))

    def __get_key(self, val):
        for key, value in self.sessions_ids.items():
            if val == value:
                return key
        return -1

    def ctrl(self, session_id: int) -> NetSessionController:
        return self.session_controllers[session_id]

    def run(self) -> None:
        self.server_socket.listen(LISTEN_QUEUE)
        self.running = True

        while self.running:
            try:
                readable, _, _ = select.select(
                    [self.server_socket], [], [], 0.1)
                for _ in readable:
                    client_socket, ip_address = self.server_socket.accept()
                    session_id = self.__get_key(False)

                    # On crée un contrôleur pour servir cette session client...
                    session_controller = NetSessionController(
                        client_socket)

                    if len(self.session_controllers) >= session_id + 1:
                        self.session_controllers[session_id] = session_controller
                    else:
                        self.session_controllers.append(session_controller)

                    session_controller.start()

                    # On cherche le premier session_id qui dont l'usage est False
                    if session_id != -1:
                        self.__send_session_id(session_controller, session_id)
                        self.sessions_ids[session_id] = True
                        print(f"Client {session_id} connected from {ip_address[0]}:{ip_address[1]}")
                    else:
                        print("No spot is left for another player")

            except OSError:
                break

    def stop(self) -> None:
        for ctrl in self.session_controllers:
            ctrl.stop()
        self.running = False
        print("Server closed")

    def notify_session_stoped(self, session_id: int) -> None:
        self.sessions_ids[session_id] = False


class NetServer:
    """Serveur de sessions TCP/IP. Couche présentation de la communication réseau."""

    def __init__(self, host: str = NetSettings.SERVER_HOST, port: int = NetSettings.SERVER_PORT) -> None:
        print("Starting server...")

        self.__server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        self.__server_socket.setblocking(False)

        try:
            self.__server_socket.bind((host, port))
        except socket.error:
            print("ERROR : Failed to bind socket.")
            sys.exit()

        self.listener = NetListener(self.__server_socket)

    @staticmethod
    def get_ip() -> str:
        """Retourne l'adresse IP du serveur."""
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        return local_ip

    def get_port(self) -> int:
        """Retourne le port sur lequel écoute le serveur."""
        return self.__server_socket.getsockname()[1]

    def receive(self) -> list:
        all_messages = []
        for ctrl in self.listener.session_controllers:
            messages = self.receive_from_ctrl(ctrl)
            for message in messages:
                all_messages.append(message)
        return all_messages

    @staticmethod
    def receive_from_ctrl(ctrl: NetSessionController) -> list:
        messages = []

        if ctrl:
            while True:
                message = ctrl.read()
                if message:
                    messages.append(message)
                else:
                    break

        return messages

    def send(self, message: NetMessage) -> None:
        """Envoie un message à tous les clients connectés."""
        if message.destination != NetMessage.DEST_ALL:
            ctrl_to_send = self.listener.ctrl(int(message.destination))
            ctrl_to_send.write(message.copy())
        else:
            for ctrl in self.listener.session_controllers:
                ctrl.write(message.copy())

    def send_to_all_but_one(self, message: NetMessage, session_id: str) -> None:
        """Envoie un message à tous les clients connectés sauf un (session_id)."""
        ctrl_to_avoid = self.listener.ctrl(int(session_id))
        for ctrl in self.listener.session_controllers:
            if ctrl != ctrl_to_avoid:
                ctrl.write(message.copy())

    def sessions_controllers(self) -> list:
        return self.listener.session_controllers

    def close_session_controller(self, session_id: str) -> None:
        ctrl = self.listener.session_controllers[int(session_id)]
        ctrl.stop()
        self.listener.notify_session_stoped(int(session_id))

    def start(self) -> None:
        self.listener.start()

    def stop(self) -> None:
        self.listener.stop()


class NetRX(threading.Thread):
    """Tâche de réception des messages en provenance du réseau."""

    def __init__(self, session_socket: socket.socket, session_controller: NetSessionController) -> None:
        super().__init__()

        self.session_socket = session_socket
        self.session_socket.setblocking(False)
        self.session_controller = session_controller

        self.running = False

    def __queue(self, messages: list) -> None:
        """Place un ou plusieus messages sur la queue RX."""
        for message in messages:
            self.session_controller.rx_queue.put(message)

    @staticmethod
    def __split(data: str) -> list:
        """Découpe une chaîne de caractères reçue du réseau en messages."""
        messages = []

        while len(data) > 0:
            message = data2message(data)
            if not message:
                print("ERROR: data doesn't respect length, buffer dropped")
                break
            if type(message) == NetMessage:
                data = data[NetMessage.HEADER_BYTES+len(message.data):]
                messages.append(message)
            else:
                data = data[message:]
                print("ERROR: bad data type, message dropped")

        return messages

    def run(self) -> None:
        self.running = True

        while self.running:
            try:
                readable, _, _ = select.select(
                    [self.session_socket], [], [], 0.1)
                for s in readable:
                    if s == self.session_socket:
                        raw_data = self.session_socket.recv(4096)
                    if raw_data:
                        data = raw_data.decode()
                        messages = self.__split(data)
                        self.__queue(messages)
            except OSError:
                print("ERROR: Connection with server interrupted.")
                break

        self.session_socket.close()

    def stop(self) -> None:
        self.running = False


class NetTX(threading.Thread):
    """Tâche de transmission des messages vers le réseau."""

    def __init__(self, session_socket: socket.socket, session_controller: NetSessionController) -> None:
        super().__init__()

        self.session_socket = session_socket
        self.session_controller = session_controller

        self.running = False

    def run(self) -> None:
        self.running = True

        while self.running:
            if self.session_controller.tx_queue.not_empty:
                try:
                    message = self.session_controller.tx_queue.get(timeout=0.1)
                    data = message2data(message)
                    self.session_socket.send(data.encode())
                except Empty:
                    continue
                except OSError:
                    break

    def stop(self) -> None:
        self.running = False
