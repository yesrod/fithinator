from .server import Server
from .config import Config
from .display import Display

import sys
import time
import multiprocessing
from queue import Empty


def update_loop(s, q, refresh=15):
    global updating
    updating = True
    while updating:
        try:
            for server in s:
                server.update_info()
                server.update_players()
                server.update_rules()
            q.put(s)
            time.sleep(refresh)
        except KeyboardInterrupt:
            updating = False
            break


def server_setup(c):
    s = []
    for server in c.servers.keys():
        s.append(Server(server, c.get_server(server)))
    return s


def main_loop():
    c = Config(parsed_args.config)
    s = server_setup(c)
    d = Display(c, c.get_display(), s)
    q = multiprocessing.Queue()
    timeout = 15  # seconds, TODO: make this configurable

    try:
        update_process = multiprocessing.Process(
            group=None, 
            target=update_loop, 
            name='hoplite data collection',
            args=(s, q)
        )
        update_process.daemon = True
        update_process.start()
        s = q.get(block=True)
        while True:
            try:
                s = q.get(block=False)
            except Empty:
                pass
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
