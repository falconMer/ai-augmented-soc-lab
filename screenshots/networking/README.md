# Networking Evidence

This folder contains screenshots captured during the initial VirtualBox networking setup for the AI-Augmented SOC Lab.

## Evidence

### 1. Host-only network configuration

![VirtualBox host-only network configuration](01-host-only-network-config.png)

Verified from the screenshot:

- Adapter configured manually
- IPv4 address: `192.168.56.1`
- Network mask: `255.255.255.0`
- Planned lab subnet: `192.168.56.0/24`

### 2. VM NAT adapter

![VirtualBox NAT adapter](02-vm-adapter-nat.png)

The first VM network adapter is configured as **NAT** to provide Internet access for package installation, updates, documentation, and API access.

### 3. VM host-only adapter

![VirtualBox host-only VM adapter](03-vm-adapter-host-only.png)

The second VM network adapter is configured as **Host-only Adapter** using `VirtualBox Host-Only Ethernet Adapter`. This interface will carry isolated SOC lab traffic.

## Remaining validation

These screenshots confirm the planned adapter configuration, but the following still need separate verification before the networking phase is considered complete:

- DHCP server disabled for the host-only network
- Windows `ipconfig` confirms the host-only interface address
- Static IP assignment inside each Lubuntu VM
- Connectivity tests between the host, Wazuh VM, and testing VM
- NAT Internet connectivity from both VMs
