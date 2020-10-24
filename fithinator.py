import a2s

servers = (
    ('Main Server', ('216.52.148.223', 27015)),
    ('24/7 Payload', ('216.52.148.223', 27069)),
    ('Heavy Boxing', ('216.52.148.223', 27060))
)

for server in servers:
    config_name = server[0]
    info = a2s.info(server[1])
    players = a2s.players(server[1])
    rules = a2s.rules(server[1])

    print(info.server_name)
    print(info.map_name)
    print("%s/%s online" % (info.player_count, info.max_players))
    print()