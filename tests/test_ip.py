import unittest
from unittest.mock import patch
import socket

from ip import connect


class TestConnect(unittest.TestCase):

    @patch("ip.socket.socket")
    def test_open_port(self, mock_socket):
        mock_sock = mock_socket.return_value.__enter__.return_value
        result = connect("127.0.0.1", 80)
        self.assertEqual(result.name, "OPEN")

    @patch("ip.socket.socket")
    def test_closed_port(self, mock_socket):
        mock_sock = mock_socket.return_value.__enter__.return_value
        mock_sock.connect.side_effect = ConnectionRefusedError
        result = connect("127.0.0.1", 80)
        self.assertEqual(result.name, "CLOSED")

    @patch("ip.socket.socket")
    def test_timeout(self, mock_socket):
        mock_sock = mock_socket.return_value.__enter__.return_value
        mock_sock.connect.side_effect = socket.timeout
        result = connect("127.0.0.1", 80)
        self.assertEqual(result.name, "TIMEOUT")

    @patch("ip.socket.socket")
    def test_error(self, mock_socket):
        mock_sock = mock_socket.return_value.__enter__.return_value
        mock_sock.connect.side_effect = OSError("Test error")
        result = connect("127.0.0.1", 80)
        self.assertEqual(result.name, "ERROR")


if __name__ == "__main__":
    unittest.main()