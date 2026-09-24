# Lab Setup and Networking

> Status: SOC-WAZUH networking verified / ready for manager-only Wazuh install

## Host Hardware

- CPU: AMD Ryzen 5 4650U
- RAM: 16 GB
- Available working disk at project start: approximately 50 GB
- Hypervisor: Oracle VirtualBox 7.x

## Final VM Plan

| VM | Role | RAM target | Disk target | Lab IP |
|---|---|---:|---:|---|
| `SOC-WAZUH` | Wazuh Manager only (Lubuntu 24.04 LTS) | ~3 GB | ~15 GB dynamic | `192.168.56.10` |
| `ATTACKER01` | Controlled security-testing workstation | 1.5–2 GB | 8–10 GB dynamic | `192.168.56.20` |
| `DC01` (optional later) | Windows Server / Active Directory | ~3 GB | only if space permits | `192.168.56.30` |

The Windows host is the first monitored endpoint and uses `192.168.56.1` on the VirtualBox host-only adapter.

## Network Design

Each VM uses two adapters:

1. **Adapter 1 — NAT**
   - Internet access for package installation, updates, documentation, and APIs.

2. **Adapter 2 — Host-only Adapter**
   - Isolated SOC lab communication.
   - Lab subnet: `192.168.56.0/24`.
   - DHCP disabled.
   - Static addressing used for reproducibility.

Bridged networking is intentionally not used for controlled security testing.

## Addressing

| System | Address |
|---|---|
| Windows host | `192.168.56.1` |
| `SOC-WAZUH` | `192.168.56.10` |
| `ATTACKER01` | `192.168.56.20` |
| `DC01` later | `192.168.56.30` |

## Verified SOC-WAZUH Interfaces

The lightweight rebuild has the expected dual-interface configuration:

| Interface | Purpose | Address |
|---|---|---|
| `enp0s3` | VirtualBox NAT / Internet | `10.0.2.15/24` via DHCP |
| `enp0s8` | Isolated host-only lab | `192.168.56.10/24` static |

Both interfaces are UP and the host-only address is persistent.

## Verified Network Milestones

- [x] VirtualBox host-only adapter created
- [x] Host-only subnet configured as `192.168.56.0/24`
- [x] DHCP disabled
- [x] Windows host-only address confirmed as `192.168.56.1`
- [x] NAT and Host-only adapters configured on the SOC VM
- [x] SOC VM static host-only address confirmed as `192.168.56.10/24`
- [x] SOC VM NAT address confirmed as `10.0.2.15/24`
- [x] SOC VM can reach Windows host at `192.168.56.1`
- [x] SOC VM Internet connectivity verified
- [ ] `ATTACKER01` networking configured

## Lightweight Rebuild

The existing full Wazuh VM was a completed prototype. The final `SOC-WAZUH` VM uses Lubuntu 24.04 LTS because VirtualBox clipboard integration is part of the working lab workflow:

```text
OS:        Lubuntu 24.04 LTS
RAM:       3072 MB
vCPU:      2
Disk:      15 GB dynamically allocated
Adapter 1: NAT
Adapter 2: VirtualBox Host-Only Ethernet Adapter
Lab IP:    192.168.56.10/24
Gateway:   none on the Host-only interface
DNS:       none required on the Host-only interface
```

The NAT interface remains DHCP-managed and provides the default route.

## Evidence

Sanitized interface verification is stored at:

```text
evidence/networking/01-soc-interface-verification.txt
```

## Security Rationale

The attacker workstation remains off the physical LAN. Controlled reconnaissance and attack simulations must target only dedicated lab systems or the Windows host's lab interface.

## Historical Resource Finding

The initial all-in-one Wazuh deployment proved functional but included OpenSearch/Wazuh Indexer and Dashboard, which added unnecessary memory and disk pressure for this small lab. The final design keeps the Wazuh Manager detection engine and consumes local JSON alerts directly.

## Connectivity Verification

Both required paths are now verified:

- Host-only communication from `SOC-WAZUH` to the Windows host at `192.168.56.1`
- Internet access through the NAT interface

Windows Firewall initially blocked inbound ICMP on the host-only adapter. A lab-scoped ICMPv4 inbound rule for `192.168.56.0/24` resolved the test without exposing the physical LAN.

## Next Step

Install only the `wazuh-manager` package. Do not install Wazuh Indexer, Wazuh Dashboard, or Filebeat in the final lightweight architecture.
