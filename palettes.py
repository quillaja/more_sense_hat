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

BRIGHTER = [(a, a, a) for a in range(32, 256, 32)] + [WHITE]
DIMMER = BRIGHTER[::-1]

GR_SMOOTH = [(0, 255, 0), (85, 255, 0), (170, 255, 0), (255, 255, 0),
             (255, 192, 0), (255, 128, 0), (255, 64, 0), (255, 0, 0)]
RG_SMOOTH = GR_SMOOTH[::-1]

GR = [GREEN] * 3 + [YELLOW] * 2 + [RED] * 3
RG = GR[::-1]

BR_SMOOTH = [(0, 0, 255), (85, 0, 255), (170, 0, 255), (255, 0, 255),
             (255, 0, 192), (255, 0, 128), (255, 0, 64), (255, 0, 0)]
RB_SMOOTH = BR_SMOOTH[::-1]

BR = [BLUE] * 3 + [MAGENTA] * 2 + [RED] * 3
RB = BR[::-1]

BG_SMOOTH = [(0, 0, 255), (0, 85, 255), (0, 170, 255), (0, 255, 255),
             (0, 255, 192), (0, 255, 128), (0, 255, 64), (0, 255, 0)]
GB_SMOOTH = BG_SMOOTH[::-1]

BG = [BLUE] * 3 + [CYAN] * 2 + [GREEN] * 3
GB = BG[::-1]

BGR_SMOOTH = [(0, 0, 255), (0, 64, 192), (0, 128, 128), (0, 192, 64),
              (0, 255, 0), (90, 180, 0), (180, 90, 0), (255, 0, 0)]
RGB_SMOOTH = BGR_SMOOTH[::-1]

BGR = [BLUE, BLUE, CYAN, GREEN, GREEN, YELLOW, YELLOW, RED]
RGB = BGR[::-1]