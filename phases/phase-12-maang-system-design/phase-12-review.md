# Phase 12 Review: MAANG-Level System Design

## 1. Phase Summary

Phase 12 is where the Big Data pieces become complete architectures.

The core idea:

```text
requirements drive architecture
  -> scale drives ingestion and storage choices
  -> latency drives streaming and serving choices
  -> correctness drives reconciliation and governance
  -> failure handling proves maturity
```

If you remember only one sentence:

```text
A strong data system design answer explains data flow, scale, trade-offs, and failure behavior before naming tools.
```

## 2. Universal System Design Skeleton

Use this flow in every interview:

1. Clarify product goal.
2. List functional requirements.
3. List non-functional requirements.
4. Estimate scale.
5. Define events/APIs.
6. Define data model.
7. Draw high-level architecture.
8. Explain data flow.
9. Deep dive core components.
10. Explain scaling and partitioning.
11. Explain consistency and correctness.
12. Explain failure handling.
13. Add monitoring, cost, and security.
14. Explain trade-offs.
15. Finish with a crisp final answer.

## 3. Product Analytics Designs

| System | Main Data | Serving Need | Biggest Trap |
|---|---|---|---|
| YouTube analytics | playback and engagement events | creator dashboards, ML, BI | treating live views as final exact counts |
| Netflix viewing analytics | playback sessions and QoE telemetry | content metrics, quality alerts, recommendations | ignoring sessionization and heartbeat volume |
| LinkedIn feed analytics | impressions plus engagement | ranking feedback and experiments | not logging ranking context |
| Amazon clickstream | product views, search, cart, purchase | funnels, personalization, attribution | treating purchases like loose page views |

Reusable pattern:

```text
client events
  -> event gateway
  -> Kafka/Pub/Sub
  -> stream hot metrics/features
  -> lakehouse raw/silver/gold
  -> OLAP/warehouse/feature store
```

## 4. Real-Time Operational Designs

| System | Low-Latency Need | Correctness Need |
|---|---|---|
| fraud detection | approve/deny/review quickly | audit decisions and labels |
| ad analytics | pacing and live advertiser dashboards | billing reconciliation |
| real-time dashboard | fresh business metrics | freshness display and finalization |
| metrics monitoring | alerts and SLOs | avoid missing health signals |
| Uber location | latest driver/rider state | fresh geospatial matching |

Strong line:

```text
The live path optimizes freshness; the batch/reconciliation path optimizes correctness.
```

## 5. Enterprise Platform Designs

| System | Main Priority |
|---|---|
| enterprise data lake | governed shared storage |
| finance warehouse | accuracy, reconciliation, auditability |
| MySQL CDC to lakehouse | reliable database change replication |
| batch + streaming hybrid | fast live metrics plus accurate final metrics |

Enterprise designs should always mention:

- ownership
- governance
- lineage
- access control
- retention
- quality checks
- cost controls
- incident response

## 6. Common Architecture Choices

| Need | Common Choice |
|---|---|
| high-volume event ingestion | Kafka, Kinesis, Pub/Sub |
| replayable raw history | lakehouse/object storage |
| low-latency dashboard slicing | Druid, Pinot, ClickHouse |
| official business reporting | warehouse/lakehouse gold tables |
| ML training features | offline feature store |
| low-latency ML serving features | online feature store |
| logs search | OpenSearch/Elasticsearch/Loki/Splunk style systems |
| metrics alerting | Prometheus/TSDB style systems |
| database updates | CDC with Debezium/binlog/WAL |

## 7. Partitioning Cheat Sheet

| Workload | Partition By |
|---|---|
| video analytics | event_date, video_id, event_type |
| clickstream sessionization | user_id/session_id |
| feed joins | impression_id |
| location matching | city_id/geocell |
| campaign analytics | campaign_id and time |
| metrics | time-series hash and time |
| lakehouse tables | date plus common filter columns |
| CDC streams | table and primary key |

Avoid:

```text
partitioning by a high-cardinality column that creates tiny files
or by a low-cardinality column that creates hot partitions
```

## 8. Correctness Checklist

Ask these questions:

- What is the source of truth?
- Are events duplicated?
- Can events arrive late?
- Can events arrive out of order?
- Are deletes/updates required?
- Is live data approximate?
- What is the finalized data path?
- Can we replay from raw data?
- How do we reconcile?
- How do we audit decisions or reports?

## 9. Failure Checklist

Always cover:

- producer retry
- broker/stream lag
- consumer failure
- checkpoint restore
- dead letter queue
- schema changes
- duplicate events
- late events
- serving store outage
- stale dashboard/model features
- backfill/replay

## 10. Monitoring Checklist

For every data architecture, monitor:

- ingestion rate
- error rate
- lag
- freshness
- completeness
- duplicate rate
- late-event rate
- processing duration
- query latency
- storage growth
- cost
- quality checks

Strong distinction:

```text
Pipeline health means jobs are running.
Data health means outputs are fresh, complete, and correct enough.
```

## 11. Security Checklist

Mention:

- authentication and authorization
- least privilege
- encryption in transit and at rest
- PII/PHI/sensitive classification
- masking/tokenization where needed
- audit logs
- retention and deletion
- tenant/team isolation

## 12. Common Interview Traps

| Trap | Better Answer |
|---|---|
| jumping to tools immediately | start with requirements and scale |
| no capacity estimate | give rough order-of-magnitude numbers |
| no raw replay layer | keep immutable raw events where possible |
| no dedupe plan | use event_id/order_id/transaction_id |
| no late-event plan | use watermarks and correction/backfill |
| no failure path | explain degraded mode and recovery |
| no cost discussion | partition, compact, tier, pre-aggregate |
| no security discussion | protect raw sensitive data and audit access |
| no final vs live distinction | separate approximate live and reconciled final |

## 13. Fast Recall

```text
YouTube = playback events -> hot metrics + lakehouse + creator analytics.
Netflix = viewing sessions + QoE telemetry + recommendations.
Uber = moving dots -> geocell latest state + historical lake.
LinkedIn = impression context + engagement + experiments.
Amazon = clickstream footsteps + funnels + personalization.
Fraud = features + rules + model + decision audit.
Ads = impressions/clicks/conversions + pacing + billing.
Logs = service diaries into searchable storage.
Metrics = time-series health numbers and alerts.
Features = offline training + online serving.
Enterprise lake = governed bronze/silver/gold.
Finance warehouse = reconciled official numbers.
CDC = binlog changes into lakehouse MERGE.
Dashboard = stream aggregates + OLAP + freshness.
Hybrid = live scoreboard + official scorebook.
```

## 14. Practice Prompt

Take any Phase 12 topic and answer it in this 10-minute format:

```text
1 minute: requirements
1 minute: scale
2 minutes: architecture
2 minutes: data model and flow
2 minutes: scaling/correctness/failures
1 minute: monitoring/security/cost
1 minute: trade-offs and final summary
```

