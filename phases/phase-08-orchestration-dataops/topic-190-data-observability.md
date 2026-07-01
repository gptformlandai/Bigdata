# Topic 190: Data Observability

## 1. Goal

Understand data observability as the ability to detect, diagnose, and prevent data issues.

## 2. Baby Intuition

Data observability is like health monitoring for your data platform.

It tells you when data is late, missing, broken, strange, or unreliable.

## 3. What It Is

- Simple definition: Data observability monitors the health of data and pipelines.
- Technical definition: Data observability collects and analyzes metadata, metrics, logs, lineage, quality signals, freshness, volume, schema, and anomalies to detect and troubleshoot data reliability issues.
- Category: Data reliability and operations.
- Related terms: freshness, volume, schema, lineage, quality, anomaly detection, incident, alert.

## 4. Why It Exists

Data problems are often silent:

- dashboard stale
- table empty
- schema changed
- null rate spiked
- row count dropped
- pipeline succeeded with wrong data
- upstream source changed

Observability helps teams know before users complain.

## 5. Where It Fits In A Data Platform

```text
pipelines + tables + logs + metadata + lineage
  -> observability system
  -> alerts, dashboards, root-cause analysis
```

## 6. How It Works Step By Step

1. Collect metadata from orchestrators, warehouses, lakes, and catalogs.
2. Track freshness and pipeline runs.
3. Track table volume and schema changes.
4. Monitor quality metrics and anomalies.
5. Use lineage to identify upstream/downstream impact.
6. Alert owners when important issues occur.
7. Support incident investigation and prevention.

## 7. How To Use It Practically

Common observability pillars:

| Pillar | Example |
|---|---|
| freshness | table updated on time |
| volume | row count normal |
| schema | no unexpected column/type changes |
| quality | nulls/duplicates/ranges within limits |
| lineage | upstream/downstream impact |
| performance | pipeline/query duration |

## 8. Real-World Scenario

- Product/system: Executive revenue dashboard.
- Problem: Upstream payments table stopped updating but downstream job still succeeded using old data.
- How observability helps: freshness alert detects stale input before dashboard users notice.
- What would go wrong without it: executives make decisions from stale revenue.

## 9. System Design Angle

Mention data observability when:

- pipelines are business-critical
- data quality incidents hurt trust
- many dependencies exist
- lineage/root cause matters
- on-call needs useful alerts

Important:

```text
Observability is not only task logs; it includes data health.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| detects issues earlier | tool setup and cost |
| improves trust | noisy alerts if poorly tuned |
| helps root cause | needs metadata access |
| shows lineage impact | ownership must be defined |

## 11. Failure Modes

- Failure: Alert noise.
- Symptom: teams ignore alerts.
- Recovery: tune severity/thresholds.
- Prevention: alert on user/business impact.

- Failure: Missing lineage.
- Symptom: hard to find impacted dashboards.
- Recovery: add lineage integration.
- Prevention: standardized pipelines.

- Failure: Monitoring only tasks.
- Symptom: successful pipeline with bad data.
- Recovery: add data checks.
- Prevention: monitor freshness, volume, schema, quality.

## 12. Common Mistakes

- Mistake: Treating observability as a dashboard only.
- Why it is wrong: it must alert and support action.
- Better approach: connect monitoring to ownership and incident process.

- Mistake: Alerting on every minor anomaly.
- Why it is wrong: creates fatigue.
- Better approach: severity based on criticality and users.

## 13. Mini Example

```text
Dataset: orders_gold
freshness: updated within 30 minutes
volume: daily row count within historical range
schema: no breaking changes
quality: order_id unique and not null
lineage: feeds revenue_dashboard
```

## 14. Interview Questions

1. What is data observability?
2. How is it different from pipeline monitoring?
3. What signals do you track?
4. Why does lineage matter?
5. How do you reduce alert noise?

## 15. Interview Speak

"Data observability monitors the health of datasets and pipelines using freshness, volume, schema, quality, lineage, performance, and anomaly signals. It helps detect issues before users do and supports root-cause analysis through ownership and lineage."

## 16. Quick Recall

- One-line summary: Data observability tells you whether data is healthy.
- Three keywords: freshness, quality, lineage.
- One trap: Monitoring only task success.
- One memory trick: Health check for data products.
