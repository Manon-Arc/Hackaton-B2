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

def sos():
    
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


def main():
    pwm.duty(0)
    e = espnow.ESPNow()
    e.active(True)

    IS_CONNECT = False

    while not IS_CONNECT:
        peer = b'@"\xd8\xea\xd5\x10'   # MAC address of peer's wifi interface
        e.add_peer(peer)      # Must add_peer() before send()
        e.send(peer,"PLEASE", True) #Erreur
        host, msg = e.recv()
        if msg == b'CONNECTED':  # msg == None if timeout in recv()
            IS_CONNECT = True
    #Set spreader
    
    while True:
        print("t")
        host, msg = e.recv()
        print(msg)
        if msg == b'SOS':
            sos()
        else :
            pwm.duty(0)

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_mac = wlan_sta.config('mac')
print(wlan_mac)

main()
