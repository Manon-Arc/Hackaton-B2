import deplacements
import espnow
import network
import ubinascii

def Com():
    CURRENT_MAC = ""
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    wlan_mac = wlan_sta.config('mac')
    CURRENT_MAC = ubinascii.hexlify(wlan_mac).decode()
    print(wlan_mac)

    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

    e = espnow.ESPNow()Com
    e.active(True)
    
    return e