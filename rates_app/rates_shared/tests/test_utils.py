""" Test Utils Module """

from unittest import TestCase, main
from unittest.mock import patch, mock_open
import pathlib

from rates_shared.utils import parse_command, read_config

YAML_CONFIG = """server:
  host: 127.0.0.1
  port: 5000
database:
  server: localhost\\SQLExpress
  database: somedb
  username: user
  password: pass"""


class TestUtils(TestCase):
    """ Test Utils Class """

    def test_parse_command(self) -> None:
        """ Parse Command Test """

        client_command = "GET 2021-04-01 CAD"

        result = parse_command(client_command)

        self.assertEqual(result, ("GET", "2021-04-01", "CAD"))

    def test_parse_command_invalid_format(self) -> None:
        """ Parse Command Test """

        client_command = "JUNK"

        result = parse_command(client_command)

        self.assertEqual(result, None)

    def test_read_config(self) -> None:
        """ Read Config Test """

        with patch('rates_shared.utils.open',
                   mock_open(read_data=YAML_CONFIG)) as mock:

            config = read_config()

            self.assertEqual(config, {
                "server": {
                    "host": "127.0.0.1",
                    "port": 5000,
                },
                "database": {
                    "server": "localhost\\SQLExpress",
                    "database": "somedb",
                    "username": "user",
                    "password": "pass",
                }
            })

            mock.assert_called_once_with(
                pathlib.Path(
                    "config",
                    "rates_config.yml"),
                encoding="UTF-8")


if __name__ == "__main__":
    main()
