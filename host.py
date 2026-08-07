import socket
import sys

def resolve_host(hostname):
    try:
        return socket.gethostbyname(hostname)

    except socket.gaierror as e:
        print("Could not resolve hostname:", e)
        sys.exit(1)