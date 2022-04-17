# multiconn-server.py

import sys
import socket
import selectors
import types

#DEFINIMOS LAS FUNCIONES:

def accept_wrapper(sock):

    #para poner el socket en un modo de no-bloqueo
    #si se bloqueara, el servidor se conelaría hasta obtener una respuesta del cleinte, dejando de lado otros posibles sockets que se pueden crear
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)

    #creamos un objeto para mantener la información que se le quiere pasar al cliente
    #previamente, necesitamos saber que el servidor está listo para leer y escribir info
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)




def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    #si el socket está listo para leer, entonces la sentencia del if será True
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:

            #la info adicional, se almacena aquí para que pueda ser mandada después
            data.outb += recv_data


        #en el caso de que no se reciva ningún tipo de información, entonces
        #quiere decir que el cliente ha cerrado su socket, por lo tanto el socket del server también tendrá que cerrarse
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()


    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write

            #la info adicional que estábamso almacenando, se llega a enviar al cliente con esta función
            data.outb = data.outb[sent:]



sel = selectors.DefaultSelector()


host, port = '127.0.0.1', 65432

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")

#con esta diferencia, el servidor no se podrá bloquear
lsock.setblocking(False)

#con el data de esta función, se almacenará toda la información con el socket
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:

        #devuelve una lista de tuplas, una por cada socket
        events = sel.select(timeout=None)
        for key, mask in events:

            #tenemos dos opciones, que la tupla sea None
            #entonces, entonces de la función listen, se tendrá que aceptar la conexión
            if key.data is None:
                accept_wrapper(key.fileobj)

            #si no es None, entonces el socket ya ha sido aceptado y se tendrá que servir al cliente
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()