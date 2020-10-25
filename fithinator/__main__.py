from .server import Server
from .config import Config
from .display import Display

import argparse
import time
import sys

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
    d = Display(c.get_display())

    try:
        while True:
            output = str()
            for target in c.servers.keys():
                server = Server(c.get_server(target))
                try:
                    info = server.get_info()
                except socket.timeout:
                    output += "Failed to query %s\n\n\n\n" % target
                    continue
                #players = server.get_players()

                output += info.server_name + "\n"
                output += info.map_name + "\n"
                output += "%s/%s online" % (info.player_count, info.max_players) + "\n\n"
                #for player in players:
                #    print("  " + player.name)
                #print()
            d.write(output)
            for i in range(60):
                time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

if __name__ == "__main__":
    parse_args()
    __main__()
