from machine import Pin
from time import sleep

motor1_step = Pin(17, Pin.OUT)
motor1_dir = Pin(19, Pin.OUT)
motor2_step = Pin(22, Pin.OUT)
motor2_dir = Pin(23, Pin.OUT)
Canon = Pin(25, Pin.OUT)


def angle_to_steps(angle):
    if angle < 0 or angle > 360:
        raise ValueError("Angle must be between 0 and 360 degrees")
    return int(angle * 200 / 360)


def move_motor(motor, steps, direction):
    if motor == 1:
        step_pin = motor1_step
        dir_pin = motor1_dir
    elif motor == 2:
        step_pin = motor2_step
        dir_pin = motor2_dir
    else:
        raise ValueError("Invalid motor number")

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
