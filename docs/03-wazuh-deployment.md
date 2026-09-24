# Wazuh Deployment

> Status: full-stack prototype completed; lightweight manager-only Wazuh deployment running

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
evidence/wazuh/03-manager-only-service-verification.txt
evidence/wazuh/04-local-alert-pipeline-verification.txt
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

### Runtime verification

The manager-only deployment was started successfully on 2026-09-24:

- `wazuh-manager.service` is enabled and `active (running)`.
- Startup completed with `status=0/SUCCESS`.
- Wazuh core processes including `wazuh-analysisd`, `wazuh-remoted`, `wazuh-authd`, `wazuh-db`, `wazuh-logcollector`, `wazuh-monitord`, `wazuh-syscheckd`, `wazuh-modulesd`, and `wazuh-apid` are running.
- Cluster mode remains disabled by design.
- Mail, agentless, integration, and syslog forwarding daemons are not running because they are not required for this lab.
- Observed manager memory usage shortly after startup: approximately `706.6 MiB`, with a peak of `725.9 MiB`.

This confirms the lightweight redesign is substantially smaller than the earlier all-in-one deployment.

### Local alert pipeline verification

The manager-only deployment is successfully generating local alerts:

- `/var/ossec/logs/alerts/alerts.json` exists and was actively growing.
- JSON alerts include parsed rule metadata, MITRE ATT&CK mappings, source event data, agent/manager metadata, and the original log.
- Example manager-local detections included successful sudo activity, PAM session events, and listening-port changes.
- The manager's own network telemetry confirmed listeners on:
  - `1514/TCP` — `wazuh-remoted`
  - `1515/TCP` — `wazuh-authd`
  - `55000/TCP` — Wazuh API

This validates the core interface for the custom SOC backend: Wazuh can perform local decoding/rule evaluation and produce JSON alerts without Indexer, Dashboard, or Filebeat.

### Resource observation

At this point the guest reported approximately 1.2 GiB RAM in use. The VM itself is still allocated about 8 GiB RAM and has a 40 GiB guest filesystem, which is larger than the final target. The manager-only service footprint leaves enough headroom to reduce the VM allocation later.

### Next Step

Reduce the VM RAM allocation to the final target if desired, then enroll the Windows endpoint against manager address `192.168.56.10` and verify that endpoint-generated alerts appear in `alerts.json`.
