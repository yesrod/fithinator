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
            print(f'ERROR: No servers found in {config_file}')
            raise
        try:
            self.display = config['display']
        except KeyError:
            print(f'Display not found in {config_file}')
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

        try:
            self.font_size = int(config['font_size'])
            if not self.font_size:
                self.font_size = 16
        except (KeyError, ValueError):
            self.font_size = 16

        try:
            self.show_fps = config['show_fps']
            if not isinstance(self.show_fps, bool):
                self.show_fps = False
        except KeyError:
            self.show_fps = False

    def get_server(self, server):
        return (self.servers[server]['host'],
                self.servers[server]['port']
        )

    def get_display(self):
        return self.display

