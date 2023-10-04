from machine import Pin
from time import sleep

step_pin = Pin(17, Pin.OUT)
dir_pin = Pin(19, Pin.OUT)
Canon = Pin(25, Pin.OUT)


def angle_to_steps(angle):
    if angle < 0 or angle > 360:
        raise ValueError("Angle must be between 0 and 360 degrees")
    return int(angle * 200 / 360)


def move_motor(steps, direction):
    dir_pin.value(direction)
    for i in range(steps):
        step_pin.value(1)
        sleep(0.001)
        step_pin.value(0)
        sleep(0.001)


def canon():
    if Canon.value() == 0:
        Canon.value(1)
    else:
        Canon.value(0)
