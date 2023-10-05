import time
import machine
import espnow
import network

broche_sortie = machine.Pin(13, machine.Pin.OUT)
pwm = machine.PWM(broche_sortie)


# Settings of short and long calls
song=512  #512 origine
short = 0.3  # is egal to silence
long = 0.75

def Sos():
    
    pwm.duty(0)
    time.sleep(short)
    # S
    pwm.duty(song) # Volume on
    time.sleep(short)
    pwm.duty(0) # Silence
    broche_sortie.value(0) # Stop alim
    time.sleep(short)
    pwm.duty(song) 
    time.sleep(short)
    pwm.duty(0)
    broche_sortie.value(0)
    time.sleep(short)
    pwm.duty(song)
    time.sleep(short)
    pwm.duty(0)
    broche_sortie.value(0)
    time.sleep(short)

    # O
    pwm.duty(song)
    time.sleep(long)
    pwm.duty(0)
    broche_sortie.value(0)
    time.sleep(short)
    pwm.duty(song)
    time.sleep(long)
    pwm.duty(0)
    broche_sortie.value(0)
    time.sleep(short)
    pwm.duty(song)
    time.sleep(long)
    pwm.duty(0)
    broche_sortie.value(0)
    time.sleep(short)

    # S
    pwm.duty(song)
    time.sleep(short)
    pwm.duty(0)
    broche_sortie.value(0)
    time.sleep(short)
    pwm.duty(song)
    time.sleep(short)
    pwm.duty(0)
    broche_sortie.value(0)
    time.sleep(short)
    pwm.duty(song)
    time.sleep(short)
    pwm.duty(0)
    broche_sortie.value(0)
    time.sleep(short)
    
def Sos_Com(e):
    while True :
        pwm.duty(0)
        mess = None
        host, mess = e.recv()
        print(host, mess)
        if mess == b'SOS':
            sos.Sos()
        else :
            pwm.duty(0)
    
