# Detection Scenarios

> Status: first custom detection validated

Each scenario documents the objective, telemetry source, detection logic, ATT&CK mapping, validation result, limitations, and improvement ideas.

## Scenario 1 — Encoded PowerShell Execution

### Objective

Detect Windows PowerShell process creation when the command line uses `-enc` or `-EncodedCommand`.

### Source and target

- Source endpoint: `FALCON-PC`
- Telemetry source: Sysmon Event ID 1 — Process Create
- Collection: Wazuh Agent
- Detection engine: Wazuh Manager
- Custom rule ID: `100100`

### Detection logic

The rule is evaluated only for events already classified in the Wazuh `sysmon_event1` group.

It then requires both:

1. `win.eventdata.image` ends in `powershell.exe`
2. `win.eventdata.commandLine` contains `-enc` or `-EncodedCommand`

### MITRE ATT&CK

- `T1059.001` — PowerShell
- Tactic observed in the generated alert: Execution

### Controlled validation

A harmless PowerShell command was Base64-encoded and executed with `-EncodedCommand`.

Expected behavior:

```text
PowerShell process creation
  -> Sysmon Event ID 1
  -> Wazuh Agent
  -> Wazuh Manager
  -> custom rule 100100
  -> level 8 alert
```

### Result

The rule fired successfully.

Observed alert properties:

- rule ID: `100100`
- level: `8`
- description: `AI-SOC: PowerShell executed with an encoded command`
- agent: `FALCON-PC`
- Sysmon event ID: `1`
- process: `powershell.exe`
- integrity level: High
- MITRE technique: `T1059.001`
- group tags include `execution` and `suspicious_powershell`

### Evidence

Sanitized validation evidence:

```text
evidence/detections/01-encoded-powershell-detection.txt
```

![Wazuh alert for the encoded PowerShell detection rule](../screenshots/detections/01-encoded-powershell-rule-fired.png)

Rule source:

```text
detection-rules/ai_soc_rules.xml
```

### False-positive considerations

Encoded PowerShell is suspicious but not inherently malicious. Legitimate administration, software deployment, management tooling, and automation can also use encoded commands.

The rule is intentionally treated as a triage signal rather than proof of compromise.

### Possible improvements

Future correlation can increase confidence by combining this signal with:

- unusual parent process
- outbound network activity
- suspicious child processes
- execution from user-writable paths
- repeated encoded PowerShell executions
- known-bad IOC enrichment
- high-risk user or host context

## Planned Scenarios

- Network reconnaissance / service discovery
- Repeated authentication failures
- New local user creation
- Privileged group modification
- Suspicious outbound connection
- Persistence-related activity
- Active Directory scenarios after `DC01` is added

## Scenario Quality Rule

A scenario is not considered complete just because an alert fired. The write-up should explain what was observed, what was missed, false-positive considerations, and how the detection could be improved.
