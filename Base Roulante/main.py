import espnow
import network
import ubinascii
import _thread
import time

# Variable de mise en Place
IS_CONNECT = False
REMOTE_MAC_ADDRESS = b'@"\xd8\xea\xd5\x10'

# Variable d'états
CURRENT_MOVEMENT = "STOP"
WHEEL_SPEED = 50
IS_GIRO_ON = False
IS_CANON_SHOOTING = False
IS_PHARE_ON = False
IS_CANON_UPING = False
IS_CANON_DOWNING = False

# Variable de liaisons machine
GYROPHARE_MOTOR = machine.PWM(machine.Pin(25), freq=50)
GYROPHARE_LED = machine.Pin(33, machine.Pin.OUT)

CANON = machine.Pin(32, machine.Pin.OUT)

ROUE_AVANT_GAUCHE = (machine.PWM(machine.Pin(17), freq=50), machine.PWM(machine.Pin(5), freq=50))
ROUE_AVANT_DROIT = (machine.PWM(machine.Pin(4), freq=50), machine.PWM(machine.Pin(16), freq=50))
ROUE_ARRIERE_GAUCHE = (machine.PWM(machine.Pin(18), freq=50), machine.PWM(machine.Pin(19), freq=50))
ROUE_ARRIERE_DROIT = (machine.PWM(machine.Pin(2), freq=50), machine.PWM(machine.Pin(0), freq=50))



#              --------------------         Recheck
step_pin = Pin(23, Pin.OUT)
dir_pin = Pin(22, Pin.OUT)

PHARE = machine.Pin(13, mode=machine.Pin.OUT)


# Activation ESP-NOW + WLAN (Nécessaire pour ESP-NOW)
wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_mac = wlan_sta.config('mac')

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
e.active(True)


def main():
    global CURRENT_MOVEMENT, IS_GIRO_ON, IS_CANON_SHOOTING, IS_PHARE_ON, IS_CANON_UPING, IS_CANON_DOWNING

    _thread.start_new_thread(t_deplacements, (0,))
    _thread.start_new_thread(t_giro, (0,))
    _thread.start_new_thread(t_canon, (0,))


    try:
        e.add_peer(REMOTE_MAC_ADDRESS)
    except OSError as err:
        print(f"!! WARNING !!\n\n{err}\n\n !! END WARNING !!")

    a_wait_connection()

    while True:
        host, msg = e.recv()
        if msg == b'A':
            CURRENT_MOVEMENT = "A"
        elif msg == b'R':
            CURRENT_MOVEMENT = "R"
        elif msg == b'TD':
            CURRENT_MOVEMENT = "TD"
        elif msg == b'TG':
            CURRENT_MOVEMENT = "TG"
        elif msg == b'RD':
            CURRENT_MOVEMENT = "RD"
        elif msg == b'RG':
            CURRENT_MOVEMENT = "RG"
        elif msg == b'DAD':
            CURRENT_MOVEMENT = "DAD"
        elif msg == b'DAG':
            CURRENT_MOVEMENT = "DAG"
        elif msg == b'DBD':
            CURRENT_MOVEMENT = "DBD"
        elif msg == b'DBG':
            CURRENT_MOVEMENT = "DBG"
        elif msg == b'STOP':
            CURRENT_MOVEMENT = "STOP"
        elif msg == b'GIRO OFF':
            IS_GIRO_ON = False
        elif msg == b'GIRO ON':
            IS_GIRO_ON = True

        elif msg == b'UP Start':
            IS_CANON_DOWNING = False
            IS_CANON_UPING = True
        elif msg == b'UP Stop':
            IS_CANON_UPING = False
        elif msg == b'DOWN Start':
            IS_CANON_UPING = False
            IS_CANON_DOWNING = True
        elif msg == b'DOWN Stop':
            IS_CANON_DOWNING = False



        elif msg == b'TIR':
            IS_CANON_SHOOTING = True
        elif msg == b'STOP TIR':
            IS_CANON_SHOOTING = False
        elif msg == b'PHARE ON':
            IS_PHARE_ON = True
        elif msg == b'PHARE OFF':
            IS_PHARE_ON = False

        else:
            pass




def a_wait_connection():
    global IS_CONNECT
    while not IS_CONNECT:
        print("Waiting...")
        e.send(REMOTE_MAC_ADDRESS, "PLEASE", True)
        host, msg = e.recv(100)
        if msg == b'CONNECTED' and host == REMOTE_MAC_ADDRESS:  # msg == None if timeout in recv()
            IS_CONNECT = True
            print("Remote Connected")
        else:
            print(host + " not equal to " + REMOTE_MAC_ADDRESS)
            print("Try new connection")


def t_giro(i):
    while True:
        if IS_GIRO_ON:
            GYROPHARE_LED.value(1)
            GYROPHARE_MOTOR.duty(26)
            time.sleep(0.3)
            GYROPHARE_MOTOR.duty(123)
            time.sleep(0.3)
        else:
            GYROPHARE_LED.value(0)

def t_deplacements(i):
    while True:
        if CURRENT_MOVEMENT == "A":
            avancer()
        elif CURRENT_MOVEMENT == "R":
            reculer()
        elif CURRENT_MOVEMENT == "TD":
            translation_droite()
        elif CURRENT_MOVEMENT == "TG":
            translation_gauche()
        elif CURRENT_MOVEMENT == "RD":
            rotation_horaire()
        elif CURRENT_MOVEMENT == "RG":
            rotation_antihoraire()
        elif CURRENT_MOVEMENT == "DAD":
            diagonale_avant_droit()
        elif CURRENT_MOVEMENT == "DAG":
            diagonale_avant_gauche()
        elif CURRENT_MOVEMENT == "DBD":
            diagonale_arriere_droit()
        elif CURRENT_MOVEMENT == "DBG":
            diagonale_arriere_gauche()
        elif CURRENT_MOVEMENT == "STOP":
            arret()
        else:
            arret()


def angle_to_steps(angle):
    max_angle = 0
    min_angle = 0
    if angle < 0 or angle > 360:
        raise ValueError("Angle must be between 0 and 360 degrees")
    print(angle)
    return int(angle * 200 / 360)


def move_motor(steps, direction):
    dir_pin.value(direction)
    for i in range(steps):
        step_pin.value(1)
        sleep(0.001)
        step_pin.value(0)
        sleep(0.001)


def t_canon(i):
    while True:
        #if IS_CANON_SHOOTING:
        #    CANON.value(1)
        #else:
        #    CANON.value(0)
        if IS_CANON_UPING:
            move_motor(angle_to_steps(1), True)
        elif IS_CANON_DOWNING:
            move_motor(angle_to_steps(1), False)

def t_phare(i):
    while True:
        if IS_PHARE_ON:
            PHARE.value(1)
        else:
            PHARE.value(0)


def wheel_forward(wheel):
    wheel[0].duty(int((WHEEL_SPEED / 100) * 1024))
    wheel[1].duty(0)


def wheel_backward(wheel):
    wheel[0].duty(0)
    wheel[1].duty(int((WHEEL_SPEED / 100) * 1024))


def wheel_stop(wheel):
    wheel[0].duty(0)
    wheel[1].duty(0)


def avancer():
    wheel_forward(ROUE_AVANT_GAUCHE)
    wheel_forward(ROUE_AVANT_DROIT)
    wheel_forward(ROUE_ARRIERE_GAUCHE)
    wheel_forward(ROUE_ARRIERE_DROIT)


def reculer():
    wheel_backward(ROUE_AVANT_GAUCHE)
    wheel_backward(ROUE_AVANT_DROIT)
    wheel_backward(ROUE_ARRIERE_GAUCHE)
    wheel_backward(ROUE_ARRIERE_DROIT)


def translation_gauche():
    wheel_backward(ROUE_AVANT_GAUCHE)
    wheel_forward(ROUE_AVANT_DROIT)
    wheel_forward(ROUE_ARRIERE_GAUCHE)
    wheel_backward(ROUE_ARRIERE_DROIT)


def translation_droite():
    wheel_forward(ROUE_AVANT_GAUCHE)
    wheel_backward(ROUE_AVANT_DROIT)
    wheel_backward(ROUE_ARRIERE_GAUCHE)
    wheel_forward(ROUE_ARRIERE_DROIT)


def rotation_horaire():
    wheel_forward(ROUE_AVANT_GAUCHE)
    wheel_backward(ROUE_AVANT_DROIT)
    wheel_forward(ROUE_ARRIERE_GAUCHE)
    wheel_backward(ROUE_ARRIERE_DROIT)


def rotation_antihoraire():
    wheel_backward(ROUE_AVANT_GAUCHE)
    wheel_forward(ROUE_AVANT_DROIT)
    wheel_backward(ROUE_ARRIERE_GAUCHE)
    wheel_forward(ROUE_ARRIERE_DROIT)


def diagonale_avant_gauche():
    wheel_stop(ROUE_AVANT_GAUCHE)
    wheel_forward(ROUE_AVANT_DROIT)
    wheel_forward(ROUE_ARRIERE_GAUCHE)
    wheel_stop(ROUE_ARRIERE_DROIT)


def diagonale_avant_droit():
    wheel_forward(ROUE_AVANT_GAUCHE)
    wheel_stop(ROUE_AVANT_DROIT)
    wheel_stop(ROUE_ARRIERE_GAUCHE)
    wheel_forward(ROUE_ARRIERE_DROIT)


def diagonale_arriere_gauche():
    wheel_stop(ROUE_AVANT_GAUCHE)
    wheel_backward(ROUE_AVANT_DROIT)
    wheel_backward(ROUE_ARRIERE_GAUCHE)
    wheel_stop(ROUE_ARRIERE_DROIT)


def diagonale_arriere_droit():
    wheel_backward(ROUE_AVANT_GAUCHE)
    wheel_stop(ROUE_AVANT_DROIT)
    wheel_stop(ROUE_ARRIERE_GAUCHE)
    wheel_backward(ROUE_ARRIERE_DROIT)


def arret():
    wheel_stop(ROUE_AVANT_GAUCHE)
    wheel_stop(ROUE_AVANT_DROIT)
    wheel_stop(ROUE_ARRIERE_GAUCHE)
    wheel_stop(ROUE_ARRIERE_DROIT)


main()
