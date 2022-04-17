# echo-server.py

#primero siempre se tiene que improtar la librería y definir el host y el puerto

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

#se crea la conexión servidor con un socket en un bucle

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    #método bind, para asociar un socket con una red con un puerto y un host
    s.bind((HOST, PORT))

    #se escucha la conexión con el listen
    s.listen()

    #se aceta la conexión con el acept
    conn, addr = s.accept()

    #se crea un bucle capaz de leer cualquier mensaje mandado por un cliente
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
