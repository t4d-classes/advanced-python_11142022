""" rate server module """
from typing import Optional
from multiprocessing.sharedctypes import Synchronized
import multiprocessing as mp
import sys
import socket
import threading

# Use a multiprocessing shared "Value" object to track the count of
# connected clients
# increment the count when a client connects, and decrement the count when
# a client disconnects
# add a new server command named "count" that displays the count of
# connected clients

class ClientConnectionThread(threading.Thread):
    """ client connection thread """

    def __init__(self, conn: socket.socket, client_count: Synchronized):
        threading.Thread.__init__(self)
        self.conn = conn
        self.client_count = client_count

    def run(self) -> None:

        try:

            self.conn.sendall(b"Connected to the Rates Server")

            while True:

                message = self.conn.recv(2048).decode("UTF-8")

                if not message:
                    break

                print(f"recv: {message}")
                self.conn.sendall(message.encode('UTF-8'))
        
        except ConnectionAbortedError:
            pass

        finally:
            with self.client_count.get_lock():
                self.client_count.value -= 1

          


def rate_server(host: str, port: int, client_count: Synchronized) -> None:
    """rate server"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

        socket_server.bind( (host, port) )
        socket_server.listen()

        print(f"server is listening on {host}:{port}")

        while True:
            conn, addr = socket_server.accept()
            print(f"client at {addr[0]}:{addr[1]} connected")

            a_thread = ClientConnectionThread(conn, client_count)
            a_thread.start()

            with client_count.get_lock():
                client_count.value += 1






def command_start_server(
    server_process: Optional[mp.Process],
    host: str,
    port: int,
    client_count: Synchronized) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        server_process = mp.Process(
            target=rate_server,
            args=(host, port, client_count))
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


def command_count(client_count: Synchronized) -> None:
    """ command count """

    print(client_count.value)


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
        client_count: Synchronized = mp.Value('i', 0)

        # define the host and port variables here
        host = "127.0.0.1"
        port = 5050

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(
                    server_process, host, port, client_count)
            elif command == "stop":
                server_process = command_stop_server(server_process)
            elif command == "status":
                command_status(server_process)
            elif command == "count":
                command_count(client_count)
            elif command == "exit":
                server_process = command_exit(server_process)
                break

    except KeyboardInterrupt:
        server_process = command_exit(server_process)

    sys.exit(0)


if __name__ == '__main__':
    main()
