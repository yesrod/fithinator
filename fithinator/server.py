import a2s
import socket

class Server():

    def __init__(self, addr):
        global address
        address = addr

    def get_address(self):
        return address

    def set_address(self, addr):
        global address
        address = addr

    def get_info(self):
        try:
            return a2s.info(address)
        except socket.timeout:
            return None

    def get_players(self):
        try:
            return a2s.players(address)
        except socket.timeout:
            return None

    def get_rules(self):
        try:
            return a2s.rules(address)
        except socket.timeout:
            return None