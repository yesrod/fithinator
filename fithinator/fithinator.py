from fithinator.server import Server
from fithinator.config import Config
from fithinator.display import Display

import logging
import sys
import time
import multiprocessing
from queue import Empty

LOGGER = logging.Logger(__name__)


class Fithinator:
    def __init__(self, parsed_args):
        self.updating = False
        self.config = Config(parsed_args.config)
        self.servers = self.server_setup()
        self.display = Display(
            self.config, 
            self.config.get_display(), 
            self.servers, 
            font_size=self.config.font_size, 
            show_fps=self.config.show_fps
        )
        self.q = multiprocessing.Queue()
        if self.config.debug:
            LOGGER.setLevel(logging.DEBUG)


    def update_loop(self, s, q, refresh=15):
        self.updating = True
        while self.updating:
            try:
                for server in s:
                    server.update_info()
                    server.update_players()
                    server.update_rules()
                q.put(s)
                time.sleep(refresh)
            except KeyboardInterrupt:
                self.updating = False
                break


    def server_setup(self):
        s = []
        for server in self.config.servers.keys():
            s.append(Server(server, self.config.get_server(server)))
        return s


    def main_loop(self):
        timeout = 15  # seconds, TODO: make this configurable

        update_process = multiprocessing.Process(
            group=None, 
            target=self.update_loop, 
            name='hoplite data collection',
            args=(self.servers, self.q)
        )
        update_process.daemon = True
        update_process.start()
        self.servers = self.q.get(block=True)
        try:
            while True:
                try:
                    self.servers = self.q.get(block=False)
                except Empty:
                    pass
                if not self.config.summary and not self.config.details:
                    self.display.display_summary(timeout, servers=self.servers)
                else:
                    if self.config.summary:
                        self.display.display_summary(timeout, servers=self.servers)
                    if self.config.details:
                        self.display.display_detail(timeout, servers=self.servers)
        except (KeyboardInterrupt, SystemExit):
            self.updating = False
            update_process.join(30)
            sys.exit()
