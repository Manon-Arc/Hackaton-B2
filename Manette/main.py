import time
import espnow
from machine import Pin, ADC
import network
import _thread

# @"\xd8\xea\xd5\x10

LAST_DIR = "STOP"
GYRO_STATUS = "OFF"

peer=""

IS_CONNECT = False

PIN_BTN_ACCESSOIRE = Pin(16, Pin.IN, Pin.PULL_UP)

PIN_INTERRUPT_GIRO = Pin(19, Pin.OUT, value=1)
PIN_INTERRUPT_GIRO2 = Pin(17, Pin.IN, value=0)
PIN_INTERRUPT_GIRO2.value(0)

JOYSTICK_X = ADC(Pin(35))
JOYSTICK_Y = ADC(Pin(34))

JOYSTICK_X.atten(ADC.ATTN_11DB)
JOYSTICK_Y.atten(ADC.ATTN_11DB)

PIN_BTN_ROTATION_GAUCHE = Pin(12, Pin.IN, Pin.PULL_UP)
PIN_BTN_ROTATION_DROITE = Pin(13, Pin.IN, Pin.PULL_UP)

PIN_BTN_CANON_UP = Pin(27, Pin.IN, Pin.PULL_UP)
PIN_BTN_CANON_DOWN = Pin(14, Pin.IN, Pin.PULL_UP)

PIN_BTN_CANON_TIR = Pin(23, Pin.IN, Pin.PULL_UP)
PIN_BTN_PLOT = Pin(26, Pin.IN, Pin.PULL_UP)

COMMUNICATION = espnow.ESPNow()
COMMUNICATION.active(True)

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_mac = wlan_sta.config('mac')
print(wlan_mac)



def listen(i):
    global peer
    global IS_CONNECT
    while True:
        host, msg = COMMUNICATION.recv()
        if msg == b'PLEASE':  # msg == None if timeout in recv()
            print(host, msg)
            peer = host
            try:
                COMMUNICATION.add_peer(peer)
            except:
                pass
            COMMUNICATION.send(peer, "CONNECTED", True)
            IS_CONNECT = True
        elif msg == b'ARE YOU HERE':
            COMMUNICATION.send(peer, "YES I AM", True)

_thread.start_new_thread(listen, (0,))

while not IS_CONNECT:
    pass

while True:
    centerX = (1880, 1990)
    centerY = (1830, 1940)

    A = False
    R = False
    G = False
    D = False
    yValue = JOYSTICK_X.read()
    xValue = JOYSTICK_Y.read()

    if (xValue > centerX[1]):
        R = True
    if (yValue > centerY[1]):
        D = True
    if (yValue < centerY[0]):
        G = True
    if (xValue < centerX[0]):
        A = True

    if A:
        if D:
            if LAST_DIR != "DAD":
                COMMUNICATION.send(peer, "DAD", True)
                print("DD")
                LAST_DIR = "DAD"

        elif G:
            if LAST_DIR != "DAG":
                COMMUNICATION.send(peer, "DAG", True)
                print("DG")
                LAST_DIR = "DAG"

        else:
            if LAST_DIR != "A":
                COMMUNICATION.send(peer, "A", True)
                print("A")
                LAST_DIR = "A"

    elif R:
        if D:
            if LAST_DIR != "DBD":
                COMMUNICATION.send(peer, "DBD", True)
                print("DBD")
                LAST_DIR = "DBD"

        elif G:
            if LAST_DIR != "DBG":
                COMMUNICATION.send(peer, "DBG", True)
                print("DBG")
                LAST_DIR = "DBG"

        else:
            if LAST_DIR != "R":
                COMMUNICATION.send(peer, "R", True)
                print("R")
                LAST_DIR = "R"

    elif D:
        if LAST_DIR != "TD":
            COMMUNICATION.send(peer, "TD", True)
            print("TD")
            LAST_DIR = "TD"

    elif G:
        if LAST_DIR != "TG":
            COMMUNICATION.send(peer, "TG", True)
            print("TG")
            LAST_DIR = "TG"

    else:
        if LAST_DIR != "STOP":
            COMMUNICATION.send(peer, "STOP", True)
            LAST_DIR = "STOP"
            print("STOP")

    # if not PIN_BTN_ACCESSOIRE.value():
    #    print("btn sos")
    #    COMMUNICATION.send(peer, "SOS", True)

    if PIN_INTERRUPT_GIRO2.value():
        if GYRO_STATUS != "ON":
            COMMUNICATION.send(peer, "GIRO ON", True)
            GYRO_STATUS = "ON"
            print("GYRO ON")
    else:
        if GYRO_STATUS != "OFF":
            COMMUNICATION.send(peer, "GIRO OFF", True)
            GYRO_STATUS = "OFF"
            print("GYRO OFF  ")

    # if not PIN_BTN_CANON_TIR.value():
    #    print("tir")
    #    COMMUNICATION.send(peer, "TIR", True)
    # else:
    #    COMMUNICATION.send(peer, "STOP TIR", True)

    # if not PIN_BTN_PLOT.value():
    #    print("plot")
    #    kill = True
    #    COMMUNICATION.send(peer, "PLOT", True)

    # if not PIN_BTN_CANON_UP.value():
    #    print("canon up")
    #    COMMUNICATION.send(peer, "UP", True)
    # if not PIN_BTN_CANON_DOWN.value():
    #    print("Canon down")
    #    COMMUNICATION.send(peer, "DOWN", True)

    if not PIN_BTN_ROTATION_GAUCHE.value():
        print("rotation gauche")
        COMMUNICATION.send(peer, "RG", True)

    if not PIN_BTN_ROTATION_DROITE.value():
        print("rotation droite")
        COMMUNICATION.send(peer, "RD", True)

    time.sleep(0.3)




