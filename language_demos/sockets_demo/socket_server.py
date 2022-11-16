""" socket server """

import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

    socket_server.bind( ('127.0.0.1', 5075 ) )
    socket_server.listen()

    print("server is listening on 127.0.0.1:5075")

    conn, addr = socket_server.accept()

    print(f"client at {addr[0]}:{addr[1]} connected")

    conn.sendall(b"Welcome to the socket server!")

    while True:

        message = conn.recv(2048).decode("UTF-8")
        print(f"recv: {message}")
        conn.sendall(message.encode('UTF-8'))
