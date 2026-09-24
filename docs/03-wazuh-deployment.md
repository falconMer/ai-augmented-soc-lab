# Wazuh Deployment

> Status: full-stack prototype completed; lightweight manager-only rebuild in progress

## Goal

Document both the completed all-in-one Wazuh prototype and the final resource-optimized manager-only deployment used by the project.

## Prototype Environment

| Item | Value |
|---|---|
| VM role | `SOC-WAZUH` |
| Guest hostname observed in logs | `smail-virtualbox` |
| OS | Lubuntu 24.04 LTS (Ubuntu Noble base) |
| Lab IP | `192.168.56.10` |
| Deployment | All-in-one |
| Wazuh version | `4.14.7` |
| Filebeat version | `7.10.2-2` |

## Installation Method

The Wazuh 4.14 installation assistant was used:

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
sudo bash ./wazuh-install.sh -a
```

Generated passwords, certificates, API credentials, and the contents of `wazuh-install-files.tar` are intentionally excluded from the repository.

## Verified Components

After the VM recovered from an installation-time crash/reboot, the following services were verified with `systemctl`:

- [x] `wazuh-manager` — active (running)
- [x] `wazuh-indexer` — active (running)
- [x] `wazuh-dashboard` — active (running)
- [x] `filebeat` — active (running)

Installed packages were also verified:

- `wazuh-manager 4.14.7-1`
- `wazuh-indexer 4.14.7-1`
- `wazuh-dashboard 4.14.7-1`
- `filebeat 7.10.2-2`

The dashboard process was confirmed listening on TCP port `443` on `0.0.0.0`.

The dashboard was then accessed successfully from the Windows host at `https://192.168.56.10`. After an initial backend timeout while the services were warming up, the Wazuh Overview loaded successfully and showed the expected fresh-instance state with no agents registered.

## Validation Checklist

- [x] Wazuh manager service running
- [x] Wazuh indexer service running
- [x] Wazuh dashboard service running
- [x] Filebeat service running
- [x] Wazuh packages installed
- [x] Dashboard listening on TCP/443
- [x] Dashboard login verified from Windows host
- [x] Dashboard Overview loads successfully
- [ ] First endpoint agent enrolled
- [ ] Disk usage checked after installation

## Evidence

Sanitized evidence is stored under:

```text
evidence/wazuh/01-service-verification.txt
evidence/wazuh/02-dashboard-access-verification.txt
```

Credentials, tokens, private keys, and certificate material are intentionally excluded.

## Problems / Fixes

### Attempt 1 — unsupported guest OS / slow manager restart

The first deployment attempt used a newer Lubuntu release whose Ubuntu base was outside the Wazuh recommended platform list. The manager initially started but later exceeded the systemd startup timeout during the installer's post-configuration restart.

**Resolution:** Rebuilt the Wazuh VM on Lubuntu 24.04 LTS.

### Attempt 2 — interrupted Wazuh indexer download

On Lubuntu 24.04 LTS, the installer failed while downloading the large `wazuh-indexer` package from `packages.wazuh.com` with an input/output read error.

**Resolution:** Re-added the Wazuh APT repository and pre-fetched the indexer package with APT retry handling:

```bash
sudo apt-get -o Acquire::Retries=10 --download-only install wazuh-indexer
```

The installation assistant was then rerun.

### Attempt 3 — VM crash near the end of installation

During the successful package deployment, the VM crashed after the dashboard, indexer, manager, and Filebeat had been installed and configured. The installer log ended around a daemon reload timeout instead of printing its normal final summary.

After reboot, all four services started successfully, the packages were present, and the dashboard was listening on TCP/443.

### Initial dashboard timeout

The first dashboard load returned a 20-second backend timeout. No reinstall was performed. After the Wazuh services had additional startup time, the Overview loaded normally from the Windows host.

## Final Lightweight Deployment

The final lab was rebuilt on Lubuntu 24.04 LTS with only the `wazuh-manager` package. The heavy Indexer/OpenSearch, Dashboard, and Filebeat components are intentionally omitted.

### Package installation verification

On 2026-09-24, package state was verified after a potentially interrupted install:

- `dpkg -l` reported `ii  wazuh-manager 4.14.8-1`, confirming the package is fully installed.
- `dpkg --audit` returned no output, confirming there are no incomplete package configurations.
- `systemctl status wazuh-manager` showed the service is installed but currently `inactive (dead)` and disabled; this is a service-start state, not an incomplete package installation.
- `/var/log/dpkg.log` recorded the package reaching `status installed wazuh-manager:amd64 4.14.8-1`.

### Final architecture intent

Before starting the service, the manager configuration is adjusted for the no-indexer design:

- Wazuh Indexer connector disabled
- Vulnerability Detection disabled for the initial lightweight phase
- Wazuh Manager retained for agent communication, rules, decoding, and local JSON alert generation

### Next Step

Back up `/var/ossec/etc/ossec.conf`, disable the indexer connector and Vulnerability Detection module, then enable and start `wazuh-manager`. Verify service health and local alert generation before enrolling the Windows endpoint.
