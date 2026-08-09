import unittest
from unittest.mock import patch

from subnet import discover_hosts


class TestDiscoverHosts(unittest.TestCase):

    @patch("subnet.srp")
    def test_discover_hosts(self, mock_srp):

        mock_srp.return_value = (
            [
                ("sent_packet_1", type("Packet", (), {"psrc": "192.168.1.10"})()),
                ("sent_packet_2", type("Packet", (), {"psrc": "192.168.1.20"})())
            ],[]
        )

        network = "192.168.1.0/24"

        from ipaddress import ip_network

        hosts = discover_hosts(ip_network(network))
        self.assertEqual(hosts, ["192.168.1.10", "192.168.1.20"])


if __name__ == "__main__":
    unittest.main()