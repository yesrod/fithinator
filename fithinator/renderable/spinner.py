from fithinator.renderable import Renderable


class Spinner(Renderable):
    """
    A text-based spinning icon, just to show screen refresh is working
    """

    def __init__(self,
        spinner_chars = ('|', '/', '-', '\\'),
        frame_delay = 1
    ):
        self.spinner_chars = spinner_chars
        self.frame_delay = frame_delay
        self._spinner_state = 0

    def render(self):
        if self._spinner_state > len(self.spinner_chars):
            self._spinner_state = 0
        ret = self.spinner_chars[self._spinner_state]
        self._spinner_state += 1
        return ret
