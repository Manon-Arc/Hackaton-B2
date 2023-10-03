import time
import machine

broche_sortie = machine.Pin(4, machine.Pin.OUT)
pwm = machine.PWM(broche_sortie)


# Settings of short and long calls

short = 0.3 # Short, is egal to silence
long = 0.75

# Set spreader

pwm.duty(0)
time.sleep(short)

# S
pwm.duty(512) # Volume on
time.sleep(short)
pwm.duty(0) # Silence
broche_sortie.value(0) # Stop alim
time.sleep(short)
pwm.duty(512) 
time.sleep(short)
pwm.duty(0)
broche_sortie.value(0)
time.sleep(short)
pwm.duty(512)
time.sleep(short)
pwm.duty(0)
broche_sortie.value(0)
time.sleep(short)

# O
pwm.duty(512)
time.sleep(long)
pwm.duty(0)
broche_sortie.value(0)
time.sleep(short)
pwm.duty(512)
time.sleep(long)
pwm.duty(0)
broche_sortie.value(0)
time.sleep(short)
pwm.duty(512)
time.sleep(long)
pwm.duty(0)
broche_sortie.value(0)
time.sleep(short)

# S
pwm.duty(512)
time.sleep(short)
pwm.duty(0)
broche_sortie.value(0)
time.sleep(short)
pwm.duty(512)
time.sleep(short)
pwm.duty(0)
broche_sortie.value(0)
time.sleep(short)
pwm.duty(512)
time.sleep(short)
pwm.duty(0)
broche_sortie.value(0)
time.sleep(short)
