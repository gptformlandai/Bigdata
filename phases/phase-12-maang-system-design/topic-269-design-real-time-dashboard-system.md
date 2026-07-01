# Topic 269: Design Real-Time Dashboard System

## 1. Goal

Design a system that powers dashboards with fresh metrics from streaming and batch data sources.

## 2. Baby Intuition

A real-time dashboard is like a control room screen.

It needs fresh numbers quickly, but it also needs to avoid showing misleading broken data.

## 3. Requirements

Clarify:

- What metrics are shown?
- What freshness is required: seconds, minutes, or hours?
- How many users and dashboard queries?
- Are metrics approximate or exact?
- What happens when data is delayed?

## 4. Functional Requirements

- ingest events or metric updates
- compute near-real-time aggregates
- serve dashboard queries with low latency
- support filters and dimensions
- show freshness/status indicators
- reconcile with batch source if needed
- alert when dashboard data is stale

## 5. Non-Functional Requirements

- low query latency
- predictable freshness
- high availability
- scalable fan-out to many users
- protection from expensive queries
- correctness for important metrics
- clear degraded states

## 6. Capacity Estimation

Example:

```text
1M events/sec
dashboard freshness target = 1 minute
10K dashboard users
common query latency target = under 2 seconds
```

Dashboard systems usually need pre-aggregations because raw event scans are too slow.

## 7. Events And APIs

Input event:

```json
{
  "event_type": "order_created",
  "order_id": "o1",
  "amount": 50,
  "region": "US",
  "event_time": "2026-07-02T10:00:00Z"
}
```

Dashboard query:

```text
GET /dashboard/metrics?metric=revenue&group_by=region&window=last_1h
```

## 8. Data Model

Aggregated table:

```text
revenue_minute_metrics(window_start, region, product_category, orders, revenue)
```

Dashboard metadata:

```text
metric_name, definition, owner, freshness_slo, allowed_dimensions
```

## 9. High-Level Architecture

```text
events
  -> Kafka/Pub/Sub
  -> stream aggregation
  -> real-time OLAP store
  -> dashboard API/cache
  -> dashboard UI

events/lake
  -> batch reconciliation
  -> warehouse/gold tables
  -> corrected aggregates if needed
```

## 10. Data Flow

1. Events enter streaming ingestion.
2. Stream processor computes minute-level aggregates.
3. Aggregates are written to OLAP store.
4. Dashboard API queries OLAP store or cache.
5. UI displays metric value and freshness timestamp.
6. Batch jobs reconcile final daily numbers.
7. Corrections update historical dashboard values if needed.

## 11. Deep Dive Components

Serving store choices:

- Druid/Pinot/ClickHouse for slice-and-dice analytics
- Redis/cache for very small fixed dashboards
- warehouse for slower official reports

Freshness display:

- show last updated time
- show stale warning
- distinguish live vs finalized metrics

Query protection:

- allow only approved dimensions
- pre-aggregate common metrics
- cache common dashboard queries
- enforce query timeouts

## 12. Scaling And Partitioning

- Partition streams by aggregation key.
- Partition OLAP by time.
- Sort/cluster by common dimensions.
- Precompute minute/hour/day rollups.
- Cache popular dashboard views.
- Use separate read replicas or clusters for heavy tenants.

## 13. Consistency And Correctness

- Real-time metrics may be approximate until finalized.
- Deduplicate events by event_id.
- Handle late events with watermark and correction updates.
- Define metric ownership and business meaning.
- Use batch reconciliation for official numbers.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| stream lag | show stale badge and alert |
| OLAP store down | serve cached last-known values with warning |
| bad metric logic | rollback and recompute |
| late data | update affected windows |
| query overload | rate limit and cache |

## 15. Monitoring, Cost, And Security

Monitor:

- metric freshness
- stream lag
- OLAP ingest latency
- dashboard query latency
- cache hit rate
- failed queries

Cost:

- pre-aggregate instead of raw scans
- limit high-cardinality dimensions
- cache popular queries
- downsample old data

Security:

- enforce dashboard permissions
- apply row/column policies
- avoid exposing sensitive raw events
- audit access to business metrics

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| real-time stream aggregation | fresh dashboards | complex late data handling |
| cache | low latency | possible staleness |
| OLAP store | flexible slicing | extra system to operate |
| batch reconciliation | trustworthy final numbers | numbers can change later |

## 17. Interview-Ready Final Answer

"I would design real-time dashboards with streaming pre-aggregation and an OLAP serving layer. Events flow into Kafka, stream processors compute minute-level aggregates, and an OLAP store serves low-latency dashboard queries. The UI should display freshness and distinguish live from finalized metrics. Batch jobs reconcile official results and correct late data. I would protect the system with dedupe, watermarks, caching, query limits, freshness alerts, and fallback to cached last-known values when serving is degraded."

## 18. Quick Recall

- One-line summary: Real-time dashboards need fresh pre-aggregated metrics and clear freshness status.
- Core tools: Kafka, stream aggregation, OLAP store, cache, batch reconciliation.
- Main trap: showing stale/approximate data as final truth.
- Memory trick: control room screen with a freshness clock.

