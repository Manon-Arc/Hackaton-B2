Utiliser ESPNOW

Connection depuis une ESP Tiers :

On initie ESPNOW pour on envoie une requête de connection à l'ESP principale possédant l'adresse mac **"\$MAC_ADRESSE$"**

L'adresse mac de notre ESP principale actuelle est : **@"\xd8\xea\xd5\x10**

```python
import espnow

def main():

    [...]

    e = espnow.ESPNow()
    e.active(True)

    IS_CONNECT = False

    while !IS_CONNECT:
        peer = b'$MAC_ADRESSE$'   # MAC address of peer's wifi interface
        e.add_peer(peer)      # Must add_peer() before send()
        e.send(peer, "PLEASE", True)
        host, msg = e.recv()
        if msg == b'CONNECTED':  # msg == None if timeout in recv()
            IS_CONNECT = True

    [...]

```

Avec ESPNOW on a la possibilité de transmettre une chaîne de caractères qui sera reçu sous la forme ***b'\$chaine_de_caractère$'***

Pour envoyer une chaîne de caractère à une ESP, on utilise :
```python

e = espnow.ESPNow()
e.active(True)
e.add_peer(b'$MAC_ADRESSE$')
e.send(b'$MAC_ADRESSE$', $chaîne_de_caractères$, True)

```

Pour recevoir et lire les données, l'ESP réceptrice doit utiliser ce code :
```python

e = espnow.ESPNow()
e.active(True)

host, msg = e.recv()

```

La variable host contient l'adresse mac de l'ESP qui envoie le message sous la forme ***b'\$MAC_ADRESSE$'***

La variable msg contient la chaîne de caractère envoyé par l'ESP sous la forme ***b'\$chaine_de_caractère$'***

### **ATTENTION**

La ligne e.recv() stop l'exécution du code jusqu'à reception d'un messsage !
