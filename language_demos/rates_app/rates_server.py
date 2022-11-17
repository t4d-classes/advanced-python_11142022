""" rate server module """
from typing import Optional
from multiprocessing.sharedctypes import Synchronized
import multiprocessing as mp
import sys
import socket
import threading
import re
import requests


CLIENT_COMMAND_PARTS = (
    r"^(?P<name>[A-Z]+) "
    r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}) "
    r"(?P<symbol>[A-Z]{3})$"
)

CLIENT_COMMAND_REGEX = re.compile(CLIENT_COMMAND_PARTS)

# Add support for the following client command

# GET 2019-01-03 EUR

# GET is the command name
# 2019-01-03 is the date of the current rates to retrieve
# EUR is the currency symbol to retrieve, DO NOT USE USD

# Call the Rates API using the USD as the base to get the currency rate
# for the specified date and return the client application

# Ideally your code will do the following:

# 1. Use a regular expression with named capture groups to extract parts
# of the command

# 2. Add a function named "process_client_command" to
# "ClientConnectionThread" that will process the parsed command including
# calling the API, extracting the API response, and send back the rate
# value to the client

# Data comes back as JSON

# *3. Send back an error message for an incorrectly formatted command or an
# unsupported command name (only the GET command is supported)

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

                command = self.conn.recv(2048).decode("UTF-8")

                if not command:
                    break

                command_match = CLIENT_COMMAND_REGEX.match(command)

                if not command_match:
                    self.conn.sendall(b"Invalid Command Format")
                    continue

                command_dict = command_match.groupdict()
                command_name = command_dict["name"]
                currency_date = command_dict["date"]
                currency_symbol = command_dict["symbol"]

                self.process_client_command(
                    command_name, currency_date, currency_symbol
                )

                
        
        except ConnectionAbortedError:
            pass

        finally:
            with self.client_count.get_lock():
                self.client_count.value -= 1


    def process_client_command(
        self, command_name: str,
        currency_date: str, currency_symbol: str) -> None:
        """ process client command """

        if command_name != "GET":
            self.conn.sendall(b"Invalid Command")
            return

        resp = requests.get((
            "http://127.0.0.1:5060"
            f"/api/{currency_date}"
            f"?base=USD&symbols={currency_symbol}"), timeout=60)

        currency_rate = resp.json()["rates"][currency_symbol]

        self.conn.sendall(
            f"{currency_symbol}: {currency_rate}".encode("UTF-8"))



def rate_server(host: str, port: int, client_count: Synchronized) -> None:
    """rate server"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

        socket_server.bind( (host, port) )
        socket_server.listen()

        print(f"server is listening on {host}:{port}")

        while True:
            conn, addr = socket_server.accept()
            print(f"client at {addr[0]}:{addr[1]} connected")

            with client_count.get_lock():
                client_count.value += 1

            a_thread = ClientConnectionThread(conn, client_count)
            a_thread.start()


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
