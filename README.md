# Final Project: Simple IPv4 Router

This project involves implementing a simple router for a Large Language Model (LLM) startup company using Mininet and a POX controller. The objective is to create a network topology that simulates a production environment, incorporating routing and firewall rules to manage traffic between different subnets, trusted and untrusted hosts, and a dedicated server. The implementation aims to enhance network security by strictly controlling IP and ICMP traffic flows as specified in the project requirements.

## Devices and IP Addresses
![image](https://github.com/paolopedroso/simpleipv4router/assets/108847100/3d6b0b71-a109-4052-9e75-7c8242512e38)

**Floor 1 Hosts (Department A)**
- h101: 128.114.1.101/24
- h102: 128.114.1.102/24
- h103: 128.114.1.103/24
- h104: 128.114.1.104/24

**Floor 2 Hosts (Department B)**
- h201: 128.114.2.201/24
- h202: 128.114.2.202/24
- h203: 128.114.2.203/24
- h204: 128.114.2.204/24

**External Hosts**
- Trusted Host (h_trust): 192.47.38.109/24
- Untrusted Host (h_untrust): 108.35.24.113/24

**LLM Server**
- h_server: 128.114.3.178/24

## Project Goals

1. **Network Topology Creation**: Construct a Mininet topology for the specified network.
2. **Traffic Control via POX Controller**: Implement a POX controller to enforce the firewall rules.

## Traffic Control Rules

- **Untrusted Host Restrictions**:
  - Block all IP traffic to internal hosts and the LLM server.
  - Block all ICMP traffic to internal hosts and the LLM server.

- **Trusted Host Restrictions**:
  - Allow all traffic to Department A hosts.
  - Block all IP traffic to the LLM server.
  - Block ICMP traffic to Department B hosts and the LLM server.

- **Department Restrictions**:
  - Block ICMP traffic between Department A and Department B hosts.

## Implementation and Testing

Modify the Mininet and POX controller files to meet the project requirements. Test using Mininet commands and Wireshark to verify packet flow and ensure compliance with the traffic control rules.

## Deliverables

2. **topo_skel.py**: Mininet topology code.
3. **controller_skel.py**: POX controller code.
4. **README.txt**: Explanation of the submission.

