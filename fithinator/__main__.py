from .server import Server
from .config import Config
from .display import Display

import argparse
import time
import sys
import pkg_resources
import textwrap

from itertools import zip_longest

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
            if not c.summary and not c.details:
                display_summary(c, d)
            else:
                if c.summary:
                    display_summary(c, d)
                if c.details:
                    display_detail(c, d)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

def display_summary(c, d):
    key_chunk = grouper(c.servers.keys(), 3)
    for chunk in key_chunk:
        q = []
        for target in chunk:
            if target == None:
                output = " "
            else:
                output = "\n"
                server = Server(c.get_server(target))
                info = server.get_info()
                if info == None:
                    output += "%s\nUPDATE FAILED\n\n" % target
                else:
                    if info.password_protected:
                        locked = d.lock + " "
                    else:
                        locked = ""

                    output += target + "\n"
                    output += wrapped(info.map_name, int(d.max_char // 2)) + "\n"
                    output += locked + "%s/%s online" % (info.player_count, info.max_players) + "\n\n"
            q.append(output)
        d.write_quarters( ul = q[0],
                          ur = q[1],
                          ll = q[2],
                          lr = d.fith_logo )
        time.sleep(15)

def display_detail(c, d):
    for target in c.servers.keys():
        server = Server(c.get_server(target))
        info = server.get_info()
        if info == None:
            body = "%s\nUPDATE FAILED\n\n" % target
        else:
            if info.password_protected:
                locked = d.lock + " "
            else:
                locked = ""

            body = "\n" + wrapped(info.server_name, d.max_char) + "\n"
            body += "\n" + wrapped(info.map_name, d.max_char) + "\n"
            body += "\n" + locked + "%s/%s online" % (info.player_count, info.max_players) + "\n\n"

        d.write_header_body(target, body)
        time.sleep(15)

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def wrapped(s, max):
    return "\n".join(textwrap.wrap(s, width=max))

if __name__ == "__main__":
    parse_args()
    __main__()
