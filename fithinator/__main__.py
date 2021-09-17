from .server import Server
from .config import Config
from .display import Display

import argparse
import sys
import pkg_resources

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
    timeout = 15  # seconds, TODO: make this configurable

    try:
        while True:
            if not c.summary and not c.details:
                d.display_summary(c, d, timeout)
            else:
                if c.summary:
                    d.display_summary(c, d, timeout)
                if c.details:
                    d.display_detail(c, d, timeout)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

if __name__ == "__main__":
    parse_args()
    __main__()
