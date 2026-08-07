import ipaddress
import sys
from scapy.all import ARP, Ether, srp
from ip import connect


def discover_hosts(network) :
    hosts = []
    # print(list(network.hosts()))
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(network))
    answered, unanswered = srp(packet, timeout=2)
    for sent, received in answered:
        hosts.append(received.psrc)
    return hosts

def print_subnet_results(results):
    print("Host             | Port   | Status")
    print("-----------------+--------+--------")

    for (host, port), status in results.items():
        print(f"{host:<16} | {port:<6} | {status}")

def subnet_scan(subnet) :
    results = {}
    try:
        network = ipaddress.ip_network(subnet, strict=False)
        if network.num_addresses > 1024:
            print("Subnet too large")
            return
        hosts = discover_hosts(network)
        if not hosts:
            print("No active hosts found")
            return
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
        for host in hosts :
            for port in ports :
                print("Trying port ", port)
                result = connect(host, port)
                results[(host, port)] = result.name
        print_subnet_results(results)
    except Exception as e:
        print("Error scanning subnet:", e)
        sys.exit(1)