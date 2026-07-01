# Topic 272: Common Big Data Interview Questions

## 1. Goal

Prepare answers for common Big Data interview questions across concepts, tools, operations, and system design.

## 2. Baby Intuition

Interview questions test two things:

```text
Do you understand the concept?
Can you explain when and why to use it?
```

Do not answer like a textbook only. Add real-world use, trade-offs, and failure modes.

## 3. Answer Formula

Use this structure:

```text
1. Simple definition
2. Why it exists
3. How it works
4. Where used
5. Trade-off or failure mode
6. Short example
```

## 4. Core Concept Questions

| Question | Strong Answer Shape |
|---|---|
| What is Big Data? | data too large/fast/varied for single-machine traditional processing |
| Batch vs streaming? | batch processes bounded data, streaming processes continuous events |
| ETL vs ELT? | ETL transforms before loading, ELT loads first then transforms |
| Data lake vs warehouse? | lake stores raw/varied data cheaply, warehouse stores structured analytics data |
| Lakehouse? | lake storage plus warehouse-like table management and ACID |
| OLTP vs OLAP? | OLTP serves transactions, OLAP serves analytics |

## 5. Distributed Systems Questions

| Question | Key Points |
|---|---|
| Why partition data? | scale storage/compute, parallelism, but introduces skew and routing |
| What is replication? | copies data for availability/read scale, with consistency trade-offs |
| What is idempotency? | safe retry without duplicate effect |
| What is backpressure? | slow downstream signals upstream to reduce rate |
| At-least-once vs exactly-once? | delivery/processing guarantees and duplicate handling |

Strong line:

```text
In data systems, retries are normal, so idempotency is a design requirement.
```

## 6. Storage And Format Questions

| Question | Key Points |
|---|---|
| Why Parquet? | columnar, compressed, predicate pushdown, analytics-friendly |
| Avro vs Parquet? | Avro row/event serialization, Parquet columnar analytics |
| Partitioning vs bucketing? | partition creates directories by value, bucketing hashes into fixed files |
| Small files problem? | too many files hurt metadata and query planning |
| Schema evolution? | safely changing schema over time |

## 7. Pipeline Questions

| Question | Strong Answer Shape |
|---|---|
| How do you design a data pipeline? | source, ingestion, validation, processing, storage, serving, monitoring |
| How do you handle bad records? | validation, quarantine/DLQ, alerting, replay |
| How do you handle late events? | event time, watermarks, allowed lateness, correction jobs |
| How do you ensure data quality? | schema, freshness, completeness, uniqueness, business checks |
| How do you backfill data? | replay raw data with idempotent writes and versioned logic |

## 8. Tool Questions

| Tool | What To Emphasize |
|---|---|
| Spark | distributed batch processing, lazy DAG, shuffle, joins, memory |
| Kafka | durable event log, partitions, consumer groups, offsets |
| Airflow | orchestration, DAGs, scheduling, retries, backfills |
| dbt | SQL transformations, lineage, tests, documentation |
| Iceberg/Delta/Hudi | ACID tables on lake, time travel, upserts |
| Snowflake/BigQuery/Redshift | warehouse/query execution and cost/performance |

## 9. Operations Questions

Common prompts:

- Pipeline is late. What do you check?
- Row count suddenly drops. What do you do?
- Kafka consumer lag is growing. Why?
- Spark job is slow. How do you debug?
- Dashboard numbers are wrong. How do you investigate?

Answer pattern:

```text
scope impact
check freshness and logs
compare source vs target
inspect recent changes
isolate failing stage
recover with replay/backfill
add prevention
```

## 10. Common Mistakes

- Giving only definitions.
- Naming tools without explaining why.
- Ignoring failure modes.
- Ignoring cost.
- Saying "exactly once" without explaining dedupe/idempotency.
- Not asking clarifying questions in system design.

## 11. Practice Plan

Daily 30-minute practice:

1. Pick 5 questions.
2. Speak each answer in 90 seconds.
3. Add one trade-off.
4. Add one failure mode.
5. Record weak topics for revision.

## 12. Quick Recall

- One-line summary: Big Data interview answers need definition, use case, trade-off, and failure handling.
- Three keywords: why, how, trade-off.
- One trap: tool-name dumping.
- Memory trick: explain like engineer, not glossary.

