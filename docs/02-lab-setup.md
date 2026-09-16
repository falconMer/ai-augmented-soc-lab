# Lab Setup and Networking

> Status: not started

## Host Hardware

- CPU: AMD Ryzen 5 4650U
- RAM: 16 GB
- Available working disk: approximately 50 GB

## Virtual Machines

| VM | Role | RAM target | Disk target | Lab IP |
|---|---|---:|---:|---|
| `SOC-WAZUH` | Wazuh all-in-one SIEM | ~6 GB | ~25 GB dynamic | `192.168.56.10` |
| `ATTACKER01` | Controlled security-testing workstation | 1.5–2 GB | 10–12 GB dynamic | `192.168.56.20` |
| `DC01` (later) | Windows Server / Active Directory | ~3 GB | as space permits | `192.168.56.30` |

## Network Plan

Each VM will use:

1. **NAT adapter** for package downloads and updates.
2. **Host-only adapter** for isolated lab communication.

Planned lab network: `192.168.56.0/24`.

The Windows host-only adapter IP must be verified with `ipconfig` before documenting it as final.

## Validation Checklist

- [ ] Host-only network created
- [ ] Wazuh VM receives planned lab IP
- [ ] Testing VM receives planned lab IP
- [ ] Windows host can reach Wazuh VM
- [ ] Testing VM can reach Wazuh VM
- [ ] NAT connectivity works independently from the lab network

## Evidence to Capture

- VirtualBox network configuration
- `ipconfig` on Windows
- `ip -br address` on Lubuntu VMs
- Successful connectivity tests
