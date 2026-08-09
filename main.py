import sys
from ip import ip_scan
from subnet import subnet_scan
from host import resolve_host

def help() :
    print("Usage: py main.py <flag> <arguments>")
    print("Flags:")
    print("    --help or -h")
    print("    --ip <ip>")
    print("    --subnet <subnet> or -s <subnet>")
    print("    --host <hostname>")
    sys.exit(1)

def usage() :
    print("Usage: py main.py <flag> <arguments>")
    print("For more information, run 'py main.py --help'")
    sys.exit(1)

arg_length = len(sys.argv)
if (arg_length < 2):
    usage()

match sys.argv[1]:
    case "--help" | "-h":
        help()
    case "-ip": # A single IP address
        if (arg_length < 3):
            usage()
            sys.exit(1)
        ip_scan(sys.argv[2])
    case "--subnet" | "-s": # A subnet
        if (arg_length < 3):
            usage()
            sys.exit(1)
        results = subnet_scan(sys.argv[2])
    case "--host":
        if (arg_length < 3):
            usage()
            sys.exit(1)
        resolve_host(sys.argv[2])
    case _:
        print("Unknown option")
        usage()

    # case "--host":


# A hostname (bonus)

