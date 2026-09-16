# Windows Telemetry

> Status: not started

## Goal

Onboard the Windows endpoint into Wazuh and collect useful endpoint telemetry using Windows Event Logs and Sysmon.

## Planned Flow

```text
Windows endpoint
    ↓
Sysmon + Windows Event Logs
    ↓
Wazuh Agent
    ↓
Wazuh Manager
    ↓
Searchable alerts / telemetry
```

## Validation Checklist

- [ ] Wazuh Windows agent installed
- [ ] Agent appears active in dashboard
- [ ] Sysmon installed
- [ ] Sysmon operational channel collected by Wazuh
- [ ] Process creation visible
- [ ] Authentication events visible
- [ ] Network-related events visible where configured

## Baseline Activity

Before attack simulations, capture normal activity such as ordinary PowerShell use, browser activity, file creation, and sign-in activity. This baseline will later help distinguish suspicious behavior from normal events.

## Evidence

Save only sanitized screenshots/configuration examples. Never commit credentials, personal data, or unrelated private host information.
