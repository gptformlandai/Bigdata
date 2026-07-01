# Topic 161: Druid

## 1. Goal

Understand Apache Druid as a real-time OLAP database for fast slice-and-dice analytics.

## 2. Baby Intuition

Druid is like a live analytics cube for event data.

It is built so users can filter, group, and aggregate fresh events quickly.

## 3. What It Is

- Simple definition: Druid is a real-time analytical database for event data.
- Technical definition: Apache Druid is a distributed columnar OLAP datastore optimized for low-latency ingestion, time-based partitioning, filtering, aggregation, and interactive analytics.
- Category: Real-time OLAP datastore.
- Related terms: segment, datasource, historical node, middle manager/indexer, broker, coordinator, rollup.

## 4. Why It Exists

Some analytics need fresh data and very fast dashboards:

- ad impressions/clicks
- operational metrics
- user behavior dashboards
- network/security events
- product analytics

Classic batch warehouses may be enough for hourly/daily reports, but not always for interactive live metrics.

## 5. Where It Fits In A Data Platform

```text
Kafka/events/files
  -> Druid ingestion
  -> Druid segments
  -> dashboard/API queries
```

Druid often serves end-user dashboards where queries are filter-heavy and time-based.

## 6. How It Works Step By Step

1. Events arrive from Kafka or batch files.
2. Druid ingests and indexes them into time-partitioned segments.
3. Segments store columns and indexes for fast filtering.
4. Broker nodes receive queries.
5. Brokers route work to historical/realtime nodes.
6. Nodes scan relevant segments and aggregate results.
7. Broker merges partial results and returns the answer.

## 7. How To Use It Practically

Important concepts:

| Concept | Meaning |
|---|---|
| datasource | logical table/event stream |
| segment | immutable chunk of indexed data |
| dimension | filter/group-by attribute |
| metric | numeric value to aggregate |
| rollup | pre-aggregate rows during ingestion |

Good fit queries:

```text
events over time
filter by campaign/country/device
group by minute/hour/day
compute counts, sums, percentiles
```

## 8. Real-World Scenario

- Product/system: Ad analytics dashboard.
- Problem: Advertisers need impressions, clicks, and spend within seconds/minutes.
- How Druid helps: realtime ingestion plus indexed time segments support fast dashboard queries.
- What would go wrong without it: warehouse queries may be too slow or stale for live campaign decisions.

## 9. System Design Angle

Use Druid when:

- queries are time-series/event analytics
- freshness matters
- dashboard latency matters
- filters and aggregations dominate
- ingestion from Kafka is important

Be careful with:

- high-cardinality dimensions
- ingestion tuning
- segment sizing
- rollup correctness
- complex joins

## 10. Trade-offs

| Pros | Cons |
|---|---|
| fast time-based analytics | not a general relational warehouse |
| realtime ingestion | operational complexity |
| indexed filtering | schema/ingestion design matters |
| good dashboard latency | joins are limited compared with warehouses |
| rollup support | rollup can lose raw detail if misused |

## 11. Failure Modes

- Failure: Bad segment sizing.
- Symptom: too many segments or slow queries.
- Recovery: compact/reindex.
- Prevention: tune ingestion granularity and segment size.

- Failure: High-cardinality dimension explosion.
- Symptom: memory/index overhead.
- Recovery: reduce indexed dimensions or redesign.
- Prevention: choose dimensions carefully.

- Failure: Kafka ingestion lag.
- Symptom: dashboard freshness drops.
- Recovery: scale ingestion tasks.
- Prevention: monitor lag and task health.

## 12. Common Mistakes

- Mistake: Using Druid as a full warehouse replacement.
- Why it is wrong: it is specialized for OLAP event/time analytics.
- Better approach: use it as serving OLAP plus warehouse/lake for broad analytics.

- Mistake: Rolling up data without understanding future questions.
- Why it is wrong: lost detail may not be recoverable in Druid.
- Better approach: keep raw data in lake and roll up only safe metrics.

## 13. Mini Example

```text
Query:
For each campaign, show clicks per minute for the last 1 hour.

Druid:
scan recent time segments
filter campaign events
aggregate clicks by minute
```

## 14. Interview Questions

1. What is Druid?
2. What kind of workloads fit Druid?
3. What is a Druid segment?
4. How does Druid support realtime analytics?
5. When would you avoid Druid?

## 15. Interview Speak

"Druid is a distributed real-time OLAP datastore for event and time-series analytics. It ingests streams or batch data into indexed segments and serves fast filter/group-by aggregations for dashboards. I would use it for low-latency analytics, not as a general-purpose warehouse."

## 16. Quick Recall

- One-line summary: Druid serves fast live event analytics from indexed segments.
- Three keywords: segments, realtime, dashboards.
- One trap: Treating Druid as a relational warehouse.
- One memory trick: Live analytics cube for events.
