from machine import Pin
from time import sleep

motor1_step = Pin(27, Pin.OUT)  # TODO: Change to correct pin
motor1_dir = Pin(26, Pin.OUT)  # TODO: Change to correct pin
# motor2_step = Pin(2, Pin.OUT)  # TODO: Change to correct pin
# motor2_dir = Pin(3, Pin.OUT)  # TODO: Change to correct pin


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
