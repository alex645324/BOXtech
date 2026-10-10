from signal import pause

from gpiozero import Button

BUTTON_PIN = 17

button = Button(BUTTON_PIN)


def on_hold(callback):
    button.when_pressed = callback


def on_release(callback):
    button.when_released = callback


def wait():
    pause()
