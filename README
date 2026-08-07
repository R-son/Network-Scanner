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

And now I'm slowly turning that into a proper little network scanner.

This project is primarily a learning exercise, but I'm trying to keep the code organized enough that it could eventually become a genuinely useful tool.

---

## 🎥 Demo

### Single IP

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

### Subnet discovery

![Subnet Scan Demo](assets/subnet-scan.gif)

```text
$ sudo python main.py --subnet 192.168.1.0/24

Host             Port   Status
--------------------------------
192.168.1.13     22     CLOSED
192.168.1.13     80     OPEN
192.168.1.58     22     OPEN
192.168.1.100    80     TIMEOUT
```

---

# ⚙️ What it can do

### 🎯 Scan a single IP

Give the scanner an IP address and choose the TCP ports you want to test.

It distinguishes between:

| Status         | Meaning                                       |
| -------------- | --------------------------------------------- |
| 🟢 **OPEN**    | A TCP connection was successfully established |
| 🔴 **CLOSED**  | The host responded, but nothing is listening  |
| 🟡 **TIMEOUT** | No response was received before the timeout   |
| ⚠️ **ERROR**   | Something unexpected went wrong               |

---

### 🌐 Scan a subnet

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

---

# 🛠️ Under the hood

This project intentionally uses relatively low-level Python networking functionality instead of relying on an existing port-scanning library.

### `socket`

Used for TCP connections:

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(TIMEOUT)
sock.connect((ip, port))
```

This is the part that actually asks:

> "Can I establish a TCP connection to this IP and port?"

---

### `ipaddress`

Used to validate and manipulate addresses and networks:

```python
ipaddress.ip_address(ip)
```

and:

```python
ipaddress.ip_network(subnet, strict=False)
```

This handles things such as:

```text
192.168.1.42/24
        ↓
192.168.1.0/24
```

---

### Scapy

Scapy is used for ARP-based host discovery.

The subnet scanner essentially builds an Ethernet + ARP packet:

```python
Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(network))
```

and sends it over the network.

The hosts that answer are then passed to the TCP scanner.

---

# 🗂️ Project structure

```text
Network-Scanner/
│
├── main.py
├── ip.py
├── subnet.py
├── host.py
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

### `ip.py`

Single-IP scanning.

Contains:

* IP validation
* Port validation
* TCP connections
* Timeout handling
* Port status enum
* IP scan output

### `subnet.py`

Local network scanning.

Contains:

* Subnet validation
* ARP host discovery
* Multi-host scanning
* Subnet result formatting

### `host.py`

🚧 **Work in progress**

The plan is to resolve a hostname into an IP address and then reuse the existing IP scanning functionality.

---

# 🚀 Usage

## Help

```bash
python main.py --help
```

## Scan an IP

```bash
python main.py --ip 192.168.1.58
```

Then select the ports:

```text
Enter ports separated by commas (e.g. 80, 443): 22,80,443
```

## Scan a subnet

ARP scanning requires elevated privileges on many Linux systems:

```bash
sudo python main.py --subnet 192.168.1.0/24
```

Then choose the ports to scan.

---

# 📦 Requirements

* Python 3.10+
* Scapy
* A system capable of sending ARP packets

Install Scapy with:

```bash
pip install scapy
```

On Linux, subnet discovery may require:

```bash
sudo python main.py --subnet 192.168.1.0/24
```

---

# 🧪 What I've learned building this

This project has been a way of learning by actually breaking things and figuring out why they broke.

Some of the concepts I've worked through:

* IPv4 addresses
* CIDR notation
* Subnet masks
* Network and broadcast addresses
* TCP sockets
* TCP ports
* Socket timeouts
* Exception handling
* ARP
* Ethernet frames
* Host discovery
* DNS / hostname resolution
* Python modules
* Command-line arguments
* Structuring a multi-file Python project

One of the more useful lessons has been realizing that something as simple as:

```python
sock.connect((ip, port))
```

actually involves quite a lot of networking underneath it.

---

# 🛣️ Roadmap

* [x] Single IP scanning
* [x] TCP port scanning
* [x] Port validation
* [x] Timeout handling
* [x] Error handling
* [x] Subnet validation
* [x] ARP host discovery
* [x] Multi-host subnet scanning
* [ ] Hostname scanning
* [ ] Improve CLI
* [ ] Better error messages
* [ ] Improve scan performance
* [ ] More flexible port selection
* [ ] More polished output

---

# ⚠️ Disclaimer

This project is intended for **educational purposes and authorized network testing**.

Only scan machines and networks that you own or have explicit permission to test.

Network scanning can generate traffic and may trigger firewalls, intrusion detection systems, or other security mechanisms.

Don't point it at random networks just because you can.

---

## 📚 Built with

🐍 **Python**
⚡ **Scapy**
🔌 **Python sockets**
🌐 **ipaddress**

---

> *Started as "I wonder how port scanning actually works."*
>
> *Currently somewhere between "I understand it" and "why is this packet doing that?"*
