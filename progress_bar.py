import palettes as p


def clamp(value, min_value, max_value):
    '''Clamps `value` to [`min_value`, `max_value`].'''
    return min(max_value, max(value, min_value))


def scale(target, value, min_value, max_value):
    '''Scales `value` to the range [0, `target`].'''
    target * ((value - min_value) / (max_value - min_value))


def full_monotone(sense, max_value=100, min_value=0, color=(255, 255, 255)):
    """
    Produces a function to set the LED matrix of the SenseHat specified by
    `sense` in the fashion of a progress bar where a `value` of `min_value` 
    turns off all the lights and a `value` of `max_value` turns on all the 
    lights. The produced progress bar function will set the LED matrix and 
    return a proprtion in the range [0,1].

    Example usage:
    `
    # create progress bar for temp in F, from freezing to boiling
    # with blue display
    bar1 = full_monotone(my_hat, 212, 32, (0, 0, 255))
    bar1(90)

    # red progress bar with values between 0 and 100
    bar2 = full_monotone(my_hat, color=(255, 0, 0))
    bar2(50)  # half of led matrix lit
    bar2(75)  # 75% of matrix lit
    bar2(105) # all leds lit. value is clamped to the min and max
    ` 
    """
    # scale max and min values to [0, whatever]
    value_adj = 0 - min_value
    min_value, max_value = min_value + value_adj, max_value + value_adj

    def func(value):
        value = value + value_adj  # scale input value to match max/min
        value = min(max_value, max(value, min_value))  # clamp value
        on, part = divmod(64 * value, max_value)  #scale value to num of leds
        part = part / max_value  # remake part as porportion
        on, off = int(on), int(64 - on)  #numer of pixels 100% on or off

        # calc the partially lit pixel's rgb values
        dim_color = tuple([int(c * part) for c in color])
        dim, off = (1, off - 1) if part else (0, off)  # need dim pix or not?

        # create list of 64 colors which will be used to set the led matrix
        data = [color] * on + [dim_color] * dim + [(0, 0, 0)] * off
        sense.set_pixels(data)

    return func


def set_row_palette(sense, row, palette):
    """Set's all the pixels in the given `row` (in [0,7]) to the colors 
    specified by `palette`."""
    pixels = sense.get_pixels()
    pixels = pixels[:8 * row] + palette + pixels[8 * row + 8:]
    sense.set_pixels(pixels)


def set_row_level(sense, row, level, palette=p.WHITE_SOLID):
    """Set's the `row`'s level (ie height) (in [0,8]), and also applies
    the specified `palette` to the row."""
    set_row_palette(sense, row, palette[:level] + [p.OFF] * (8 - level))


class Display(object):
    """
    A class to make accessing and manipulating the SenseHat's LED matrix
    more convenient. This class allows access to the LEDs as a set of rows from
    0 to 7, where each row has a particular level (ie height) and palette. A 
    row's level must be from 0 to 8, where 0 means no pixels in the row are lit,
    and 8 means all are lit. A row's palette is a list of 8 colors tuples 
    applied to the row.
    """

    class _Row:
        """Represents a row's data."""

        def __init__(self, level=0, palette=p.WHITE_SOLID):
            """Initialize the row."""
            self.level = level
            self.palette = palette

        # def _set_level(self, value):

        # level = property(_set_level, _get_level)
        # palette = property(_set_palette, _get_palette)

    def __init__(self, sense, palette=p.WHITE_SOLID):
        """Initiallizes the object with the given SenseHat() instance.
        Clear's the sense hat's LED matrix. Sets each row's `palette`."""
        self._sense = sense
        sense.clear()
        self._rows = [Display._Row(palette=palette) for i in range(8)]

    def __setitem__(self, row, value):
        """ Sets the row's level or palette depending on what type is `value`,
        then applies the change to the LED matrix, and stores the new value."""
        if isinstance(value, int):
            # set row's level
            self._rows[row].level = value
            set_row_level(self._sense, row, self._rows[row].level,
                          self._rows[row].palette)
        elif isinstance(value, list):
            # set row's palette
            self._rows[row].palette = value
            set_row_level(self._sense, row, self._rows[row].level,
                          self._rows[row].palette)
        elif isinstance(value, Display._Row):
            self[row] = value.level
            self[row] = value.palette

    def __getitem__(self, row):
        """Returns the `Display._Row` instance for the given row. Consider it
        READ ONLY."""
        return self._rows[row]  #self._rows[row].level, self._rows[row].palette


def spark_line(sense, max_value=100, min_value=0, palette=p.WHITE_SOLID):
    """
    Produces a function to use the SenseHat specified by `sense` as a 
    sparkline style graph. After initializing with an optional `max_value`, 
    `min_value`, and `palette`, use the resulting sparkline by passing
    values to it.

    Example:
    `
    # sparkline with default max/min and the green-red transitioning palette
    spark1 = spark_line(my_hat, palette=p.GR_SMOOTH)
    spark1(50) #row 0 of LED matrix has 4 leds lit
    spark1(100) #row 0 has 8 lit, row 1 has 4 lit
    ...
    spark(16) #row 0 has 1 lit, etc...
    `
    """
    d = Display(sense, palette)

    # scale max and min values to [0, whatever]
    value_adj = 0 - min_value
    min_value, max_value = min_value + value_adj, max_value + value_adj

    def func(value):
        value = value + value_adj  # scale input value to match max/min
        value = min(max_value, max(value, min_value))  # clamp value
        value = int(value * (8.0 / max_value))  # scale value to [0,8]

        # move every row's level over 1,
        # then set the scaled value to the new level of row 0
        for i in range(7, 0, -1):
            d[i] = d[i - 1].level
        d[0] = value

    return func


class MultiPoint(object):
    """
    This class allows tracking multiple 2-part data values. Add points with
    `add_point()` and supply data using `[]` and supplying the key for the
    point to be updated. The point will not appear on the LED matrix until data
    has been supplied at least once.
    """

    class _Point:
        """Holds data for a point on the LED matrix"""

        def __init__(self, color, x_extents, y_extents):
            self.x, self.y = None, None
            self.color = color
            self.x_min, self.x_max = x_extents
            self.y_min, self.y_max = y_extents

        def update(self, coord):
            x, y = coord
            x = clamp(x, self.x_min, self.x_max)  # clamp value
            y = clamp(y, self.y_min, self.y_max)

            #TODO refactor scaling
            self.x = int(scale(7, x, self.x_min, self.x_max))
            self.y = int(scale(7, y, self.y_min, self.y_max))

    def __init__(self, sense):
        self._sense = sense
        self._points = dict()

    def _clear_all(self):
        for pt in iter(self._points.values()):
            if pt.x and pt.y:
                self._sense.set_pixel(pt.x, pt.y, p.OFF)

    def _redraw_all(self):
        for pt in iter(self._points.values()):
            if pt.x and pt.y:
                self._sense.set_pixel(pt.x, pt.y, pt.color)

    def remove_point(self, key):
        """Deletes the point."""
        self._clear_all()
        self._points.pop(key)
        self._redraw_all()

    def add_point(self, key, color, x_extents=(0, 100), y_extents=(0, 100)):
        """Add a new data point to show. `color` should be a RGB 3-tuple."""
        self._points[key] = MultiPoint._Point(color, x_extents, y_extents)

    def _set_value(self, key, value):
        """Sets the value of a point. `value` must be a
        2-tuple of `(x, y)`."""
        self._clear_all()
        self._points[key].update(value)
        self._redraw_all()

    def __setitem__(self, key, value):
        """Allows the value of a point to be set using []. `value` must be a
        2-tuple of `(x, y)`."""
        self._set_value(key, value)
