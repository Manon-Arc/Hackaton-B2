import deplacements
import espnow
import network
import ubinascii
import sos


def Deplacements_Com(e):
    while True :
        mess = None
        host, mess = e.recv()
        print(host, mess)
        if mess == b'A' :
            deplacements.Avancer()
        elif mess == b'R' :
            deplacements.Reculer()
        elif mess == b'TD' :
            deplacements.Translation_D()
        elif mess == b'TG' :
            deplacements.Translation_G()
        elif mess == b'RD' :
            deplacements.Rotation_D()
        elif mess == b'RG' :
            deplacements.Rotation_G()
        elif mess == b'DD' :
            deplacements.D_D()
        elif mess == b'DG' :
            deplacements.D_G()
        elif mess == b'DBD':
            deplacements.D_B_D()
        elif mess == b'D_B_G':
            deplacements.D_B_G()
        elif mess == b'STOP':
            deplacements.Rien()