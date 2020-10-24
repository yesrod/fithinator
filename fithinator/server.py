import a2s

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
        return a2s.info(address)

    def get_players(self):
        return a2s.players(address)

    def get_rules(self):
        return a2s.rules(address)