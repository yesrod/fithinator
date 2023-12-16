import a2s
from a2s.exceptions import BrokenMessageError
import socket

class Server():

    def __init__(self, name, addr):
        self.name = name
        self.address = addr
        self.info = None
        self.players = None
        self.rules = None


    def set_address(self, addr):
        self.address = addr


    def update_info(self):
        try:
            self.info = a2s.info(self.address)
        except (socket.timeout, OSError, BrokenMessageError):
            print(f"{self.name}: error updating info")
            self.info = None


    def update_players(self):
        try:
            self.players = a2s.players(self.address)
        except (socket.timeout, OSError, BrokenMessageError):
            print(f"{self.name}: error updating players")
            self.players = None


    def update_rules(self):
        try:
            self.rules = a2s.rules(self.address)
        except (socket.timeout, OSError, BrokenMessageError):
            print(f"{self.name}: error updating rules")
            self.rules = None
