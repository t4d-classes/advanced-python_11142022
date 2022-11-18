""" rate client module """
from typing import Any
import sys
import socket
import yaml
import pathlib

def read_config() -> Any:
    """" read config """

    with open(
        pathlib.Path("rates_app", "config", "rates_config.yml"),
        encoding="UTF-8") as config_file:

        return yaml.load(config_file, Loader=yaml.SafeLoader)


def main(host: str, port: int) -> None:
    """ main """

    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
            socket_client.connect( (host, port) )
            welcome_message = socket_client.recv(2048)
            print(welcome_message.decode('UTF-8'))
            while True:
                command = input("> ")
                if command == "exit":
                    break
                else:
                    socket_client.sendall(command.encode("UTF-8"))
                    print(socket_client.recv(2048).decode("UTF-8"))

    except ConnectionResetError:
        print("Server connection was closed.")

    except KeyboardInterrupt:
        pass

    sys.exit(0)

if __name__ == "__main__":
    config = read_config()
    main(config["server"]["host"], int(config["server"]["port"]))
