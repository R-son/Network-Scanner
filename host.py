import socket
import sys
from ip import connect, print_ip_results
import socket
import ipaddress

def ip_scan(ip, family=socket.AF_INET):
    results = {}

    try:
        ipaddress.ip_address(ip)
        while True:
            user_input = input(
                "Enter ports separated by commas for ip " + ip + " (e.g. 80, 443):")

            ports = [
                int(port.strip())
                for port in user_input.split(",")
                if port.strip()
            ]

            valid = True

            for port in ports:
                if not (1 <= port <= 65535):
                    print("Invalid port. Please enter the ports again.")
                    valid = False
                    break

            if valid:
                break

        for port in ports:
            print("Trying port", port)
            result = connect(ip, port, family)
            results[port] = result.name

        print_ip_results(results)

    except Exception as e:
        print("Error:", e)
        sys.exit(1)

def resolve_host(hostname):
    try:
        addresses = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)

        for address in addresses:
            family = address[0]
            ip = address[4][0]
            ip_scan(ip, family)

    except socket.gaierror as e:
        print("Could not resolve hostname:", e)