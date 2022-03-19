from .server import Server
from .servers import Servers
from .config import Config
from .display import Display
from .utils import debug_msg

import argparse
import sys
import time
import pkg_resources
import multiprocessing

def parse_args():
    global parsed_args
    p = argparse.ArgumentParser(description="FITHINATOR: Status monitor for FITH servers")
    p.add_argument('-c', '--config',
                        type=str,
                        default='/boot/fithinator.yml',
                        help='Location of the config file, default /boot/fithinator.yml'
    )
    parsed_args = p.parse_args()


def update_loop(refresh=15):
    global updating
    updating = True
    global s
    while updating:
        try:
            for server in s.server_list:
                server.update_info()
                server.update_players()
                server.update_rules()
            time.sleep(refresh)
        except KeyboardInterrupt:
            updating = False
            break


def server_setup(c):
    s = []
    for server in c.servers.keys():
        s.append(Server(server, c.get_server(server)))
    return s


def __main__():
    c = Config(parsed_args.config)
    global s
    s = Servers(server_setup(c))
    d = Display(c, c.get_display(), s)
    timeout = 15  # seconds, TODO: make this configurable

    try:
        update_process = multiprocessing.Process(
            group=None, 
            target=update_loop, 
            name='hoplite data collection'
        )
        update_process.daemon = True
        update_process.start()
        while True:
            if not c.summary and not c.details:
                d.display_summary(timeout, servers=s)
            else:
                if c.summary:
                    d.display_summary(timeout, servers=s)
                if c.details:
                    d.display_detail(timeout, servers=s)
    except (KeyboardInterrupt, SystemExit):
        global updating
        updating = False
        update_process.join(30)
        sys.exit()

if __name__ == "__main__":
    parse_args()
    __main__()
