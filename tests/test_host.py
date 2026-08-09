import unittest
import socket
from unittest.mock import patch

from host import resolve_host


class TestResolveHost(unittest.TestCase):

    @patch("host.ip_scan")
    @patch("host.socket.getaddrinfo")
    def test_resolve_ipv4(self, mock_getaddrinfo, mock_ip_scan):
        mock_getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0))]
        resolve_host("localhost")
        mock_ip_scan.assert_called_once_with("127.0.0.1", socket.AF_INET)

    @patch("host.ip_scan")
    @patch("host.socket.getaddrinfo")
    def test_resolve_ipv6(self, mock_getaddrinfo, mock_ip_scan):
        mock_getaddrinfo.return_value = [(socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("::1", 0, 0, 0))]
        resolve_host("localhost")
        mock_ip_scan.assert_called_once_with("::1", socket.AF_INET6)

    @patch("host.ip_scan")
    @patch("host.socket.getaddrinfo")
    def test_resolve_ipv4_and_ipv6(self, mock_getaddrinfo, mock_ip_scan):
        mock_getaddrinfo.return_value = [
            (socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("::1", 0, 0, 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "",("127.0.0.1", 0))
        ]
        resolve_host("localhost")
        self.assertEqual(mock_ip_scan.call_count, 2)
        mock_ip_scan.assert_any_call("::1", socket.AF_INET6)
        mock_ip_scan.assert_any_call("127.0.0.1", socket.AF_INET)

    @patch("host.socket.getaddrinfo")
    def test_invalid_hostname(self, mock_getaddrinfo):
        mock_getaddrinfo.side_effect = socket.gaierror
        resolve_host("this-host-does-not-exist")


if __name__ == "__main__":
    unittest.main()