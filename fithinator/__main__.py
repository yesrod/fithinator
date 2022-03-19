from .server import Server
from .config import Config
from .display import Display
from .utils import debug_msg

import argparse
import sys
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


def update_loop(s, refresh=15):
    global updating
    updating = True
    while updating:
        for server in s:
            s.update_info()
            s.update_players()
            s.update_rules()
        time.sleep(refresh)


def server_setup(c):
    s = []
    for server in c.servers.keys():
        s.append(Server(c.get_server(server)))
    return s


def __main__():
    c = Config(parsed_args.config)
    s = server_setup(c)
    debug_msg(c, s)
    d = Display(c, c.get_display(), s)
    timeout = 15  # seconds, TODO: make this configurable

    try:
        update_process = multiprocessing.Process(
            group=None, 
            target=update_loop, 
            name='hoplite data collection', 
            args=(s)
        )
        update_process.daemon = True
        update_process.start()
        while True:
            if not c.summary and not c.details:
                d.display_summary(timeout)
            else:
                if c.summary:
                    d.display_summary(timeout)
                if c.details:
                    d.display_detail(timeout)
    except (KeyboardInterrupt, SystemExit):
        global updating
        updating = False
        update_process.join(30)
        sys.exit()

if __name__ == "__main__":
    parse_args()
    __main__()
