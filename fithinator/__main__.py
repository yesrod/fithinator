from .server import Server
from .config import Config

c = Config('config.yml')

for target in c.servers.keys():
    server = Server(c.get_server(target))
    info = server.get_info()

    print(info.server_name)
    print(info.map_name)
    print("%s/%s online" % (info.player_count, info.max_players))
    print()