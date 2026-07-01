# Topic 162: Pinot

## 1. Goal

Understand Apache Pinot as a real-time distributed OLAP store for user-facing analytics.

## 2. Baby Intuition

Pinot is like a fast analytics backend behind a product dashboard.

It is built for many users asking fresh analytical questions quickly.

## 3. What It Is

- Simple definition: Pinot is a real-time OLAP database for fast analytics over events.
- Technical definition: Apache Pinot is a distributed columnar OLAP datastore designed for low-latency analytical queries, realtime ingestion, offline ingestion, indexing, and high-concurrency user-facing analytics.
- Category: Real-time OLAP serving store.
- Related terms: segment, table, controller, broker, server, realtime table, offline table, index.

## 4. Why It Exists

User-facing analytics needs:

- low query latency
- high concurrency
- fresh data
- filtering and aggregation
- scalable ingestion

Examples:

- user dashboard in SaaS app
- live delivery metrics
- ad analytics
- marketplace seller dashboards
- anomaly monitoring

## 5. Where It Fits In A Data Platform

```text
Kafka / batch files
  -> Pinot realtime/offline tables
  -> product dashboards / APIs / analysts
```

Pinot is often used as a serving layer for analytical APIs.

## 6. How It Works Step By Step

1. Data is ingested from streams or batch.
2. Pinot creates columnar segments.
3. Segments may include indexes for fast filtering.
4. Broker receives SQL query.
5. Broker routes query to servers holding relevant segments.
6. Servers scan/filter/aggregate locally.
7. Broker merges responses and returns result.

## 7. How To Use It Practically

Important concepts:

| Concept | Meaning |
|---|---|
| realtime table | consumes streaming data |
| offline table | loads batch data |
| hybrid table | combines realtime and offline |
| broker | query routing node |
| server | stores and scans segments |
| controller | cluster/table management |

Good fit:

```text
low-latency group-by/count/sum over recent and historical events
```

## 8. Real-World Scenario

- Product/system: Seller analytics dashboard.
- Problem: Thousands of sellers need near-real-time sales and traffic metrics.
- How Pinot helps: realtime ingestion and low-latency query serving support product-facing dashboards.
- What would go wrong without it: warehouse queries may be too slow or expensive for high-concurrency product traffic.

## 9. System Design Angle

Use Pinot when:

- analytics are embedded in a product
- many users query at the same time
- low latency matters
- Kafka ingestion is important
- filters/aggregations dominate

Be careful with:

- table/index design
- segment size
- retention
- high cardinality
- joins and complex SQL expectations

## 10. Trade-offs

| Pros | Cons |
|---|---|
| low-latency analytical serving | specialized workload fit |
| realtime ingestion | cluster/index tuning |
| high concurrency | not ideal for complex warehouse modeling |
| good for product analytics | schema/index design is important |
| hybrid realtime/offline patterns | operational ownership needed |

## 11. Failure Modes

- Failure: Broker/server overload.
- Symptom: dashboard/API latency spikes.
- Recovery: scale cluster or optimize queries/indexes.
- Prevention: capacity planning and query limits.

- Failure: Realtime ingestion stuck.
- Symptom: data freshness lag.
- Recovery: restart/scale consumers and inspect stream.
- Prevention: freshness alerts.

- Failure: Wrong index strategy.
- Symptom: queries scan too much data.
- Recovery: add/change indexes and rebuild segments.
- Prevention: design from query patterns.

## 12. Common Mistakes

- Mistake: Using Pinot for every ad hoc analytical workload.
- Why it is wrong: broad exploratory SQL may fit a warehouse/lake engine better.
- Better approach: use Pinot for serving known, latency-sensitive patterns.

- Mistake: Ignoring high-cardinality columns.
- Why it is wrong: indexes and memory can become expensive.
- Better approach: evaluate cardinality and access patterns.

## 13. Mini Example

```text
Product API:
GET /seller/123/metrics?window=7d

Pinot query:
filter seller_id=123
group by day
aggregate orders and revenue
```

## 14. Interview Questions

1. What is Pinot?
2. Pinot vs warehouse?
3. What is a realtime table?
4. Why does Pinot fit user-facing analytics?
5. What indexes/tuning concerns matter?

## 15. Interview Speak

"Pinot is a distributed columnar OLAP serving store for low-latency, high-concurrency analytics. I would use it behind product dashboards or analytical APIs where queries are known, filter-heavy, and freshness matters."

## 16. Quick Recall

- One-line summary: Pinot powers fast user-facing analytics APIs.
- Three keywords: realtime, segments, high concurrency.
- One trap: Expecting full warehouse flexibility.
- One memory trick: Pinot is analytics serving for products.
