from machine import Pin
motor = Pin(16, Pin.OUT)

def launch_plot():
    if motor.value() == 1:
        motor.value(0)
    else:
        motor.value(1)
    
