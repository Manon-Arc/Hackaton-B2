from machine import Pin
import espnow
import network


def main():
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

    while True:
        print("t")
        host, msg = e.recv()
        print(msg)
        if msg == b'PHARE ON':
            pin_led13 = Pin(13, mode=Pin.OUT, value=1) # Light on
        else :
            pin_led13 = Pin(13, mode=Pin.OUT, value=0) # Light off

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_mac = wlan_sta.config('mac')
print(wlan_mac)

main()
