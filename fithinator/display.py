from luma.core import cmdline, error
from luma.core.render import canvas
import luma.emulator.device
import pkg_resources

class Display():

    def __init__(self, display):
        self.display = display

        resource_package = __name__
        resource_path = '/conf'
        static_path = pkg_resources.resource_filename(resource_package, resource_path)

        try:
            parser = cmdline.create_parser(description='FITHINATOR display args')
            conf = cmdline.load_config('%s/%s.conf' % (static_path, display))
            args = parser.parse_args(conf)
        except FileNotFoundError:
            conf = ['--display=%s' % display]
            args = parser.parse_args(conf)


        try:
            self.device = cmdline.create_device(args)
        except error.Error as e:
            parser.error(e)
            self.device = None

    def write(self, output):
        with canvas(self.device) as self.draw:
            self.draw.text((0, 0), output)