# Evaluation

> Status: planned

The project will be evaluated on more than whether the software runs.

## Candidate Metrics

| Metric | Purpose |
|---|---|
| Detection coverage | Which simulated behaviors produced useful telemetry/alerts? |
| False-positive rate | How often does the pipeline escalate normal activity? |
| IOC extraction accuracy | Are relevant indicators extracted correctly? |
| ATT&CK mapping accuracy | Are techniques mapped correctly? |
| Correlation quality | Does the system connect related events without over-grouping? |
| AI classification quality | Does the agent reach evidence-supported conclusions? |
| Report completeness | Does the generated report preserve the useful evidence? |
| Triage time | How much time is saved compared with manual review? |

## Test Method

Each controlled scenario should have an expected outcome recorded before execution. Actual results will then be compared against that expectation.

## Important Limitation

LLM confidence values are not treated as calibrated probabilities. They are descriptive outputs and must be checked against evidence.
