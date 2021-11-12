import arcade
import socket


from game import Game
from game_client import GameClient
from ninja_vs_samourais_window import NinjaVSSamourais


def is_valid_ip(ip: str) -> bool:
    """Valide si une chaîne de caractères représente une adresse IP valide."""
    try:
        socket.inet_aton(ip)
    except socket.error:
        return False

    return True


def main() -> None:
    """Programme principal du client de Ninja VS Samouraïs."""

    game_client = None

    try:
        while True:
            server_ip = input("Game server's IP address: ")
            if is_valid_ip(server_ip):
                break

        game = Game()

        game_client = GameClient(server_ip)
        game_client.start()

        NinjaVSSamourais(game, game_client)
        arcade.run()
    except KeyboardInterrupt:
        if game_client:
            game_client.stop()


if __name__ == '__main__':
    main()
