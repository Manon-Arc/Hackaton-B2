import espnow
import network
import ubinascii
import com
import com_deplacements
import phare
import sos
import _thread
import giro
import move_canon
import canon

e = com.Com()

IS_CONNECT = False
while not IS_CONNECT:
    print("Test")
    peer = b'@"\xd8\xea\xd5\x10'   # MAC address of peer's wifi interface
    e.add_peer(peer)      # Must add_peer() before send()
    e.send(peer, "PLEASE", True)
    host, msg = e.recv()
    if msg == b'CONNECTED':  # msg == None if timeout in recv()
        IS_CONNECT = True


_thread.start_new_thread(sos.Sos_Com,(e,))
_thread.start_new_thread(giro.Giro_Com,(e,))
_thread.start_new_thread(phare.Phare_Com,(e,))
_thread.start_new_thread(move_canon.move,(e,))
_thread.start_new_thread(canon.canon,(e,))
while True :
    com_deplacements.Deplacements_Com(e)
