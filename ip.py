import ipaddress
import socket
import sys
from enum import Enum

TIMEOUT = 20
class port_status(Enum) :
    OPEN = 1
    CLOSED = 2
    TIMEOUT = 3
    ERROR = 4

def print_ip_results(results) :
    
    print("Port | Status")
    print("-----+--------")

    for port, status in results.items():
        print(f"{port:<4} | {status}")

def ip_scan(ip) :
    results = {}
    try :
        ipaddress.ip_address(ip)
        while True:
            user_input = input("Enter ports separated by commas (e.g. 80, 443):")
            ports = [int(port.strip()) for port in user_input.split(",") if port.strip()]

            valid = True
            for port in ports:
                if not (1 <= port <= 65535):
                    print("Invalid port. Please enter the ports again.")
                    valid = False
                    break

            if valid:
                break
        # print("Ports: ", ports)
        for port in ports :
            print("Trying port ", port)
            result = connect(ip, port)
            results[port] = result.name
        print_ip_results(results)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

# def connect(ip, port) :
#     try :
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock :
#             sock.settimeout(TIMEOUT)
#             # raise socket.timeout()
#             # raise RuntimeError("Test error")
#             sock.connect((ip, port))
#             print("Port {} is open".format(port))
#             return port_status.OPEN
            
#     except socket.timeout:
#         print(f"Port {port} timed out")
#         return port_status.TIMEOUT

#     except ConnectionRefusedError:
#         print(f"Port {port} is closed")
#         return port_status.CLOSED

#     except OSError as e:
#         print(f"Error scanning port {port}: {e}")
#         return port_status.ERROR

def connect(ip, port, family=socket.AF_INET):
    try:
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            sock.connect((ip, port))

            print(f"Port {port} is open")
            return port_status.OPEN

    except socket.timeout:
        print(f"Port {port} timed out")
        return port_status.TIMEOUT

    except ConnectionRefusedError:
        print(f"Port {port} is closed")
        return port_status.CLOSED

    except OSError as e:
        print(f"Error scanning port {port}: {e}")
        return port_status.ERROR