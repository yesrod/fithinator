from luma.core import cmdline, error
from luma.core.render import canvas
from PIL import ImageFont, Image

import luma.emulator.device
import pkg_resources

class Display():

    def __init__(self, display):
        self.display = display

        resource_package = __name__
        resource_path = ''
        static_path = pkg_resources.resource_filename(resource_package, resource_path)

        self.font = ImageFont.truetype('%s/font/OpenSans-Regular.ttf' % static_path, 16)

        try:
            parser = cmdline.create_parser(description='FITHINATOR display args')
            conf = cmdline.load_config('%s/conf/%s.conf' % (static_path, display))
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
            self.draw.text((0, 0), output, font=self.font)

    def write_quarters(self, ul=None, ur=None, ll=None, lr=None):
        with canvas(self.device) as self.draw:
            for q in ('ul', 'ur', 'll', 'lr'):
                self.quarter(q, eval(q))

    def quarter(self, quarter, output):
        half_x = int(self.device.width / 2)
        half_y = int(self.device.height / 2)
        quarters = {'ul': (0, 0), 
                    'ur': (half_x, 0), 
                    'll': (0, half_y),
                    'lr': (half_x, half_y)}
        if quarter not in quarters.keys():
            raise ValueError("quarter must be one of %s" % ", ".join(quarters))

        if type(output) == str:
            self.draw.text(quarters[quarter], output, font=self.font)
        elif callable(getattr(output, 'tobitmap', None)):
            resized = output.resize(quarters[quarter])
            self.draw.bitmap(quarters[quarter], resized.tobitmap())

    def load_image(self, image_path):
        return Image.open(image_path)