# ADR-001: Replace Full Wazuh SIEM with Manager-Only Detection Architecture

**Status:** Accepted  
**Context:** Resource-constrained portfolio lab

## Decision

Use Wazuh Manager without Wazuh Indexer/OpenSearch, Wazuh Dashboard, or Filebeat in the final lab.

The Wazuh Agent and Sysmon remain on the Windows endpoint. Wazuh Manager performs endpoint communication, decoding, rule evaluation, and alert generation. A custom Python/FastAPI platform consumes `/var/ossec/logs/alerts/alerts.json` directly and provides storage, correlation, enrichment, AI investigation, and visualization.

## Context

The project runs on a laptop with:

- 16 GB RAM
- AMD Ryzen 5 4650U
- approximately 50 GB free disk at project start

A full Wazuh all-in-one prototype was successfully deployed and validated. However, the Indexer/OpenSearch and Dashboard created significant resource pressure relative to the small number of endpoints in the lab.

## Reasons

1. The project needs Wazuh's collection and detection capabilities more than a heavyweight search cluster.
2. Local Wazuh JSON alerts provide a clean interface to the custom SOC backend.
3. Removing OpenSearch substantially reduces RAM and disk pressure.
4. A custom investigation layer better demonstrates Python, automation, AI, correlation, and security engineering.
5. Full Wazuh experience is still demonstrated by the completed prototype retained in repository history and evidence.

## Consequences

### Positive

- Lower RAM and disk requirements
- Faster VM startup and recovery
- More resources available for ATTACKER01 and future DC01 scenarios
- More engineering work moves into portfolio-owned code
- Easier reproducibility on ordinary student hardware

### Tradeoffs

- No native Wazuh Dashboard in the final architecture
- No indexed historical search through OpenSearch
- Custom backend must implement its own alert persistence and querying
- Some Wazuh features that depend on the indexer/dashboard will not be the focus of the final lab

## Storage Strategy

The final backend will store only normalized alerts/incidents needed for experiments in SQLite or DuckDB. Raw Wazuh alert files will be retained for short, bounded windows and rotated to protect disk space.

## Validation Criteria

The redesign is successful when:

- Windows agent communicates with Wazuh Manager
- Sysmon events reach the manager
- Wazuh generates alerts in `alerts.json`
- Python backend ingests those alerts
- At least three controlled scenarios produce reproducible incidents
- AI analysis is grounded in correlated evidence
