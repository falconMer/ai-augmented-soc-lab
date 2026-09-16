# Lab Setup and Networking

> Status: planned / awaiting implementation verification

This document defines the initial VirtualBox network design for the AI-Augmented SOC Lab. The goal is to keep security-testing traffic separated from the physical home/network environment while still allowing lab machines to access the Internet for package installation, updates, APIs, and documentation.

## Host Hardware

- CPU: AMD Ryzen 5 4650U
- RAM: 16 GB
- Available working disk: approximately 50 GB
- Hypervisor: Oracle VirtualBox 7.x

## Initial Virtual Machines

| VM | Role | RAM target | Disk target | Planned lab IP |
|---|---|---:|---:|---|
| `SOC-WAZUH` | Wazuh all-in-one SIEM | ~6 GB | ~25 GB dynamic | `192.168.56.10` |
| `ATTACKER01` | Controlled security-testing workstation | 1.5–2 GB | 10–12 GB dynamic | `192.168.56.20` |
| `DC01` (later phase) | Windows Server / Active Directory | ~3 GB | as space permits | `192.168.56.30` |

The Windows host is also part of the host-only lab network and will later run the Wazuh Agent and Sysmon.

## Network Design

Each virtual machine will use two adapters:

1. **Adapter 1 — NAT**
   - Provides Internet access through VirtualBox.
   - Used for package downloads, updates, Wazuh installation, documentation, and API access.
   - Does not expose the VM directly to the physical LAN.

2. **Adapter 2 — Host-only Network**
   - Provides an isolated network shared by the Windows host and lab VMs.
   - Used for SIEM traffic, endpoint telemetry, controlled attack simulations, and internal lab communication.
   - Keeps testing traffic separate from the physical home/router network.

Bridged networking is intentionally not used for the security-testing network.

## Planned Addressing

Lab subnet:

```text
192.168.56.0/24
```

Planned addressing:

| System | Role | Address |
|---|---|---|
| Windows host | Monitored endpoint / management host | `192.168.56.1`* |
| `SOC-WAZUH` | Wazuh Manager, Indexer, Dashboard | `192.168.56.10` |
| `ATTACKER01` | Controlled testing workstation | `192.168.56.20` |
| `DC01` | Active Directory Domain Controller, later phase | `192.168.56.30` |

\*The Windows host-only adapter address must be verified with `ipconfig` before it is treated as final.

## Logical Topology

```text
                         Internet
                            |
                     VirtualBox NAT
                       /         \
                      /           \
             SOC-WAZUH          ATTACKER01
             Adapter 1: NAT      Adapter 1: NAT
             Adapter 2: Host     Adapter 2: Host
                 |                    |
             192.168.56.10         192.168.56.20
                 \                    /
                  \                  /
                   +----------------+
                   | Host-only LAN  |
                   |192.168.56.0/24 |
                   +--------+-------+
                            |
                     Windows Host
                     192.168.56.1*
```

## Step 1 — Install VirtualBox

Install the current VirtualBox 7.x release on the Windows host.

During installation, keep the standard networking components enabled, including VirtualBox host-only networking support.

A temporary network interruption during driver installation can occur and is expected.

## Step 2 — Open the VirtualBox Network Manager

In VirtualBox Manager, open the network configuration area. Depending on the installed version, this is available through one of the following paths:

```text
Tools -> Network
```

or:

```text
File -> Tools -> Network Manager
```

Open the **Host-only Networks** section.

## Step 3 — Create the Host-only Network

Create a host-only network and configure it as follows:

```text
IPv4 address: 192.168.56.1
Network mask:  255.255.255.0
```

This creates the planned lab subnet:

```text
192.168.56.0/24
```

The adapter name may appear as something similar to:

```text
VirtualBox Host-Only Ethernet Adapter
```

The exact adapter name should be recorded after creation.

## Step 4 — Disable DHCP for the Lab Network

Disable the DHCP server for the host-only network.

Static addressing is used so that SIEM agents, APIs, screenshots, documentation, and future detection scenarios always reference predictable addresses.

Planned static addresses:

```text
Windows Host      192.168.56.1
SOC-WAZUH         192.168.56.10
ATTACKER01        192.168.56.20
DC01              192.168.56.30
```

## Step 5 — Verify the Windows Host-only Adapter

On the Windows host, open Command Prompt or PowerShell and run:

```powershell
ipconfig
```

Locate the VirtualBox host-only adapter and confirm that it has an address in the planned subnet.

Expected result:

```text
IPv4 Address: 192.168.56.1
Subnet Mask:  255.255.255.0
```

If VirtualBox assigned a different host-only address, the actual value must be documented before continuing.

## Step 6 — VM Adapter Configuration

When the two Lubuntu VMs are created, each VM will receive:

```text
Adapter 1: NAT
Adapter 2: Host-only Network
```

The NAT interface remains DHCP-managed by VirtualBox.

The host-only interface will use a manually assigned static IP.

### `SOC-WAZUH`

```text
Host-only IP: 192.168.56.10/24
Gateway:      none on host-only interface
DNS:          none required on host-only interface
```

### `ATTACKER01`

```text
Host-only IP: 192.168.56.20/24
Gateway:      none on host-only interface
DNS:          none required on host-only interface
```

Internet-bound traffic should continue through the NAT adapter rather than the host-only interface.

## Why Two Adapters Are Used

The separation gives each VM two distinct paths:

```text
NAT
  -> Internet access

Host-only
  -> Internal SOC lab communication
```

This allows the lab to download packages and access external APIs without placing the attacker/test VM directly on the physical LAN.

## Validation Checklist

### Host-only network

- [ ] VirtualBox Host-only network created
- [ ] Host-only subnet confirmed as `192.168.56.0/24`
- [ ] DHCP disabled on the Host-only network
- [ ] Windows host-only IP verified with `ipconfig`
- [ ] Actual adapter name recorded

### VM networking — after VM creation

- [ ] `SOC-WAZUH` Adapter 1 configured as NAT
- [ ] `SOC-WAZUH` Adapter 2 configured as Host-only
- [ ] `SOC-WAZUH` receives `192.168.56.10/24`
- [ ] `ATTACKER01` Adapter 1 configured as NAT
- [ ] `ATTACKER01` Adapter 2 configured as Host-only
- [ ] `ATTACKER01` receives `192.168.56.20/24`
- [ ] Windows host can reach `SOC-WAZUH`
- [ ] Windows host can reach `ATTACKER01`
- [ ] `ATTACKER01` can reach `SOC-WAZUH`
- [ ] NAT Internet access works independently from the Host-only network

## Evidence to Capture

The following evidence should be added to the repository once the setup is completed:

1. Screenshot of the VirtualBox Host-only Network configuration.
2. Screenshot or sanitized output of Windows `ipconfig` showing the VirtualBox adapter.
3. Output of `ip -br address` from `SOC-WAZUH`.
4. Output of `ip -br address` from `ATTACKER01`.
5. Connectivity test from Windows to the Wazuh VM.
6. Connectivity test from `ATTACKER01` to the Wazuh VM.
7. Internet connectivity test from each Lubuntu VM through NAT.

Suggested screenshot paths:

```text
screenshots/networking/01-virtualbox-host-only-network.png
screenshots/networking/02-windows-host-only-adapter.png
screenshots/networking/03-wazuh-network-interfaces.png
screenshots/networking/04-attacker-network-interfaces.png
screenshots/networking/05-connectivity-tests.png
```

## Security Rationale

The testing workstation is intentionally kept off the physical LAN. Controlled reconnaissance and future attack simulations should target only systems explicitly created for this lab or the dedicated lab interface of the Windows host.

The host-only network provides a safer environment for experimenting with SOC monitoring, detections, and incident-response workflows while keeping the project reproducible.

## Next Step

After the Host-only network is created and verified, the next implementation task is to create the `SOC-WAZUH` Lubuntu VM with the planned CPU, RAM, disk, and dual-network-adapter configuration.
