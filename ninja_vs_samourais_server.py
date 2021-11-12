from time import sleep


from game import Game
from game_server import GameServer


def main(game_server: GameServer) -> None:
    """Programme principal du serveur de Ninja VS Samouraïs."""
    game = Game()
    game.next_level()

    while True:
        game_server.handle_messages(game)
        sleep(0.05)


if __name__ == '__main__':

    server = GameServer()
    server.start()
    print(f'Game server started at {server.get_ip()} on port {server.get_port()}')

    try:
        main(server)
    except KeyboardInterrupt:
        server.stop()
