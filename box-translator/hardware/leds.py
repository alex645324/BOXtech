import time

from apa102_pi.driver import apa102

NUM_LEDS = 3

RED = (255, 0, 0)
GREEN = (0, 255, 0)
AMBER = (255, 126, 0)
BLUE = (0, 0, 255)
OFF = (0, 0, 0)

strip = apa102.APA102(num_led=NUM_LEDS)


def _set_all(color):
    red, green, blue = color
    for i in range(NUM_LEDS):
        strip.set_pixel(i, red, green, blue)
    strip.show()


def idle():
    _set_all(RED)


def listening():
    _set_all(GREEN)


def working():
    _set_all(AMBER)


def speaking():
    _set_all(BLUE)


def error():
    for _ in range(3):
        _set_all(RED)
        time.sleep(0.2)
        _set_all(OFF)
        time.sleep(0.2)
