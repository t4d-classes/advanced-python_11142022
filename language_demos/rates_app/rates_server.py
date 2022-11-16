""" rate server module """
from typing import Optional
import multiprocessing as mp
import sys


def rate_server() -> None:
    """rate server"""

    # implement socket server
    # the host and port should be received as parameters into this function

    # - use "AF_INET" for IPv4
    # - use "SOCK_STREAM" for TCP

    # when a client connects, send the following string:
    #     "Connected to the Rate Server"

    # wire up an echo server which receives a string and echos back to
    # the client the string that is received

    while True:
        pass


def command_start_server(server_process: Optional[mp.Process]) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        # HINT: READ PYTHON DOCS ON HOW TO PASS PARAMETERS TO A NEW PROCESS
        server_process = mp.Process(target=rate_server)
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
        # host: 127.0.0.1
        # port: 5050

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(server_process)
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
