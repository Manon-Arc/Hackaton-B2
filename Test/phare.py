from machine import Pin
import espnow
import network

def Phare_Com(e):
    while True :
        mess = None
        host, mess = e.recv()
        print(host, mess)
        if msg == b'PHARE ON':
            pin_led13 = Pin(13, mode=Pin.OUT, value=1) # Light on
        else :
            pin_led13 = Pin(13, mode=Pin.OUT, value=0) # Light off
