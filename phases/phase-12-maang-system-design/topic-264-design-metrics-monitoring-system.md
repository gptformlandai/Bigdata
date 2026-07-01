# Topic 264: Design Metrics Monitoring System

## 1. Goal

Design a system that collects numeric metrics, stores time series, powers dashboards, and triggers alerts.

## 2. Baby Intuition

Metrics monitoring is the health dashboard of a platform.

It tracks numbers like:

```text
requests/sec, error rate, latency, CPU, Kafka lag, data freshness
```

## 3. Requirements

Clarify:

- Are metrics for infrastructure, applications, data pipelines, or all?
- Pull model, push model, or both?
- What retention and resolution are needed?
- What alerting latency is acceptable?
- How many services/metrics/labels?

## 4. Functional Requirements

- collect counters, gauges, and histograms
- store metrics as time series
- support queries by time range and labels
- power dashboards
- evaluate alert rules
- support SLO/error-budget alerts
- downsample and retain historical metrics

## 5. Non-Functional Requirements

- high write throughput
- low query latency for recent metrics
- high availability for alerting
- cardinality control
- multi-tenant access and quotas
- efficient compression
- self-monitoring

## 6. Capacity Estimation

Example:

```text
100K hosts/services
1,000 active series per host/service
= 100M active time series

sample every 15 seconds
= about 6.7M samples/sec
```

The dangerous number is active time series count, not just raw sample size.

## 7. Events And APIs

Metric sample:

```text
http_requests_total{service="checkout", env="prod", status="500"} 12345 timestamp
```

Common metric types:

- counter
- gauge
- histogram

Query example:

```text
error_rate = rate(errors_total[5m]) / rate(requests_total[5m])
```

## 8. Data Model

Time series identity:

```text
metric_name + labels = unique series
```

Example:

```text
metric_name: pipeline_freshness_minutes
labels: pipeline=orders, env=prod
samples: [(time1, value1), (time2, value2)]
```

## 9. High-Level Architecture

```text
apps/jobs/hosts
  -> metrics endpoint or push gateway
  -> scraper/collector
  -> time-series database
  -> query API
  -> dashboards
  -> alert evaluator
  -> notification system
```

## 10. Data Flow

1. Service exposes metrics endpoint or pushes samples.
2. Collector scrapes/receives samples.
3. Samples are validated and relabeled.
4. TSDB stores compressed time-series blocks.
5. Query engine executes time-window queries.
6. Alert evaluator runs rules periodically.
7. Alert manager deduplicates and routes notifications.
8. Old data is downsampled or deleted.

## 11. Deep Dive Components

Cardinality:

```text
service + status is good
service + status + user_id is dangerous
```

SLO alerting:

- define good events and total events
- calculate error budget
- alert when burn rate is too high

Data platform metrics:

- pipeline freshness
- record count
- failed records
- consumer lag
- query latency
- table size growth

## 12. Scaling And Partitioning

- Shard time series by metric name/label hash.
- Replicate data for availability.
- Keep recent metrics hot.
- Downsample older metrics.
- Limit labels and active series per tenant.
- Use remote write or long-term stores for scale.

## 13. Consistency And Correctness

- Metrics are usually eventually consistent.
- Missing samples should be visible.
- Alerting needs high availability.
- Duplicate samples can be deduped by timestamp/series.
- Avoid high-cardinality labels that overwhelm storage.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| collector down | redundant collectors |
| TSDB shard down | replication and failover |
| alert evaluator down | HA alerting pair |
| cardinality explosion | reject/drop bad series |
| missing data | alert on absent metrics |

## 15. Monitoring, Cost, And Security

Monitor the monitoring system:

- scrape success
- samples/sec
- active series
- query latency
- alert evaluator health
- dropped samples

Cost:

- enforce cardinality limits
- downsample older data
- compact time-series blocks
- avoid unnecessary labels

Security:

- restrict metric query access by tenant/team
- avoid putting sensitive values in labels
- audit admin actions

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| high scrape frequency | more precise alerts | more storage/write cost |
| long retention at full resolution | detailed history | expensive |
| downsampling | cheaper history | loses detail |
| high-cardinality labels | flexible slicing | storage explosion |

## 17. Interview-Ready Final Answer

"I would design metrics monitoring around time-series ingestion and alerting. Services expose counters, gauges, and histograms, collectors scrape or receive samples, and a TSDB stores compressed time-series data. Dashboards query recent and historical data, while an alert evaluator checks SLO and threshold rules. I would shard by time-series hash, replicate for availability, downsample old data, and enforce cardinality limits. The biggest risks are high-cardinality labels, missing metrics, noisy alerts, and the monitoring system not monitoring itself."

## 18. Quick Recall

- One-line summary: Metrics monitoring stores platform health numbers over time.
- Core tools: collectors, TSDB, dashboards, alert manager.
- Main trap: user_id or request_id as metric labels.
- Memory trick: health dashboard with a time axis.

