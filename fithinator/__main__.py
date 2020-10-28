from .server import Server
from .config import Config
from .display import Display

import argparse
import time
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

    resource_package = __name__
    resource_path = ''
    static_path = pkg_resources.resource_filename(resource_package, resource_path)

    fith_logo = d.load_image('%s/font/FITH_Logo.jpg' % static_path)
    lock = "\ua5c3"

    try:
        while True:
            q = []
            for target in c.servers.keys():
                output = "\n"
                server = Server(c.get_server(target))
                info = server.get_info()
                if info == None:
                    output += "%s\nUPDATE FAILED\n\n" % target
                    continue

                if info.password_protected:
                    locked = lock + " "
                else:
                    locked = ""

                output += target + "\n"
                output += info.map_name + "\n"
                output += locked + "%s/%s online" % (info.player_count, info.max_players) + "\n\n"
                q.append(output)
            while len(q) < 4:
                q.append(fith_logo)
            d.write_quarters( ul = q[0],
                              ur = q[1],
                              ll = q[2],
                              lr = q[3] )
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

if __name__ == "__main__":
    parse_args()
    __main__()
