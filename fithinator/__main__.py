from .server import Server
from .config import Config

import argparse

def parse_args():
    global parsed_args
    p = argparse.ArgumentParser(description="FITHINATOR: Status monitor for FITH servers")
    p.add_argument('-c', '--config',
                        type=str,
                        default='/boot/fithinator.yml',
                        help='Location of the config file, default /boot/fithinator.yml'
    )
    parsed_args = p.parse_args()

def __main__():
    c = Config(parsed_args.config)

    for target in c.servers.keys():
        server = Server(c.get_server(target))
        info = server.get_info()
        players = server.get_players()

        print(info.server_name)
        print(info.map_name)
        print("%s/%s online" % (info.player_count, info.max_players))
        for player in players:
            print("  " + player.name)
        print()

if __name__ == "__main__":
    parse_args()
    __main__()