""" socket client """

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:

    socket_client.connect( ('127.0.0.1', 5075) )

    welcome_message = socket_client.recv(2048)

    print(welcome_message.decode('UTF-8'))

    while True:

        command = input("> ")

        if command == "exit":
            break
        else:
            socket_client.sendall(command.encode("UTF-8"))
            print(socket_client.recv(2048).decode("UTF-8"))
