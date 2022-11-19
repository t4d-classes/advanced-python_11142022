""" utils module """

from typing import Any, Optional
import pathlib
import re
import yaml

# GET 2021-01-03 EUR,GBP:CAD;HKD|INR
CLIENT_COMMAND_PARTS = (
    r"^(?P<name>[A-Z]+) "
    r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}) "
    r"(?P<symbol>[A-Z,:|;]+)$"
)

CLIENT_COMMAND_REGEX = re.compile(CLIENT_COMMAND_PARTS)


def parse_command(command: str) -> Optional[tuple[str, str, str]]:
    """ parse command """

    command_match = CLIENT_COMMAND_REGEX.match(command)

    if not command_match:
        return None

    command_dict = command_match.groupdict()

    return (
        command_dict["name"],
        command_dict["date"],
        command_dict["symbol"])


def read_config() -> Any:
    """" read config """

    with open(
            pathlib.Path("config", "rates_config.yml"),
            encoding="UTF-8") as config_file:

        return yaml.load(config_file, Loader=yaml.SafeLoader)
