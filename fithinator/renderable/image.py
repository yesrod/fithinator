import time
import logging
from PIL import Image
from fithinator.renderable import Renderable

LOGGER = logging.Logger(__name__)

class ImageFile(Renderable):
    """
    A representation of an image file and associated handles, functions, etc.
    """

    def __init__(
        self,
        path,
    ):
        self.path = path
        self._anim_lastframe = (time.perf_counter_ns() / 1000000)
        self._anim_frametime = 0.0
        self._anim_refresh = 100.0  # ms, default frame duration
        self._image = self._load_image(self.path)

    def _load_image(self, image_path):
        ret = Image.open(image_path)
        self.anim_refresh = ret.info.get("duration", 100.0)
        LOGGER.debug(f"{image_path} duration: {self._anim_refresh}")
        return ret

    def render(self):
        if hasattr(self._image, 'is_animated') and self._image.is_animated:
            now = (time.perf_counter_ns() / 1000000)
            self._anim_frametime += (now - self._anim_lastframe)
            while self._anim_frametime >= self._anim_refresh:
                try:
                    self._image.seek(self._image.tell() + 1)
                except EOFError:
                    self._image.seek(0)
                self._anim_frametime -= self._anim_refresh
            self._anim_lastframe = now
        return self._image
