# 🔎 Network Scanner

> A small network scanner built from scratch in Python — partly to make something useful, and mostly to understand what the hell is actually happening underneath network scanning tools.

![Network Scanner Demo](assets/demo.gif)

---

## 🧠 Why I made this

I wanted to understand networking beyond just knowing that an IP address is an IP address.

So instead of immediately reaching for an existing scanner, I decided to build one myself.

The project started with a very simple question:

```text
"Can I connect to this port?"
```

That eventually turned into:

```text
IP address
    ↓
TCP connection
    ↓
Port status
```

Then I wanted to scan an entire network:

```text
Subnet
    ↓
ARP discovery
    ↓
Active hosts
    ↓
TCP ports
    ↓
Results
```

And eventually I wanted to be able to give the scanner a hostname instead of an IP:

```text
Hostname
    ↓
DNS resolution
    ↓
IPv4 / IPv6 address
    ↓
TCP ports
    ↓
Results
```

This project is primarily a learning exercise, but I'm trying to keep the code organized enough that it could eventually become a genuinely useful little tool.

---

# 🎥 Demo

## Single IP

![IP Scan Demo](assets/ip-scan.gif)

```text
$ python main.py --ip 192.168.1.58

Enter ports separated by commas (e.g. 80, 443): 22,80,8001

Port | Status
-----+--------
22   | OPEN
80   | OPEN
8001 | CLOSED
```

## Subnet discovery

![Subnet Scan Demo](assets/subnet-scan.gif)

```text
$ sudo python main.py --subnet 192.168.1.0/24

Enter ports separated by commas (e.g. 80, 443): 22,80

Host             Port   Status
--------------------------------
192.168.1.13     22     CLOSED
192.168.1.13     80     OPEN
192.168.1.58     22     OPEN
192.168.1.58     80     TIMEOUT
```

---

# ⚙️ What it can do

## 🎯 Scan a single IP

Give the scanner an IP address and choose the TCP ports you want to test.

It distinguishes between:

| Status         | Meaning                                       |
| -------------- | --------------------------------------------- |
| 🟢 **OPEN**    | A TCP connection was successfully established |
| 🔴 **CLOSED**  | The host responded, but nothing is listening  |
| 🟡 **TIMEOUT** | No response was received before the timeout   |
| ⚠️ **ERROR**   | Something unexpected went wrong               |

You can scan multiple ports in one run:

```text
Enter ports separated by commas (e.g. 80, 443): 22,80,443,8001
```

---

## 🌐 Scan a subnet

The subnet scanner uses **ARP** to discover active hosts on the local network.

For example:

```text
192.168.1.0/24
        ↓
   ARP discovery
        ↓
 ┌───────────────┐
 │ 192.168.1.13  │
 │ 192.168.1.58  │
 │ 192.168.1.100 │
 │ 192.168.1.254 │
 └───────────────┘
        ↓
    Port scanning
```

The user chooses the ports **once**, and those ports are then checked against every discovered host.

This means you don't have to enter the same ports separately for every machine.

> **Note:** ARP discovery only works on networks where ARP is applicable, such as a local IPv4 LAN. It is not a general-purpose way of discovering hosts across the Internet.

---

## 🏠 Scan a hostname

The hostname scanner uses Python's `socket.getaddrinfo()` to resolve a hostname.

For example:

```text
localhost
    ↓
getaddrinfo()
    ↓
┌──────────────┐
│ ::1          │ → IPv6
│ 127.0.0.1    │ → IPv4
└──────────────┘
    ↓
TCP port scanning
```

Because `getaddrinfo()` can return multiple addresses and address families, the scanner can handle both IPv4 and IPv6.

For example:

```text
$ python main.py --host localhost
```

The resolved addresses are passed to the appropriate TCP scanner.

---

# 🛠️ Under the hood

This project intentionally uses relatively low-level Python networking functionality instead of relying on an existing port-scanning library.

## `socket`

Used for TCP connections.

At its core, the scanner does something like:

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(TIMEOUT)
sock.connect((ip, port))
```

This is the part that actually asks:

> "Can I establish a TCP connection to this IP and port?"

The result determines whether the port is considered open, closed, timed out, or errored.

IPv6 connections use the appropriate address family:

```python
socket.AF_INET6
```

---

## `ipaddress`

Used to validate and manipulate IP addresses and networks.

For an individual address:

```python
ipaddress.ip_address(ip)
```

For a subnet:

```python
ipaddress.ip_network(subnet, strict=False)
```

This handles things such as:

```text
192.168.1.42/24
        ↓
192.168.1.0/24
```

It also gives access to useful network information such as:

```text
network address
broadcast address
netmask
prefix length
hosts
```

---

## Scapy

Scapy is used for ARP-based host discovery.

The subnet scanner builds an Ethernet + ARP packet:

```python
Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(network))
```

The Ethernet frame is sent as a broadcast, while the ARP request asks:

> "Who has an IP address in this network?"

Hosts that answer are collected and passed to the TCP scanner.

This was probably the part of the project where I spent the most time wondering why Scapy's documentation was giving me a page full of `XShortEnumField` instead of telling me what the hell I was supposed to do.

Eventually it started making sense.

---

## `getaddrinfo()`

Hostname resolution is handled using:

```python
socket.getaddrinfo()
```

Rather than assuming that a hostname is IPv4, the scanner checks the address family returned by the resolver.

That means a hostname can produce:

```text
AF_INET
    ↓
IPv4 address
```

or:

```text
AF_INET6
    ↓
IPv6 address
```

or even multiple addresses.

---

# 🗂️ Project structure

```text
Network-Scanner/
│
├── main.py
├── ip.py
├── subnet.py
├── host.py
├── Makefile
│
├── tests/
│   ├── test_ip.py
│   ├── test_subnet.py
│   └── test_host.py
│
├── assets/
│   ├── demo.gif
│   ├── ip-scan.gif
│   └── subnet-scan.gif
│
└── README.md
```

### `main.py`

The entry point.

Responsible for interpreting command-line arguments and deciding which scanner to run.

---

### `ip.py`

Single-IP scanning.

Contains:

* IP validation
* Port validation
* TCP connections
* IPv4/IPv6 connection handling
* Timeout handling
* Error handling
* Port status enum
* IP scan output

---

### `subnet.py`

Local network scanning.

Contains:

* Subnet validation
* ARP host discovery
* Multi-host scanning
* Port scanning across discovered hosts
* Subnet result handling

---

### `host.py`

Hostname scanning.

Contains:

* Hostname resolution
* IPv4 resolution
* IPv6 resolution
* Passing resolved addresses to the appropriate scanner

---

### `tests/`

Unit tests for the individual components.

The tests mock network operations where appropriate so that most of the test suite does **not** require a real network connection or root privileges.

---

### `Makefile`

Provides shortcuts for common development tasks:

```text
make run
make test
make test-verbose
make check
make clean
```

Because typing the same Python commands repeatedly is boring.

---

# 🚀 Usage

## Help

```bash
python main.py --help
```

---

## Scan an IP

```bash
python main.py --ip 192.168.1.58
```

Then select the ports:

```text
Enter ports separated by commas (e.g. 80, 443): 22,80,443
```

---

## Scan a subnet

ARP scanning requires elevated privileges on many Linux systems:

```bash
sudo python main.py --subnet 192.168.1.0/24
```

Then choose the ports to scan.

For example:

```text
Enter ports separated by commas (e.g. 80, 443): 22,80,443
```

---

## Scan a hostname

```bash
python main.py --host localhost
```

The hostname is resolved first, and the resulting IPv4 and/or IPv6 addresses are scanned.

---

# 🧰 Using the Makefile

Instead of typing the full Python command every time, the project includes a `Makefile`.

## Run the program

```bash
make run
```

Arguments can be passed through `ARGS`:

```bash
make run ARGS="--ip 127.0.0.1"
```

For a hostname:

```bash
make run ARGS="--host localhost"
```

For a subnet:

```bash
sudo make run ARGS="--subnet 192.168.1.0/24"
```

---

## Run the tests

```bash
make test
```

For verbose output:

```bash
make test-verbose
```

---

## Run the complete check

```bash
make check
```

This performs Python syntax/bytecode compilation and then runs the unit tests.

---

## Clean generated Python files

```bash
make clean
```

This removes Python cache files such as:

```text
__pycache__/
*.pyc
```

---

## See available Make targets

```bash
make help
```

---

# 🧪 Testing

The project contains unit tests for the main pieces of functionality.

The tests cover things such as:

```text
IP scanner
├── OPEN
├── CLOSED
├── TIMEOUT
└── ERROR

Hostname scanner
├── IPv4
├── IPv6
├── IPv4 + IPv6
└── Invalid hostname

Subnet scanner
├── Valid subnet
├── Invalid subnet
├── Hosts discovered
└── No hosts discovered
```

The network operations are mocked where appropriate.

For example, the test for a timeout doesn't actually wait twenty seconds for a real machine to stop responding. Instead, the socket is mocked to behave as though a timeout occurred.

This keeps the tests:

* fast
* repeatable
* independent of the current network
* usable without root privileges

Run them with:

```bash
make test
```

---

# 📦 Requirements

* Python 3.10+
* Scapy
* A system capable of sending ARP packets for subnet discovery

Install Scapy with:

```bash
pip install scapy
```

Or, depending on your Python installation:

```bash
python3 -m pip install scapy
```

On Linux, subnet discovery may require elevated privileges:

```bash
sudo python main.py --subnet 192.168.1.0/24
```

The normal IP and hostname scanners do not inherently require root privileges.

---

# 🧠 What I've learned building this

This project has been a way of learning by actually breaking things and figuring out why they broke.

Some of the concepts I've worked through:

* IPv4 addresses
* IPv6 addresses
* CIDR notation
* Subnet masks
* Network addresses
* Broadcast addresses
* TCP sockets
* TCP ports
* Socket timeouts
* TCP connection errors
* Exception handling
* ARP
* Ethernet frames
* Host discovery
* DNS / hostname resolution
* IPv4 vs IPv6 address families
* Python modules
* Python enums
* Command-line arguments
* Structuring a multi-file Python project
* Unit testing
* Mocking
* Makefiles

One of the more useful lessons has been realizing that something as simple as:

```python
sock.connect((ip, port))
```

actually involves quite a lot of networking underneath it.

Likewise, something that initially looked like:

```python
Ether(...) / ARP(...)
```

turned into an excuse to learn what Ethernet frames, MAC addresses, ARP requests, and broadcast traffic actually are.

And somewhere along the way I discovered that networking documentation can apparently be written in a language consisting entirely of:

```text
XShortEnumField
MultipleTypeField
SourceIPField
FieldLenField
```

So that's been fun.

---

# 🛣️ Roadmap

The original goal was simply to make a TCP port scanner.

That part grew into something a little more interesting.

### Completed

* [x] Single IP scanning
* [x] TCP port scanning
* [x] Port validation
* [x] `OPEN` status
* [x] `CLOSED` status
* [x] `TIMEOUT` status
* [x] `ERROR` status
* [x] IPv4 scanning
* [x] IPv6 scanning
* [x] Subnet validation
* [x] ARP host discovery
* [x] Multi-host subnet scanning
* [x] Hostname resolution
* [x] IPv4 hostname resolution
* [x] IPv6 hostname resolution
* [x] Unit tests
* [x] Makefile

# ⚠️ Disclaimer

This project is intended for **educational purposes and authorized network testing**.

Only scan machines and networks that you own or have explicit permission to test.

Network scanning generates traffic and may trigger:

* firewalls
* intrusion detection systems
* security alerts
* rate limiting
* other network security mechanisms

Don't point it at random networks just because you can.

---

# 📚 Built with

🐍 **Python**

⚡ **Scapy**

🔌 **Python sockets**

🌐 **ipaddress**

🧪 **unittest**

🔨 **Make**