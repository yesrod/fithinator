from luma.core import cmdline, error
from luma.core.render import canvas
from PIL import ImageFont, Image

import luma.emulator.device
import pkg_resources

class Display():

    def __init__(self, display, font_size=16):
        self.display = display

        resource_package = __name__
        resource_path = ''
        static_path = pkg_resources.resource_filename(resource_package, resource_path)

        self.font_size = font_size
        self.font_size_px = int(font_size * 1.33333333)
        self.font = ImageFont.truetype('%s/font/FreeSans.ttf' % static_path, self.font_size)

        self.fith_logo = self.load_image('%s/font/FITH_Logo.jpg' % static_path)
        self.lock = "\ua5c3"

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

    def text_align_center(self, xy, message, fill="white"):
        half_x = int(self.device.width / 2)
        lines = message.split('\n')
        for i, line in enumerate(lines):
            w = self.draw.textsize(line, font=self.font)[0]
            self.draw.text((xy[0] + ((half_x - w) / 2), 
                            xy[1] + (self.font_size_px * i)),
                            line, 
                            fill = fill,
                            font=self.font)

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
            self.text_align_center(quarters[quarter], output)
        elif callable(getattr(output, 'tobitmap', None)):
            self.draw.bitmap(quarters[quarter], 
                    output.resize((half_x, half_y)).convert('1')
            )

    def write_header(self, output):
        self.text_align_center((0,0), output)

    def write_body(self, output):
        self.text_align_center((0,self.font_size_px), output)

    def load_image(self, image_path):
        return Image.open(image_path)
