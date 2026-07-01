# Topic 278: System Design Interview Framework

## 1. Goal

Use a repeatable framework for Big Data system design interviews.

## 2. Baby Intuition

System design interviews are not about drawing the fanciest diagram.

They are about showing how you think from requirements to trade-offs.

## 3. The 45-Minute Flow

Use this time plan:

```text
0-5 min: clarify requirements
5-10 min: estimate scale and define events
10-20 min: high-level architecture
20-32 min: deep dive critical components
32-40 min: failure, scaling, correctness, monitoring
40-45 min: trade-offs and final summary
```

## 4. Clarifying Questions

Ask:

- Who are the users?
- What are the main use cases?
- What freshness is required?
- What scale should we assume?
- Is correctness or latency more important?
- Do we need historical replay?
- What data is sensitive?

Do not ask 20 questions. Ask enough to frame the design.

## 5. Requirements Template

Functional:

- ingest data
- process/transform data
- store raw and curated data
- serve dashboards/APIs/ML
- monitor and recover

Non-functional:

- throughput
- latency
- availability
- correctness
- scalability
- cost
- security

## 6. Capacity Estimation Template

Say:

```text
Let me estimate order of magnitude.
users/events per day * event size = raw storage per day.
Then I will account for peak traffic, replication, compression, and derived tables.
```

Example:

```text
100M users * 50 events/day = 5B events/day
1 KB/event = about 5 TB/day raw before compression
```

## 7. Architecture Template

Reusable Big Data architecture:

```text
sources
  -> ingestion gateway/connectors
  -> durable log or landing zone
  -> raw lake
  -> stream processing for hot path
  -> batch processing for accurate path
  -> serving stores
  -> dashboards/ML/APIs
```

Surround it with:

- schema registry
- catalog
- security
- observability
- orchestration

## 8. Deep Dive Menu

Pick the most important components:

- event schema
- partitioning
- dedupe
- late events
- stream processing
- table format
- OLAP serving
- feature store
- data quality
- backfill/replay
- access control

Do not deep dive everything equally. Choose what matters for the problem.

## 9. Correctness Checklist

Mention:

- event_id for dedupe
- event_time vs processing_time
- watermarks
- idempotent writes
- source of truth
- replay from raw
- reconciliation
- schema evolution

## 10. Failure Checklist

Cover:

- producer retry
- broker outage/lag
- stream job failure
- batch job failure
- bad data/schema
- serving store outage
- backfill and recovery

## 11. Monitoring Checklist

Monitor:

- ingestion rate
- lag
- freshness
- quality checks
- duplicate rate
- late events
- job duration
- query latency
- cost

## 12. Final Summary Template

Use this:

```text
I would design this as <architecture style>.
The source data enters through <ingestion>.
Raw data is stored in <raw layer> for replay.
<stream path> handles freshness.
<batch path> handles correctness.
<serving stores> support users.
The main trade-offs are <trade-offs>.
The key failure handling is <failure handling>.
```

## 13. Common Mistakes

- jumping directly into Kafka/Spark without requirements
- forgetting capacity estimate
- no data model
- no failure handling
- no security/cost
- no explanation of trade-offs
- diagram too complex to explain

## 14. Interview Speak

"I will first clarify the product goal and freshness/correctness requirements. Then I will estimate scale, define events and data model, propose a high-level architecture, and deep dive the most important bottlenecks: ingestion, processing, storage, serving, failure handling, and trade-offs."

## 15. Quick Recall

- One-line summary: Requirements first, tools second, trade-offs always.
- Three keywords: requirements, scale, trade-offs.
- One trap: drawing before clarifying.
- Memory trick: question, scale, flow, failure.

