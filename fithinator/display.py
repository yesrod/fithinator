from fithinator.renderable.image import ImageFile
from fithinator.renderable.spinner import Spinner

from luma.core import cmdline
from luma.core.render import canvas
from PIL import ImageFont

from itertools import zip_longest

import importlib.resources
import logging
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
    "rats": "Rats",
    "tfdb": "Dodgeball",
    "vsh": "Vs. Saxton Hale"
}

LOGGER = logging.Logger(__name__)

class Display():

    def __init__(self, config, display, servers, font_size=16):
        self.config = config
        self.display = display
        self.servers = servers

        with importlib.resources.path('fithinator.static', 'FreeSans.ttf') as p:
            font_path = str(p)
        with importlib.resources.path('fithinator.static', 'FITH_Logo.jpg') as p:
            static_logo_path = str(p)
        with importlib.resources.path('fithinator.static', 'fith_rotate.gif') as p:
            anim_logo_path = str(p)

        self.font_size = font_size
        self.font_size_px = int(font_size * 1.33333333)
        self.font = ImageFont.truetype(font_path, self.font_size)

        self.anim_lastframe = (time.perf_counter_ns() / 1000000)
        self.anim_frametime = 0.0
        self.anim_refresh = 100.0  # ms, default frame duration
        self.fith_logo = ImageFile(static_logo_path)
        self.fith_anim = ImageFile(anim_logo_path)
        self.spinner = Spinner()
        self.lock = "\ua5c3"

        self.fps = 0
        self.frame_time = (time.perf_counter_ns() / 1000000)

        parser = cmdline.create_parser(description='FITHINATOR display args')
        try:
            with importlib.resources.path('fithinator.display_conf', f"{display}.conf") as p:
                conf = cmdline.load_config(str(p))
            args = parser.parse_args(conf)
        except FileNotFoundError:
            LOGGER.warning(f"{display}.conf not found, trying manual configuration")
            conf = [f'--display={display}']
            args = parser.parse_args(conf)

        self.device = cmdline.create_device(args)
        self.max_char = int(self.device.width // self.textsize("A")[0])



    def text_align_center(self, xy, bounds, message, fill="white"):
        bound_w = bounds[0]
        lines = message.split('\n')
        for i, line in enumerate(lines):
            if hasattr(self.draw, 'textsize'):
                w = self.draw.textsize(line, font=self.font)[0]
            else:
                w = self.draw.textlength(line, font=self.font)
            self.draw.text((xy[0] + ((bound_w - w) / 2), 
                            xy[1] + (self.font_size_px * i)),
                            line, 
                            fill = fill,
                            font=self.font)


    def write(self, output):
        with canvas(self.device) as self.draw:
            self.draw.text((0, 0), output, font=self.font)


    def write_quarters(self, ul=None, ur=None, ll=None, lr=None, spinner=False):
        with canvas(self.device) as self.draw:
            for q in ('ul', 'ur', 'll', 'lr'):
                self.quarter(q, eval(q))
            if spinner:
                self.draw.text((0, 0), self.spinner.render(), font=self.font)


    def quarter(self, quarter, output):
        half_x = int(self.device.width / 2)
        half_y = int(self.device.height / 2)
        bounds = (half_x, half_y)
        quarters = {'ul': (0, 0), 
                    'ur': (half_x, 0), 
                    'll': (0, half_y),
                    'lr': (half_x, half_y)}
        if quarter not in quarters.keys():
            raise ValueError(f"quarter must be one of {', '.join(quarters)}")

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


    def textsize(self, s):
        #return self.font.getsize(s)
        if hasattr(self.font, 'getbbox'):
            left, top, right, bottom = self.font.getbbox(s)
            return (right - left, bottom - top)
        else:
            return self.font.getsize(s)


    def grouper(self, iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)


    def wrapped(self, s, max):
        return "\n".join(textwrap.wrap(s, width=max))


    def display_summary(self, timeout, servers=None):
        if servers:
            self.servers = servers
        key_chunk = self.grouper(self.servers, 3)
        for chunk in key_chunk:
            q = []
            for server in chunk:
                if server == None:
                    output = " "
                else:
                    output = ""
                    target = server.name
                    if server.info == None:
                        output += f"{target}\nUPDATE FAILED\n\n"
                    else:
                        if server.info.password_protected:
                            locked = self.lock + " "
                        else:
                            locked = ""

                        map_array = server.info.map_name.split('_')
                        map_type_raw = map_array.pop(0)
                        try:
                            map_type = map_types[map_type_raw]
                        except (KeyError, IndexError):
                            map_type = map_type_raw

                        map_name = " ".join(map_array).title()

                        output += f"{target}\n"
                        output += f"{map_type}\n"
                        output += f"{self.wrapped(map_name, int(self.max_char // 2))}\n"
                        output += f"{locked}{server.info.player_count - server.info.bot_count}/{server.info.max_players} online\n\n"
                q.append(output)

            timeout_ns = timeout * 1000000000
            framecount = 0
            runtime = 0
            while runtime < timeout_ns:
                start_ns = time.perf_counter_ns()
                self.write_quarters( 
                    ul = q[0],
                    ur = q[1],
                    ll = q[2],
                    lr = self.fith_anim.render(),
                    spinner = False
                )
                end_ns = time.perf_counter_ns()
                runtime += (end_ns - start_ns)
                framecount += 1
                self.frame_time = time.perf_counter_ns() / 1000000
            fps = (framecount / (runtime / 1000000000))
            LOGGER.debug(f"fps: {fps}")


    def display_detail(self, timeout, servers=None):
        if servers:
            self.servers = servers
        for server in self.servers:
            target = server.name
            if server.info == None:
                body = f"{target}\nUPDATE FAILED\n\n"
            else:
                if server.info.password_protected:
                    locked = self.lock + " "
                else:
                    locked = ""

                body  = f"\n{self.wrapped(server.info.server_name, self.max_char)}\n"
                body += f"\n{self.wrapped(server.info.map_name, self.max_char)}\n"
                body += f"\n{locked}{server.info.player_count - server.info.bot_count}/{server.info.max_players} online\n\n"

            timeout_ns = timeout * 1000000000
            framecount = 0
            runtime = 0
            while runtime < timeout_ns:
                start_ns = time.perf_counter_ns()
                self.write_header_body(target, body)
                end_ns = time.perf_counter_ns()
                runtime += (end_ns - start_ns)
                framecount += 1
                self.frame_time = time.perf_counter_ns() / 1000000
            fps = (framecount / (runtime / 1000000000))
            LOGGER.debug(f"fps: {fps}")
