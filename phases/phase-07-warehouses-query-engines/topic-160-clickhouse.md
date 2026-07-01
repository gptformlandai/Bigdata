# Topic 160: ClickHouse

## 1. Goal

Understand ClickHouse as a fast columnar OLAP database for analytical queries.

## 2. Baby Intuition

ClickHouse is like a very fast calculator for event tables.

It is built to scan, filter, group, and aggregate large columns quickly.

## 3. What It Is

- Simple definition: ClickHouse is a high-performance columnar database for analytics.
- Technical definition: ClickHouse is an open-source column-oriented OLAP DBMS designed for fast analytical SQL queries, high ingestion rates, compression, and distributed execution.
- Category: Real-time/near-real-time OLAP database.
- Related terms: MergeTree, columnar storage, primary key/order key, sparse index, materialized view, distributed table.

## 4. Why It Exists

Many products need fast analytical queries on fresh event/log data:

- observability dashboards
- product analytics
- security analytics
- ad metrics
- financial event exploration

Traditional warehouses may be too slow or expensive for very high-concurrency, low-latency event analytics. ClickHouse targets fast reads and aggregations.

## 5. Where It Fits In A Data Platform

```text
Apps/logs/events
  -> Kafka/batch ingestion
  -> ClickHouse tables
  -> dashboards/APIs/ad hoc analytics
```

ClickHouse is often used as a serving OLAP store, not just an offline warehouse.

## 6. How It Works Step By Step

1. Data is inserted into columnar tables.
2. Data is stored in sorted parts, commonly using MergeTree engines.
3. Columns are compressed independently.
4. Query reads only needed columns.
5. Sparse indexes and ordering help skip parts.
6. Background merges compact parts.
7. Distributed setups split data across shards/replicas.

## 7. How To Use It Practically

Common table design ideas:

| Concept | Meaning |
|---|---|
| ORDER BY | defines physical sort/order key |
| partition | coarse data grouping, often by date |
| MergeTree | core storage engine family |
| materialized view | precompute/route data on insert |
| distributed table | query across shards |

Example:

```sql
SELECT toDate(event_time) AS day, count()
FROM events
WHERE event_time >= now() - INTERVAL 7 DAY
GROUP BY day;
```

## 8. Real-World Scenario

- Product/system: Application observability.
- Problem: Engineers need dashboards over billions of logs/metrics with low latency.
- How ClickHouse helps: columnar storage, compression, sorting, and fast aggregation make dashboard queries quick.
- What would go wrong without tuning: poor order key or too many tiny inserts can hurt performance.

## 9. System Design Angle

Use ClickHouse when:

- low-latency analytical queries matter
- data is append-heavy
- aggregations over large event tables are common
- dashboard/API serving needs speed
- SQL over logs/events is important

Be careful with:

- schema/order key design
- high-cardinality columns
- update/delete expectations
- replication/sharding operations
- small insert batches

## 10. Trade-offs

| Pros | Cons |
|---|---|
| very fast OLAP queries | schema/layout design matters |
| high compression | mutable updates are not its main strength |
| high ingest support | operational expertise needed at scale |
| good for dashboards | joins need careful design |
| open source ecosystem | cluster management can be complex |

## 11. Failure Modes

- Failure: Bad ORDER BY key.
- Symptom: queries scan too much data.
- Recovery: rebuild table with better layout.
- Prevention: choose keys from common filters.

- Failure: Tiny inserts.
- Symptom: too many parts and merge pressure.
- Recovery: batch inserts and optimize.
- Prevention: buffer ingestion.

- Failure: Using it like OLTP.
- Symptom: frequent row updates/deletes are painful.
- Recovery: redesign workload.
- Prevention: use ClickHouse for analytical append-heavy use cases.

## 12. Common Mistakes

- Mistake: Thinking columnar means always fast.
- Why it is wrong: bad sort keys and query patterns can still scan too much.
- Better approach: design table layout from actual queries.

- Mistake: Using ClickHouse as a transactional database.
- Why it is wrong: it is optimized for OLAP, not row-by-row OLTP.
- Better approach: keep OLTP in operational databases.

## 13. Mini Example

```text
Dashboard query filters by tenant_id and event_time.

Good layout may order by:
(tenant_id, event_time)

This helps ClickHouse skip unrelated ranges.
```

## 14. Interview Questions

1. What is ClickHouse?
2. Why is columnar storage fast for analytics?
3. What is MergeTree?
4. What makes a good ORDER BY key?
5. When should you not use ClickHouse?

## 15. Interview Speak

"ClickHouse is a fast columnar OLAP database for event/log-style analytics and dashboard serving. It works well for append-heavy analytical workloads, but table design is critical: partitioning, ORDER BY keys, batching inserts, and materialized views strongly affect performance."

## 16. Quick Recall

- One-line summary: ClickHouse is fast columnar SQL for analytical event data.
- Three keywords: columnar, MergeTree, order key.
- One trap: Treating it like an OLTP database.
- One memory trick: Fast calculator for columns.
