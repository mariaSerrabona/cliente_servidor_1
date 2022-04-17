# multiconn-server.py

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

# ...

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")

#con esta diferencia, el servidor no se podrá bloquear
lsock.setblocking(False)

#con el data de esta función, se almacenará toda la información con el socket
sel.register(lsock, selectors.EVENT_READ, data=None)