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

        try:
            self.servers = config['servers']
        except KeyError:
            print('ERROR: No servers found in %s' % config_file)
            self.servers = None
        try:
            self.display = config['display']
        except KeyError:
            print('Display not found in %s' % config_file)
            print('Defaulting to ILI9341')
            self.display = 'ili9341'

        try:
            self.summary = config['summary']
            if not isinstance(self.summary, bool):
                self.summary = False
        except KeyError:
            self.summary = False

        try:
            self.details = config['details']
            if not isinstance(self.details, bool):
                self.details = False
        except KeyError:
            self.details = False

        try:
            self.debug = config['debug']
            if not isinstance(self.debug, bool):
                self.debug = False
        except KeyError:
            self.debug = False

    def get_server(self, server):
        return (self.servers[server]['host'],
                self.servers[server]['port']
        )

    def get_display(self):
        return self.display

