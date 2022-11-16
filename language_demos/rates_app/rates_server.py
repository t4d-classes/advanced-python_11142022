""" rate server module """
from typing import Optional
import multiprocessing as mp
import sys
import socket
import threading

class ClientConnectionThread(threading.Thread):
    """ client connection thread """

    def __init__(self, conn: socket.socket):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self) -> None:

        self.conn.sendall(b"Connected to the Rates Server")

        while True:

            message = self.conn.recv(2048).decode("UTF-8")

            if not message:
                break

            print(f"recv: {message}")
            self.conn.sendall(message.encode('UTF-8'))     


# Create "ClientConnectionThread" class that inherits from "Thread"

# Each time a client connects, a new thread should be created with the
# "ClientConnectionThread" class. The class is responsible for sending the
# welcome message and interacting with the client, echoing messages

# The server should support multiple clients at the same time


def rate_server(host: str, port: int) -> None:
    """rate server"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

        socket_server.bind( (host, port) )
        socket_server.listen()

        print(f"server is listening on {host}:{port}")

        while True:
            conn, addr = socket_server.accept()
            print(f"client at {addr[0]}:{addr[1]} connected")
            a_thread = ClientConnectionThread(conn)
            a_thread.start()






def command_start_server(
    server_process: Optional[mp.Process], host: str, port: int) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        # HINT: READ PYTHON DOCS ON HOW TO PASS PARAMETERS TO A NEW PROCESS
        server_process = mp.Process(target=rate_server, args=(host, port))
        server_process.start()
        print("server started")

    return server_process


def command_stop_server(
    server_process: Optional[mp.Process]) -> Optional[mp.Process]:
    """ command stop server """

    if not server_process or not server_process.is_alive():
        print("server is not running")
    else:
        server_process.terminate()
        print("server stopped")

    server_process = None

    return server_process


def command_status(
    server_process: Optional[mp.Process]) -> None:
    """ command status """

    if server_process and server_process.is_alive():
        print("server is running")
    else:
        print("server is stopped")


def command_exit(
    server_process: Optional[mp.Process]) -> Optional[mp.Process]:
    """ command exit """

    if server_process and server_process.is_alive():
        server_process.terminate()

    server_process = None

    return server_process


def main() -> None:
    """Main Function"""

    try:

        server_process: Optional[mp.Process] = None

        # define the host and port variables here
        host = "127.0.0.1"
        port = 5050

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(
                    server_process, host, port)
            elif command == "stop":
                server_process = command_stop_server(server_process)
            elif command == "status":
                command_status(server_process)
            elif command == "exit":
                server_process = command_exit(server_process)
                break

    except KeyboardInterrupt:
        server_process = command_exit(server_process)

    sys.exit(0)


if __name__ == '__main__':
    main()
