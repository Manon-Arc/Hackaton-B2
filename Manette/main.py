import time
import espnow
from machine import Pin, ADC
import network
import _thread

# @"\xd8\xea\xd5\x10
GYRO_STATUS = "OFF"

GYRO_IS_CLICK = False

LAST_CANON_MOUVEMENT = "STOP"

peer = ""

IS_CONNECT = False

# PIN_BTN_ACCESSOIRE = Pin(16, Pin.IN, Pin.PULL_UP)

PIN_INTERRUPT_GIRO = Pin(19, Pin.IN, Pin.PULL_UP)
# PIN_INTERRUPT_GIRO2 = Pin(17, Pin.IN, value=0)
# PIN_INTERRUPT_GIRO2.value(0)

JOYSTICK_X = ADC(Pin(35))
JOYSTICK_Y = ADC(Pin(34))

JOYSTICK_X.atten(ADC.ATTN_11DB)
JOYSTICK_Y.atten(ADC.ATTN_11DB)

PIN_BTN_ROTATION_GAUCHE = Pin(12, Pin.IN, Pin.PULL_UP)
PIN_BTN_ROTATION_DROITE = Pin(13, Pin.IN, Pin.PULL_UP)

PIN_BTN_CANON_UP = Pin(27, Pin.IN, Pin.PULL_UP)
PIN_BTN_CANON_DOWN = Pin(14, Pin.IN, Pin.PULL_UP)

# PIN_BTN_CANON_TIR = Pin(23, Pin.IN, Pin.PULL_UP)
# PIN_BTN_PLOT = Pin(26, Pin.IN, Pin.PULL_UP)

COMMUNICATION = espnow.ESPNow()
COMMUNICATION.active(True)

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_mac = wlan_sta.config('mac')


# print(wlan_mac)


# def listen(i):
#    global peer
#    global IS_CONNECT
#    while True:
#        host, msg = COMMUNICATION.recv()
#        if msg == b'PLEASE':  # msg == None if timeout in recv()
#            print(host, msg)
#            peer = host
#            try:
#                COMMUNICATION.add_peer(peer)
#            except:
#                pass
#            COMMUNICATION.send(peer, "CONNECTED", True)
#            IS_CONNECT = True
#        elif msg == b'ARE YOU HERE':
#            COMMUNICATION.send(peer, "YES I AM", True)

def a_wait_connection():
    global IS_CONNECT
    global peer

    while not IS_CONNECT:
        print("Waiting...")
        host, msg = COMMUNICATION.recv(100)
        if msg == b'PLEASE':
            peer = host
            try:
                COMMUNICATION.add_peer(peer)
                IS_CONNECT = True
                COMMUNICATION.send(peer, "CONNECTED", True)
                print("Marcus Connected")
            except OSError as err:
                print(f"!! WARNING !!\n\n{err}\n\n !! END WARNING !!")
        else:
            print("Try new connection")


def main():
    global IS_CONNECT, GYRO_IS_CLICK, GYRO_STATUS, LAST_CANON_MOUVEMENT
    a_wait_connection()

    _thread.start_new_thread(t_joystick, (0,))

    while IS_CONNECT:
        if PIN_INTERRUPT_GIRO.value():
            if not GYRO_IS_CLICK:
                GYRO_IS_CLICK = True
                if GYRO_STATUS != "ON":
                    COMMUNICATION.send(peer, "GIRO ON", True)
                    GYRO_STATUS = "ON"
                    print("GYRO ON")
                else:
                    COMMUNICATION.send(peer, "GIRO OFF", True)
                    GYRO_STATUS = "OFF"
                    print("GYRO OFF  ")
        else:
            GYRO_IS_CLICK = False


        if not PIN_BTN_CANON_UP.value():
            if LAST_CANON_MOUVEMENT != "UP":
                print("canon up start")
                COMMUNICATION.send(peer, "UP Start", True)
                LAST_CANON_MOUVEMENT = "UP"
        else:
            if LAST_CANON_MOUVEMENT != "STOP":
                print("canon up stop")
                COMMUNICATION.send(peer, "UP Stop", True)
                LAST_CANON_MOUVEMENT = "STOP"

        if not PIN_BTN_CANON_DOWN.value():
            if LAST_CANON_MOUVEMENT != "DOWN":
                print("Canon down start")
                COMMUNICATION.send(peer, "DOWN Start", True)
                LAST_CANON_MOUVEMENT = "DOWN"
        else:
            if LAST_CANON_MOUVEMENT != "STOP":
                print("canon down stop")
                COMMUNICATION.send(peer, "DOWN Stop", True)
                LAST_CANON_MOUVEMENT = "STOP"

        if not PIN_BTN_ROTATION_GAUCHE.value():
            print("rotation gauche")
            COMMUNICATION.send(peer, "RG", True)

        if not PIN_BTN_ROTATION_DROITE.value():
            print("rotation droite")
            COMMUNICATION.send(peer, "RD", True)

        time.sleep(0.3)

    main()


def treat_joystick_pos(x, y):
    centerX = (1900, 1975)
    centerY = (1850, 1925)

    R = x < centerX[0]
    D = y < centerY[0]
    G = y > centerY[1]
    A = x > centerX[1]

    if A:
        if D:
            return "DAD"

        elif G:
            return "DAG"

        else:
            return "A"

    elif R:
        if D:
            return "DBD"

        elif G:
            return "DBG"

        else:
            return "R"

    elif D:
        return "TD"

    elif G:
        return "TG"

    else:
        return "STOP"


def t_joystick(i):
    global IS_CONNECT

    while IS_CONNECT:
        LAST_DIR = "STOP"

        # centerX = (1900, 1975)
        # centerY = (1850, 1925)

        # A = False
        # R = False
        # G = False
        # D = False
        yValue = JOYSTICK_X.read()
        xValue = JOYSTICK_Y.read()

        # if (xValue < centerX[0]):
        #    R = True
        # if (yValue < centerY[0]):
        #    D = True
        # if (yValue > centerY[1]):
        #    G = True
        # if (xValue > centerX[1]):
        #    A = True
        C_DIR = treat_joystick_pos(xValue, yValue)
        if C_DIR != LAST_DIR:
            COMMUNICATION.send(peer, C_DIR, True)
            LAST_DIR = C_DIR

        # if A:
        #    if D:
        #        if LAST_DIR != "DAD":
        #            COMMUNICATION.send(peer, "DAD", True)
        #            print("DD")
        #            LAST_DIR = "DAD"

        #    elif G:
        #        if LAST_DIR != "DAG":
        #            COMMUNICATION.send(peer, "DAG", True)
        #            print("DG")
        #            LAST_DIR = "DAG"

        #    else:
        #        if LAST_DIR != "A":
        #            COMMUNICATION.send(peer, "A", True)
        #            print("A")
        #            LAST_DIR = "A"

        # elif R:
        #    if D:
        #        if LAST_DIR != "DBD":
        #            COMMUNICATION.send(peer, "DBD", True)
        #            print("DBD")
        #            LAST_DIR = "DBD"

        #    elif G:
        #        if LAST_DIR != "DBG":
        #            COMMUNICATION.send(peer, "DBG", True)
        #            print("DBG")
        #            LAST_DIR = "DBG"

        #    else:
        #        if LAST_DIR != "R":
        #            COMMUNICATION.send(peer, "R", True)
        #            print("R")
        #            LAST_DIR = "R"

        # elif D:
        #    if LAST_DIR != "TD":
        #        COMMUNICATION.send(peer, "TD", True)
        #        print("TD")
        #        LAST_DIR = "TD"

        # elif G:
        #    if LAST_DIR != "TG":
        #        COMMUNICATION.send(peer, "TG", True)
        #        print("TG")
        #        LAST_DIR = "TG"

        # else:
        #    if LAST_DIR != "STOP":
        #        COMMUNICATION.send(peer, "STOP", True)
        #        LAST_DIR = "STOP"
        #        print("STOP")


main()
