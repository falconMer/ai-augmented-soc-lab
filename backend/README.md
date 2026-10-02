# SOC Backend

The custom backend turns Wazuh alerts into a stable internal event model that can later be correlated, stored, enriched, risk-scored, and investigated by an AI agent.

## Current stage

Stage 1 implementation has started: **alert ingestion + normalization**.

The first modules intentionally use only the Python standard library. This lets us validate the data path before adding FastAPI, a database, threat-intelligence clients, or an LLM dependency.

### Files

- `soc_backend/models.py` — stable normalized alert schema
- `soc_backend/normalizer.py` — converts nested Wazuh JSON into the stable schema
- `soc_backend/reader.py` — scans Wazuh's JSON-lines alert file without loading it all into memory
- `scripts/inspect_alerts.py` — small CLI used to verify ingestion against real lab alerts

## First runtime verification

From the repository root on the Wazuh VM:

```bash
python3 backend/scripts/inspect_alerts.py \
  --rule 100100 \
  --rule 100101 \
  --last 4
```

The script should return normalized versions of the validated custom alerts. Runtime verification is still required before this stage is marked complete.

## Why normalize first

Later components should not depend directly on Wazuh's nested JSON layout. A stable internal schema makes correlation and storage easier to test and allows the backend to support additional telemetry sources in the future without rewriting every downstream component.
