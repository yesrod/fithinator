import yaml

class Config():

    def __init__(self, config_file):
        with open(config_file, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as x:
                print(x)
                config = None
                return

        self.servers = config['servers']

    def get_server(self, server):
        return (self.servers[server]['host'],
                self.servers[server]['port']
        )
