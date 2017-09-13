import time
import math
from PIL import Image

import progress_bar as pg
import palettes as p


def show_cos(prog_bar, max, revs=2, delay=0.05):
    for r in (2 * math.pi * (i / 100.0) for i in range(int(revs * 100) + 1)):
        _ = prog_bar(-max * math.cos(r))
        time.sleep(delay)


class FakeHat:
    """Implements an interface similar to `SenseHat` but displays the LED
    matrix as an image using PIL. Only implements methods used in this
    library. Image displaying is slow and crappy, but works for testing."""

    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            self.clear()

    def clear(self):
        self.data = [p.OFF] * 64

    def set_pixels(self, data):
        self.data = data
        im = Image.new('RGB', (8, 8))
        im.putdata(data)
        im.show()

    def get_pixels(self):
        return self.data
