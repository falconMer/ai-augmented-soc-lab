# Wazuh Deployment

> Status: installed / core services verified after reboot

## Goal

Deploy an all-in-one Wazuh environment containing the manager, indexer, dashboard, and Filebeat on the `SOC-WAZUH` Lubuntu VM.

## Environment

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

## Validation Checklist

- [x] Wazuh manager service running
- [x] Wazuh indexer service running
- [x] Wazuh dashboard service running
- [x] Filebeat service running
- [x] Wazuh packages installed
- [x] Dashboard listening on TCP/443
- [ ] Dashboard login verified from Windows host
- [ ] Indexer/API health verified from the lab network
- [ ] Disk usage checked after installation

## Evidence

Sanitized command output is stored under:

```text
evidence/wazuh/01-service-verification.txt
```

Future screenshots should show the dashboard and service health without exposing credentials.

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

After reboot, all four services started successfully, the packages were present, and the dashboard was listening on TCP/443. The deployment is therefore treated as operational, pending browser login and network-level validation.

## Next Validation

1. Open `https://192.168.56.10` from the Windows host.
2. Accept the expected self-signed certificate warning.
3. Log in with the locally stored `admin` credentials.
4. Capture a sanitized dashboard screenshot.
5. Verify disk and memory usage.
