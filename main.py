import sys
from ip import ip_scan

def help() :
    print("Usage: py main.py <flag> <arguments>")
    print("Flags:")
    print("    --help")
    print("    --ip <ip>")
    print("    --subnet <subnet>")
    print("    --host <hostname>")
    sys.exit(1)

def usage() :
    print("Usage: py main.py <flag> <arguments>")
    print("For more information, run 'py main.py --help'")
    sys.exit(1)

arg_length = len(sys.argv)
if (arg_length < 3):
    usage()

match sys.argv[1]:
    case "--help" | "-h":
        help()
    case "-ip": # A single IP address
        ip_scan(sys.argv[2])
        # print_ip_results(results)
    # case "--subnet":
    #     results = subnet_scan(sys.argv[2])
    case _:
        print("Unknown option")
        usage()

    # case "--host":

# A subnet (optional extension)
# A hostname (bonus)

