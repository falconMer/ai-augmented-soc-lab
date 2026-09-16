# AI Investigation Pipeline

> Status: planned

## Goal

Create an evidence-based investigation pipeline in which deterministic security processing happens before the LLM is asked to interpret an incident.

```text
Wazuh alert
  ↓
Normalization
  ↓
IOC extraction
  ↓
Historical event correlation
  ↓
Threat-intelligence enrichment
  ↓
MITRE ATT&CK mapping
  ↓
Deterministic risk score
  ↓
Evidence package
  ↓
AI investigation agent
  ↓
Analyst review
```

## Planned Agent Tools

- `get_related_events()`
- `get_host_history()`
- `get_user_history()`
- `lookup_ip()`
- `lookup_hash()`
- `query_wazuh()`
- `search_mitre()`
- `get_asset_information()`

## Output Requirements

The LLM should return validated structured output containing at least:

- classification
- confidence
- concise summary
- evidence references
- ATT&CK techniques
- recommended actions
- false-positive indicators
- suggested follow-up queries

## Safety Design

The AI may recommend remediation, but actions such as disabling accounts, blocking addresses, or isolating hosts remain analyst-approved.
