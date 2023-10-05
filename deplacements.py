from machine import Pin
import machine

pin1_A = machine.PWM(machine.Pin(0),freq=50)
pin2_A = machine.PWM(machine.Pin(2),freq=50)
pin1_B = machine.PWM(machine.Pin(4),freq=50)
pin2_B = machine.PWM(machine.Pin(12),freq=50)
pin1_C = machine.PWM(machine.Pin(14),freq=50)
pin2_C = machine.PWM(machine.Pin(16),freq=50)
pin1_D = machine.PWM(machine.Pin(18),freq=50)
pin2_D = machine.PWM(machine.Pin(21),freq=50)
vitesse = 50


def Avancer():
    pin1_A.duty(int((vitesse/100)*1024))
    pin2_A.duty(0)
    pin1_B.duty(int((vitesse/100)*1024))
    pin2_B.duty(0)
    pin1_C.duty(0)
    pin2_C.duty(int((vitesse/100)*1024))
    pin1_D.duty(0)
    pin2_D.duty(int((vitesse/100)*1024))
    
def Reculer():
    pin1_A.duty(0)
    pin2_A.duty(int((vitesse/100)*1024))
    pin1_B.duty(0)
    pin2_B.duty(int((vitesse/100)*1024))
    pin1_C.duty(int((vitesse/100)*1024))
    pin2_C.duty(0)
    pin1_D.duty(int((vitesse/100)*1024))
    pin2_D.duty(0)

def Translation_G():
    pin1_A.duty(0)
    pin2_A.duty(int((vitesse/100)*1024))
    pin1_B.duty(0)
    pin2_B.duty(int((vitesse/100)*1024))
    pin1_C.duty(0)
    pin2_C.duty(int((vitesse/100)*1024))
    pin1_D.duty(0)
    pin2_D.duty(int((vitesse/100)*1024))
    
def Translation_D():
    pin1_A.duty(0)
    pin2_A.duty(int((vitesse/100)*1024))    
    pin1_B.duty(int((vitesse/100)*1024))
    pin2_B.duty(0)
    pin1_C.duty(0)
    pin2_C.duty(int((vitesse/100)*1024))    
    pin1_D.duty(int((vitesse/100)*1024))
    pin2_D.duty(0)
    
def Rotation_D():
    pin1_A.duty(int((vitesse/100)*1024))
    pin2_A.duty(0)
    pin1_B.duty(0)
    pin2_B.duty(int((vitesse/100)*1024))    
    pin1_C.duty(0)
    pin2_C.duty(int((vitesse/100)*1024))    
    pin1_D.duty(int((vitesse/100)*1024))
    pin2_D.duty(0)
    
def Rotation_G():
    pin1_A.duty(0)
    pin2_A.duty(int((vitesse/100)*1024))
    pin1_B.duty(int((vitesse/100)*1024))
    pin2_B.duty(0)
    pin1_C.duty(int((vitesse/100)*1024))
    pin2_C.duty(0)
    pin1_D.duty(0)
    pin2_D.duty(int((vitesse/100)*1024))

def D_D() :
    pin1_A.duty(int((vitesse/100)*1024))
    pin2_A.duty(0)
    pin1_B.duty(0)
    pin2_B.duty(0)   
    pin1_C.duty(0)
    pin2_C.duty(0)
    pin1_D.duty(0)
    pin2_D.duty(int((vitesse/100)*1024))
    
def D_G() :
    pin1_A.duty(0)
    pin1_A.duty(0)    
    pin1_B.duty(int((vitesse/100)*1024))
    pin2_B.duty(0)
    pin1_C.duty(0)
    pin2_C.duty(int((vitesse/100)*1024))
    pin1_D.duty(0)
    pin2_D.duty(0)
    
def Rien() :
    pin1_A.duty(0)
    pin2_A.duty(0)
    pin1_B.duty(0)
    pin2_B.duty(0)
    pin1_C.duty(0)
    pin2_C.duty(0)
    pin1_D.duty(0)
    pin2_D.duty(0)
    
def D_B_D():
    pin1_A.duty(0)
    pin1_A.duty(0)
    pin1_B.duty(0)
    pin2_B.duty(int((vitesse/100)*1024))    
    pin1_C.duty(0)
    pin2_C.duty(0)
    pin1_D.duty(int((vitesse/100)*1024))
    pin2_D.duty(0)
    
def D_B_G():
    pin1_A.duty(int((vitesse/100)*1024))
    pin2_A.duty(0)
    pin1_B.duty(0)
    pin2_B.duty(0)
    pin1_C.duty(int((vitesse/100)*1024))
    pin2_C.duty(0)
    pin1_D.duty(0)
    pin2_D.duty(0)

