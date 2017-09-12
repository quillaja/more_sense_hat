import time
import math

import progress_bar as pg


def show_cos(prog_bar, max, revs=2, delay=0.05):
	for r in (2*math.pi*(i/100.0) for i in range(int(revs*100)+1)):
		_ = prog_bar(-max*math.cos(r))
		time.sleep(delay)

