# Windows Telemetry

> Status: Windows agent and Sysmon telemetry verified end-to-end

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
- [x] Agent confirmed Active with manager-side `agent_control`
- [x] Windows-generated alerts confirmed in manager `alerts.json`
- [x] Sysmon installed
- [x] Sysmon Operational channel collected by Wazuh
- [ ] Process creation visible
- [ ] Authentication events visible
- [ ] Network-related events visible where configured

## Baseline Activity

Before attack simulations, capture normal activity such as ordinary PowerShell use, browser activity, file creation, and sign-in activity. This baseline will later help distinguish suspicious behavior from normal events.

## Evidence

Sanitized enrollment evidence is stored at:

```text
evidence/windows/01-wazuh-agent-enrollment.txt
evidence/windows/02-sysmon-pipeline-verification.txt

Captured visual evidence also confirms:

- Windows `wazuhsvc` service is Running
- TCP connectivity to manager ports `1514` and `1515`
- Manager-side `agent_control -l` shows `FALCON-PC` as Active
- Windows-origin alert JSON is present in the manager alert stream
```

Never commit credentials, personal data, or unrelated private host information.



## Sysmon Verification

Sysmon was installed on the Windows endpoint and the Wazuh agent was configured to collect:

```text
Microsoft-Windows-Sysmon/Operational
```

The Windows agent log confirmed that Wazuh was analyzing the Sysmon Operational channel.

To verify the complete telemetry path, Wazuh raw JSON archiving was enabled temporarily, a harmless process event was generated on the Windows endpoint, and the manager archive was queried for Sysmon events from `FALCON-PC`.

The manager received a Sysmon Event ID 5 (process termination) from agent `001`, including:

- provider: `Microsoft-Windows-Sysmon`
- endpoint: `FALCON-PC`
- source IP: `192.168.56.1`
- channel: `Microsoft-Windows-Sysmon/Operational`
- process image: `C:\Windows\System32\conhost.exe`
- user: `FALCON-PC\HP`

This confirms the end-to-end path:

```text
Windows process activity
    -> Sysmon
    -> Windows Event Channel
    -> Wazuh Agent
    -> Wazuh Manager
    -> archives.json / rules pipeline
```

Raw event archiving is intended only for short verification windows because the final lab is disk constrained. The normal operating mode keeps `logall_json` disabled.
