# Topic 251: Metrics Platform

## 1. Goal

Understand how large companies collect, store, query, and alert on metrics.

## 2. Baby Intuition

A metrics platform is like a health monitor for software.

It continuously watches numbers like request count, latency, error rate, CPU usage, job duration, and pipeline freshness.

## 3. What It Is

- Simple definition: A metrics platform stores time-based numbers from systems.
- Technical definition: A metrics platform ingests numeric measurements, stores them as time series, supports fast time-window queries, and powers dashboards, alerts, SLOs, and capacity planning.
- Category: Observability/data platform component.
- Related terms: time series, counter, gauge, histogram, labels/tags, Prometheus, OpenTelemetry, SLO, alerting.

## 4. Why It Exists

Production systems need answers like:

- Is the service healthy?
- Are errors increasing?
- Is Kafka consumer lag growing?
- Is yesterday's data pipeline late?
- Is query latency above the SLO?
- Are we running out of disk/memory?

Logs are detailed but noisy. Metrics are compact numbers that can be graphed and alerted on quickly.

## 5. Where It Fits In A Data Platform

```text
apps, jobs, databases, Kafka, Spark, Airflow
  -> metric emitters/exporters
  -> collector/scraper
  -> metrics storage
  -> dashboards, alerts, SLO reports
```

Common tools:

| Area | Examples |
|---|---|
| instrumentation | OpenTelemetry, Prometheus client libraries |
| collection | Prometheus, OpenTelemetry Collector |
| long-term storage | Thanos, Cortex, Mimir, M3 |
| dashboarding | Grafana |
| alerting | Alertmanager, cloud monitoring alerts |

## 6. How It Works Step By Step

1. Application or platform emits metrics.
2. Metrics are tagged with labels like service, environment, region, and status.
3. Collector scrapes or receives metrics.
4. Storage writes metric samples by timestamp.
5. Query engine reads time windows.
6. Dashboards visualize trends.
7. Alert rules evaluate thresholds or SLO burn rate.
8. Old data is downsampled or expired.

## 7. How To Use It Practically

Common metric types:

| Type | Meaning | Example |
|---|---|---|
| counter | value only goes up | requests_total |
| gauge | value can go up/down | memory_used_bytes |
| histogram | distribution buckets | request_latency_seconds |
| summary | statistical summary | p95 latency |

Good data platform metrics:

- pipeline freshness
- records processed
- failed records
- job duration
- Kafka consumer lag
- query latency
- storage growth
- data quality pass/fail counts
- SLA/SLO status

## 8. Real-World Scenario

- Product/system: Real-time analytics pipeline.
- Problem: Team must know if streaming data is delayed.
- How metrics platform helps: Flink emits consumer lag, checkpoint duration, records per second, and failed records.
- What would go wrong without it: users see stale dashboards before engineers notice.

## 9. System Design Angle

Metrics platforms are used for:

- service health
- pipeline reliability
- SLO tracking
- alerting
- capacity planning
- cost visibility

Important design choice:

```text
high-cardinality labels can destroy metrics storage
```

Do not use unbounded labels like user_id, request_id, email, or order_id in metrics.

## 10. Trade-offs

| Pros | Cons |
|---|---|
| fast health visibility | loses event-level detail |
| compact storage compared to logs | cardinality can explode |
| powers alerts and SLOs | bad alerts create noise |
| easy trend analysis | approximate distributions |

## 11. Failure Modes

- Failure: Cardinality explosion.
- Symptom: metrics system becomes slow or expensive.
- Recovery: drop bad labels and compact storage.
- Prevention: metric label review and limits.

- Failure: Metrics collector down.
- Symptom: missing graphs and alerts.
- Recovery: restart collector and fill gaps if possible.
- Prevention: HA collectors and self-monitoring.

- Failure: Alert fatigue.
- Symptom: engineers ignore alerts.
- Recovery: tune alerts around user impact.
- Prevention: SLO-based alerting.

## 12. Common Mistakes

- Mistake: Putting user_id in metric labels.
- Why it is wrong: creates millions of unique time series.
- Better approach: use logs/traces for per-user debugging.

- Mistake: Alerting on every small spike.
- Why it is wrong: teams become numb to alerts.
- Better approach: alert on sustained user impact or SLO burn.

## 13. Mini Example

```text
Metric:
pipeline_records_processed_total{pipeline="orders", env="prod"} 150000

Alert:
pipeline_freshness_minutes{pipeline="orders"} > 30 for 10 minutes
```

## 14. Interview Questions

1. What is a metrics platform?
2. Counter vs gauge vs histogram?
3. Why is high cardinality dangerous?
4. How would you monitor a data pipeline?
5. What is an SLO-oriented alert?

## 15. Interview Speak

"A metrics platform collects numeric time-series signals from services, jobs, databases, and pipelines. I would use it for dashboards, SLOs, alerts, capacity planning, and pipeline freshness monitoring. The key risks are high-cardinality labels, missing metrics, noisy alerts, and lack of self-monitoring."

## 16. Quick Recall

- One-line summary: Metrics platforms store system health numbers over time.
- Three keywords: time series, labels, alerts.
- One trap: user_id as a metric label.
- One memory trick: Health monitor for software.

