import socket
import selectors
import types


selector = selectors.DefaultSelector()
messages = [b'Mensaje 1 del cliente', b'Mensaje 2 del cliente']
BUFFER_SIZE = 1024


def start_connections(host, port, num_conns):
    server_address = (host, port)

    for i in range(0, num_conns):

        connid = i + 1
        print('Iniciando conexión {} hacia {}'.format(connid, server_address))
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectamos usando connect_ex() en lugar de connect()
    # connect() retorna una excepcion
    # connect_ex() retorna un aviso de error

        socket_tcp.connect_ex(server_address)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        #los datos del cliente se almacenan en una varibale de tipo SimpleNamespace
        data = types.SimpleNamespace(connid=connid,
                msg_total=sum(len(m) for m in messages),
                recv_total=0,
                messages=list(messages),
                outb=b'')

        selector.register(socket_tcp, events, data=data)
        events = selector.select()
        for key, mask in events:
            service_connection(key, mask)



def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(BUFFER_SIZE) # Debe estar listo para lectura
        introduccion_datos(key)

        if recv_data:
            print('Recibido {} de conexión {}'.format(repr(recv_data), data.connid))
            data.recv_total += len(recv_data)

        #si no se recibe datos o ya se han recibido todos, se cierra conexión y por tanto, el servidor también la cerrará
        if not recv_data or data.recv_total == data.msg_total:
            print('Cerrando conexión', data.connid)
            selector.unregister(sock)
            sock.close()


    #cuando se está en el modo de escritura
    if mask & selectors.EVENT_WRITE:

        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
            introduccion_datos(key)

        if data.outb:
            #se envía la información al servidor
            print('Enviando {} a conexión {}'.format(repr(data.outb), data.connid))
            sent = sock.send(data.outb) # Debe estar listo para escritura
            data.outb = data.outb[sent:]


def introduccion_datos(key):

    client_socket = key.fileobj

    print('Introduzca los siguientes datos: temperatura mínima, temperatura máxima, presión y pluviometría')

    lista_datos=[]

    #hacemos los input para que se introduzcana los datos

    message = input(" -> ")
    temp_min=int(message)
    lista_datos.append(temp_min)

    message = input(" -> ")
    temp_max=int(message)
    lista_datos.append(temp_max)

    message = input(" -> ")
    presion=int(message)
    lista_datos.append(presion)


    message = input(" -> ")
    pluvi=int(message)
    lista_datos.append(pluvi)

    #mensaje para parar la conexión cuando se han introducido los datos
    message = input(" -> ")


#cuando se identifica una cadena de texto de tipo 'fin' se cerrará la conexión
#entendiendo así que se han introducido todos los datos pedidos
#al final se mostrará por pantalla la lista de los datos introducidos

    while message.lower().strip() != 'fin':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)

        message = input(" -> ")

    client_socket.close()  # close the connection

    print(lista_datos)

if __name__ == '__main__':
    host = socket.gethostname() # Esta función nos da el nombre de la máquina
    port = 12345
    BUFFER_SIZE = 1024 # Usamos un número pequeño para tener una respuesta rápida
    start_connections(host, port, 2)