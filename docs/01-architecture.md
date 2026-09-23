# Architecture

> Status: final lightweight design selected

## Objective

Build a compact SOC lab that preserves realistic endpoint collection and detection while moving correlation, enrichment, investigation, and visualization into a custom lightweight platform.

## Final Topology

```mermaid
flowchart LR
    A[ATTACKER01\n192.168.56.20] -->|Controlled activity| W[Windows Host\n192.168.56.1\nSysmon + Wazuh Agent]
    W -->|1514/TCP telemetry| Z[SOC-WAZUH\n192.168.56.10\nWazuh Manager only]
    Z --> J[/var/ossec/logs/alerts/alerts.json]
    J --> B[FastAPI ingestion]
    B --> D[SQLite / DuckDB]
    B --> C[Correlation / IOC / TI / MITRE / Risk]
    C --> L[AI investigation agent]
    L --> U[Lightweight SOC dashboard]
    U --> H[Analyst review]
```

## Why Manager-Only Wazuh

The first prototype used the conventional all-in-one Wazuh architecture: Manager + Filebeat + Indexer/OpenSearch + Dashboard. It was successfully deployed, but the indexing and visualization stack consumed too much RAM and disk for the available laptop resources.

The final architecture retains Wazuh Manager because it provides real endpoint enrollment, decoding, rules, alert generation, and security operations experience. It removes the Indexer, Dashboard, and Filebeat because the project does not need a heavyweight search cluster to analyze a few lab endpoints.

Wazuh Manager writes alerts locally to `/var/ossec/logs/alerts/alerts.json`. The custom backend will consume that file directly.

## Component Responsibilities

### Windows host

- Sysmon telemetry
- Windows Security/System/Application event logs
- Wazuh Agent
- Primary monitored endpoint

### Wazuh Manager

- Agent enrollment and communication
- Event decoding
- Wazuh rule evaluation
- Custom detection rules
- Local JSON alert generation

### Python SOC backend

- Tail/ingest Wazuh JSON alerts
- Normalize alert schema
- Correlate related activity
- Extract IOCs
- Query threat-intelligence sources
- Map evidence to MITRE ATT&CK
- Calculate deterministic risk scores
- Persist incidents in a lightweight local database

### AI investigation agent

The LLM receives an evidence package and uses bounded tools such as:

- `get_related_events()`
- `get_host_history()`
- `get_user_history()`
- `lookup_ip()`
- `lookup_hash()`
- `search_mitre()`

The AI explains evidence and proposes actions. It does not autonomously isolate systems, block addresses, or disable accounts in the initial version.

## Resource Targets

| Component | RAM target | Disk target |
|---|---:|---:|
| `SOC-WAZUH` | ~3 GB | ~15 GB dynamic |
| `ATTACKER01` | 1.5–2 GB | 8–10 GB dynamic |
| Python backend | Runs on host or SOC VM | Small |
| SQLite/DuckDB | Runs with backend | Small and bounded |

## Network

Host-only lab network: `192.168.56.0/24`

- Windows host: `192.168.56.1`
- SOC-WAZUH: `192.168.56.10`
- ATTACKER01: `192.168.56.20`
- DC01 later: `192.168.56.30`

Each VM uses NAT for Internet access and Host-only networking for isolated lab traffic.

## Design Principles

- Preserve real defensive tooling where it adds portfolio value.
- Avoid infrastructure that does not improve the experiment.
- Keep storage bounded and observable.
- Use deterministic logic for risk scoring.
- Use AI for investigation and explanation rather than unbounded remediation.
- Keep the LLM provider replaceable.
- Store no credentials or secrets in Git.
- Maintain human approval for response actions.

## Historical Prototype

The repository retains evidence of the completed full Wazuh deployment. The final lightweight architecture is an optimization based on measured resource constraints rather than a replacement of untested technology.
