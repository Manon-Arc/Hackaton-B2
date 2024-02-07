import machine
import time
import com

giro = machine.PWM(machine.Pin(25),freq=50)
led = machine.Pin(17, machine.Pin.OUT)
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
valeur = 0
    
    
def Giro_Com(e):
    while True :
        mess = None
        host, mess = e.recv()
        if mess == b'GIRO OFF':
            print("ok")
            led.value(0)
        elif mess == b'GIRO ON':
            print("qsdfghjk")
            led.value(1)
            giro.duty(26)
            time.sleep(0.3)
            giro.duty(123)
            time.sleep(0.3)
