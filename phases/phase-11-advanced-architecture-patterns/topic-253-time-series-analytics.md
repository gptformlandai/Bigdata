# Topic 253: Time-Series Analytics

## 1. Goal

Understand analytics over data points ordered by time.

## 2. Baby Intuition

Time-series analytics is like watching a movie frame by frame.

Each measurement has a timestamp, and the important question is how values change over time.

## 3. What It Is

- Simple definition: Time-series analytics analyzes timestamped data.
- Technical definition: Time-series analytics stores, aggregates, and queries measurements/events by time, often using time partitions, tags, rollups, retention policies, and window functions.
- Category: Analytics pattern/storage workload.
- Related terms: TSDB, time bucket, rollup, downsampling, retention, tags, Prometheus, InfluxDB, TimescaleDB, ClickHouse, Druid, Pinot.

## 4. Why It Exists

Many questions are time-based:

- How many requests per minute?
- What was p95 latency yesterday?
- Which sensor crossed a threshold?
- How did revenue trend by hour?
- Did CPU usage spike after deployment?

Generic row storage can work at small scale, but high-volume time queries need time-aware layout and rollups.

## 5. Where It Fits In A Data Platform

```text
events/metrics/sensor readings/clicks
  -> ingestion
  -> time-partitioned storage
  -> rollups/downsampling
  -> dashboards, alerts, anomaly detection, reporting
```

## 6. How It Works Step By Step

1. Data arrives with timestamp, value, and tags.
2. System validates event time.
3. Data is partitioned by time window.
4. Optional indexes are built on tags/dimensions.
5. Queries filter by time range first.
6. Aggregations compute counts, sums, averages, percentiles, rates, or windows.
7. Old raw data may be downsampled or expired.

## 7. How To Use It Practically

Example record:

```text
timestamp=2026-07-02T10:01:00Z
metric=request_latency_ms
value=82
tags: service=checkout, region=us-east
```

Common queries:

| Query | Meaning |
|---|---|
| count per minute | traffic trend |
| avg by hour | smooth trend |
| p95 latency | user experience |
| rate of counter | requests/sec |
| moving average | reduce noise |
| anomaly detection | unusual behavior |

## 8. Real-World Scenario

- Product/system: IoT temperature monitoring.
- Problem: Millions of sensors send readings every few seconds.
- How time-series analytics helps: data is partitioned by time, rolled up by minute/hour, and queried for trends or threshold breaches.
- What would go wrong without it: queries over raw sensor rows become too slow and expensive.

## 9. System Design Angle

Important design decisions:

- write volume
- query latency
- retention period
- raw vs rolled-up data
- late or out-of-order events
- tag cardinality
- hot partition handling
- compression

Common storage choices:

- Prometheus-like TSDB for operational metrics
- InfluxDB/TimescaleDB for time-series apps
- ClickHouse/Druid/Pinot for analytical event time queries
- Lakehouse for cheap long-term history

## 10. Trade-offs

| Pros | Cons |
|---|---|
| very fast time-window queries | not ideal for arbitrary transactions |
| efficient compression | high-cardinality tags are costly |
| natural for dashboards/alerts | late data complicates rollups |
| rollups reduce cost | raw detail may be lost |

## 11. Failure Modes

- Failure: Hot time partition.
- Symptom: current writes are slow.
- Recovery: shard by tag/key inside time bucket.
- Prevention: partition plus distribution key design.

- Failure: Late data arrives after rollup.
- Symptom: aggregates are incorrect.
- Recovery: recompute affected windows.
- Prevention: watermark and correction strategy.

- Failure: Retention too short.
- Symptom: cannot investigate old incident.
- Recovery: restore/archive if available.
- Prevention: define raw and rolled-up retention intentionally.

## 12. Common Mistakes

- Mistake: Querying without time filter.
- Why it is wrong: scans too much data.
- Better approach: always bound time-series queries by time range.

- Mistake: Storing every unique request_id as a tag.
- Why it is wrong: cardinality explodes.
- Better approach: use tags for bounded dimensions; use logs for request-level search.

## 13. Mini Example

```text
Raw:
10:00 latency=100
10:01 latency=120
10:02 latency=80

Rollup:
10:00-10:05 avg_latency=100
```

## 14. Interview Questions

1. What is time-series analytics?
2. Why partition by time?
3. What is downsampling?
4. How do you handle late data?
5. What is high-cardinality tag risk?

## 15. Interview Speak

"Time-series analytics is optimized for timestamped measurements and events. I would partition by time, index bounded tags, roll up older data, define retention tiers, and handle late events with watermarks or recomputation. The major risks are hot partitions and high-cardinality dimensions."

## 16. Quick Recall

- One-line summary: Time-series analytics answers how values change over time.
- Three keywords: timestamp, rollup, retention.
- One trap: unbounded tags.
- One memory trick: Movie of measurements.

