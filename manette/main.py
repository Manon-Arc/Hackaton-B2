import ubinascii
import time
import espnow
from machine import Pin, ADC
import network

CURRENT_MAC = "" #@"\xd8\xea\xd5\x10


JOYSTICK_X = ADC(Pin(35))
JOYSTICK_Y = ADC(Pin(34))

PIN_BTN_ACCESSOIRE = Pin(16, Pin.IN, Pin.PULL_UP)

JOYSTICK_X.atten(ADC.ATTN_11DB)
JOYSTICK_Y.atten(ADC.ATTN_11DB)

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_mac = wlan_sta.config('mac')
CURRENT_MAC = ubinascii.hexlify(wlan_mac).decode()
print(wlan_mac)

e = espnow.ESPNow()
e.active(True)

peer = b'0\xc6\xf70\x07\x98'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()

centerX = (1965,1995)
centerY = (1830,1855)

host, msg = e.recv()
if msg == b'PLEASE':  # msg == None if timeout in recv()
    print(host, msg)
    peer = host
    e.send(peer, "CONNECTED", True)
    
while True:

    if not PIN_BTN_ACCESSOIRE.value():
        print("btn appuyé")

    A = False
    R = False
    G = False
    D = False

    xValue = JOYSTICK_X.read()
    yValue = JOYSTICK_Y.read()

    if(xValue > 1995):
        A = True
    if(yValue > 1855):
        D = True
    if(yValue < 1830):
        G = True
    if(xValue < 1965):
        R = True

    if A:
        if D:
            e.send(peer, "DD", True)
        elif G:
            e.send(peer, "DG", True)
        else:
            e.send(peer, "A", True)
    elif R:
        if D:
            e.send(peer, "DD", True)
        elif G:
            e.send(peer, "DG", True)
        else:
            e.send(peer, "R", True)
    elif D:
        e.send(peer, "TD", True)
    elif G:
        e.send(peer, "TG", True)
    else:
        e.send(peer, "STOP", True)

    time.sleep(0.1)