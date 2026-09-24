# Windows Telemetry

> Status: Wazuh Windows agent installed and enrolled; manager-side active check pending

## Goal

Onboard the Windows endpoint into Wazuh and collect useful endpoint telemetry using Windows Event Logs and Sysmon.

## Current Flow

```text
Windows endpoint
    ↓
Windows Event Logs
    ↓
Wazuh Agent
    ↓
Wazuh Manager
    ↓
/var/ossec/logs/alerts/alerts.json
```

Sysmon will be added after baseline Wazuh agent connectivity is verified.

## Wazuh Agent Enrollment

The Windows agent was installed with Wazuh Agent 4.14.8 and configured to communicate with the manager at:

```text
192.168.56.10
```

The installer initially left `0.0.0.0` in the agent configuration, which caused the service to exit with:

```text
Invalid server address found: '0.0.0.0'
No client configured. Exiting.
```

The agent configuration was corrected to use `192.168.56.10`.

After correction, the Windows agent log confirmed:

- key request sent to `192.168.56.10`
- valid key received
- Windows Application, Security, and System event logs enabled
- File Integrity Monitoring started
- Security Configuration Assessment started
- Syscollector started
- Windows service `wazuhsvc` remained running

The agent registered with the manager using the endpoint hostname:

```text
FALCON-PC
```

A later manual `agent-auth` attempt returned `Duplicate agent name: FALCON-PC`, which is consistent with the agent having already been enrolled successfully.

## Validation Checklist

- [x] Wazuh Windows agent installed
- [x] Manager address corrected to `192.168.56.10`
- [x] Agent enrollment key received
- [x] Windows `wazuhsvc` service running
- [x] Application event log collection enabled
- [x] Security event log collection enabled
- [x] System event log collection enabled
- [ ] Agent confirmed Active with manager-side `agent_control`
- [ ] Windows-generated alerts confirmed in manager `alerts.json`
- [ ] Sysmon installed
- [ ] Sysmon Operational channel collected by Wazuh
- [ ] Process creation visible
- [ ] Authentication events visible
- [ ] Network-related events visible where configured

## Baseline Activity

Before attack simulations, capture normal activity such as ordinary PowerShell use, browser activity, file creation, and sign-in activity. This baseline will later help distinguish suspicious behavior from normal events.

## Evidence

Sanitized enrollment evidence is stored at:

```text
evidence/windows/01-wazuh-agent-enrollment.txt
```

Never commit credentials, personal data, or unrelated private host information.
