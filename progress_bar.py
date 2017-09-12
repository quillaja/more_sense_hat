#from sense_hat import SenseHat
import palettes as p


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

        return value / max_value

    return func


def set_row_palette(sense, row, palette):
    pixels = sense.get_pixels()
    pixels = pixels[:8 * (row + 1)] + palette + pixels[8 * row + 8:]
    sense.set_pixels(pixels)


def set_row_level(sense, row, level, palette=p.WHITE_SOLID):
    set_row_palette(sense, row, palette[:level] + [p.OFF] * (8 - level))
