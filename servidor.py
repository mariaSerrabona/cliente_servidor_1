import selectors
import types
import socket

selector = selectors.DefaultSelector()
def accept_conn(sock):
    #para poner el socket en un modo de no-bloqueo
    #si se bloqueara, el servidor se conelaría hasta obtener una respuesta del cleinte, dejando de lado otros posibles sockets que se pueden crear
    conn, addr = sock.accept()
    print('Conexión aceptada en {}'.format(addr))

    # Ponemos el socket en modo de no-bloqueo
    conn.setblocking(False)

    #creamos un objeto para mantener la información que se le quiere pasar al cliente
    #previamente, necesitamos saber que el servidor está listo para leer y escribir info
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, events, data=data)


def service_conn(key, mask):
    sock = key.fileobj
    data = key.data

    #si el socket está listo para leer, entonces la sentencia del if será True
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(BUFFER_SIZE)
        if recv_data:
        #la info adicional, se almacena aquí para que pueda ser mandada después
            data.outb += recv_data

        #en el caso de que no se reciva ningún tipo de información, entonces
        #quiere decir que el cliente ha cerrado su socket, por lo tanto el socket del server también tendrá que cerrarse
        else:
            print('Cerrando conexion en {}'.format(data.addr))
            selector.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('Echo desde {} a {}'.format(repr(data.outb), data.addr))
            sent = sock.send(data.outb)

            #la info adicional que estábamso almacenando, se llega a enviar al cliente con esta función
            data.outb = data.outb[sent:]





if __name__ == '__main__':
    host = socket.gethostname() # Esta función nos da el nombre de la máquina
    port = 12345
    BUFFER_SIZE = 1024 # Usamos un número pequeño para tener una respuesta rápida

    # Creamos un socket TCP
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configuramos el socket en modo de no-bloqueo
    socket_tcp.setblocking(False)
    socket_tcp.bind((host, port))
    socket_tcp.listen()
    print('Socket abierto en {} {}'.format(host, port))

    #con esta diferencia, el servidor no se podrá bloquear
    socket_tcp.setblocking(False)

    #con el data de esta función, se almacenará toda la información con el socket
    selector.register(socket_tcp, selectors.EVENT_READ, data=None)

    while socket_tcp:
        events = selector.select(timeout=None)
        for key, mask in events:
            #tenemos dos opciones, que la tupla sea None
            #entonces, entonces de la función listen, se tendrá que aceptar la conexión
            if key.data is None:
                accept_conn(key.fileobj)

            #si no es None, entonces el socket ya ha sido aceptado y se tendrá que servir al cliente
            else:
                service_conn(key, mask)

                socket_tcp.close()

    print('Conexión terminada.')