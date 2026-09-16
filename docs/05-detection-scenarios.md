# Detection Scenarios

> Status: planned

Each scenario must document the objective, source and target systems, expected telemetry, MITRE ATT&CK mapping, actual detection result, evidence, and limitations.

## Planned Scenarios

- Network reconnaissance / service discovery
- Repeated authentication failures
- Suspicious PowerShell execution
- New local user creation
- Privileged group modification
- Suspicious outbound connection
- Persistence-related activity
- Active Directory scenarios after `DC01` is added

## Scenario Quality Rule

A scenario is not considered complete just because an alert fired. The write-up should explain what was observed, what was missed, false-positive considerations, and how the detection could be improved.

See [`../attack-simulations/README.md`](../attack-simulations/README.md) for the scenario template.
