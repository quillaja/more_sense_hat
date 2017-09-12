OFF = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

WHITE_SOLID = [WHITE] * 8
RED_SOLID = [RED] * 8
GREEN_SOLID = [GREEN] * 8
BLUE_SOLID = [BLUE] * 8

GYR_SMOOTH = [(0, 255, 0), (85, 255, 0), (170, 255, 0), (255, 255, 0),
              (255, 192, 0), (255, 128, 0), (255, 64, 0), (255, 0, 0)]

GYR = [GREEN] * 3 + [YELLOW] * 2 + [RED] * 3

RYG_SMOOTH = GYR_SMOOTH[::-1]

RYG = GYR[::-1]

BR_SMOOTH = [(0, 0, 255), (85, 0, 255), (170, 0, 255), (255, 0, 255),
             (255, 0, 192), (255, 0, 128), (255, 0, 64), (255, 0, 0)]

BR = [BLUE] * 3 + [MAGENTA] * 2 + [RED] * 3

RB_SMOOTH = BR_SMOOTH[::-1]

RB = BR[::-1]
