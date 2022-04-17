# multiconn-client.py

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]

#num_conns número de conexiones que se tienen
def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)

        #para no intervenir en la conexión, se emplea connect_ex
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        #del mismo modo, la info que se quiere mandar, se almacena en un SimpleNamespace
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            #mensaje que el cliente manda al servidor
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)
