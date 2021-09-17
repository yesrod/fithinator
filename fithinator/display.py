from .server import Server
from .config import Config

from luma.core import cmdline, error
from luma.core.render import canvas
from PIL import ImageFont, Image

from itertools import zip_longest

import luma.emulator.device
import pkg_resources
import textwrap
import time

map_types = {
    "ctf": "Capture the Flag",
    "cp": "Control Point",
    "tc": "Territorial Control",
    "pl": "Payload",
    "arena": "Arena",
    "plr": "Payload Race",
    "koth": "King of the Hill",
    "sd": "Special Delivery",
    "mvm": "Mann vs. Machine",
    "rd": "Robot Destruction",
    "pd": "Player Destruction",
    "rats": "Rats"
}

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

        self.max_char = int(self.device.width // self.textsize("A")[0])

    def text_align_center(self, xy, bounds, message, fill="white"):
        bound_w = bounds[0]
        lines = message.split('\n')
        for i, line in enumerate(lines):
            w = self.draw.textsize(line, font=self.font)[0]
            self.draw.text((xy[0] + ((bound_w - w) / 2), 
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
        bounds = (half_x, half_y)
        quarters = {'ul': (0, 0), 
                    'ur': (half_x, 0), 
                    'll': (0, half_y),
                    'lr': (half_x, half_y)}
        if quarter not in quarters.keys():
            raise ValueError("quarter must be one of %s" % ", ".join(quarters))

        if type(output) == str:
            self.text_align_center(quarters[quarter], bounds, output)
        elif callable(getattr(output, 'tobitmap', None)):
            self.draw.bitmap(quarters[quarter], 
                    output.resize((half_x, half_y)).convert('1')
            )

    def write_header_body(self, header, body):
        with canvas(self.device) as self.draw:
            self.header(header)
            self.body(body)

    def header(self, output):
        self.text_align_center(
            (0,0),
            (self.device.width, self.device.height), 
            output)

    def body(self, output):
        self.text_align_center(
            (0,self.font_size_px), 
            (self.device.width, self.device.height),
            output)

    def load_image(self, image_path):
        return Image.open(image_path)

    def textsize(self, s):
        return self.font.getsize(s)

    def grouper(self, iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    def wrapped(self, s, max):
        return "\n".join(textwrap.wrap(s, width=max))

    def display_summary(self, c, d, timeout):
        key_chunk = self.grouper(c.servers.keys(), 3)
        for chunk in key_chunk:
            q = []
            for target in chunk:
                if target == None:
                    output = " "
                else:
                    output = ""
                    server = Server(c.get_server(target))
                    info = server.get_info()
                    if info == None:
                        output += "%s\nUPDATE FAILED\n\n" % target
                    else:
                        if info.password_protected:
                            locked = d.lock + " "
                        else:
                            locked = ""

                        map_array = info.map_name.split('_')
                        map_type_raw = map_array.pop(0)
                        try:
                            map_type = map_types[map_type_raw]
                        except (KeyError, IndexError):
                            map_type = map_type_raw

                        map_name = " ".join(map_array).title()

                        output += target + "\n"
                        output += map_type + "\n"
                        output += self.wrapped(map_name, int(d.max_char // 2)) + "\n"
                        output += locked + "%s/%s online" % (info.player_count, info.max_players) + "\n\n"
                q.append(output)
            d.write_quarters( ul = q[0],
                            ur = q[1],
                            ll = q[2],
                            lr = d.fith_logo )
            time.sleep(timeout)

    def display_detail(self, c, d, timeout):
        for target in c.servers.keys():
            server = Server(c.get_server(target))
            info = server.get_info()
            if info == None:
                body = "%s\nUPDATE FAILED\n\n" % target
            else:
                if info.password_protected:
                    locked = d.lock + " "
                else:
                    locked = ""

                body = "\n" + self.wrapped(info.server_name, d.max_char) + "\n"
                body += "\n" + self.wrapped(info.map_name, d.max_char) + "\n"
                body += "\n" + locked + "%s/%s online" % (info.player_count, info.max_players) + "\n\n"

            d.write_header_body(target, body)
            time.sleep(timeout)