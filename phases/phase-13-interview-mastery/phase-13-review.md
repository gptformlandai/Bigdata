# Phase 13 Review: Interview Mastery

## 1. Phase Summary

Phase 13 converts Big Data knowledge into interview execution.

The core idea:

```text
projects prove ability
questions test fundamentals
debugging tests judgment
system design tests architecture thinking
behavioral stories test ownership
```

If you remember only one sentence:

```text
A strong interview answer is clear, structured, honest, and trade-off aware.
```

## 2. Resume Project Checklist

A strong Big Data project should include:

- realistic source data
- ingestion layer
- processing layer
- storage model
- serving output
- data quality checks
- orchestration or run process
- failure/replay plan
- cost/performance note
- README and architecture diagram

Strong project types:

- clickstream analytics
- CDC to lakehouse
- real-time fraud features
- data observability platform
- recommendation feature store

## 3. Question Answer Formula

Use:

```text
definition
why it exists
how it works
where it is used
trade-off
failure mode
example
```

This works for Spark, Kafka, Airflow, lakehouse, SQL, modeling, and governance questions.

## 4. Tool Revision

| Tool | Must Explain |
|---|---|
| Spark | DAG, stages/tasks, shuffle, joins, skew, caching, AQE |
| Kafka | topics, partitions, offsets, consumer groups, ordering, lag |
| Airflow | DAGs, scheduler, executor, retries, backfills, sensors |
| SQL | joins, windows, aggregation, dedupe, performance |
| Lakehouse | ACID tables, snapshots, compaction, upserts, schema evolution |
| Warehouse | star schema, facts/dimensions, SCD, query optimization |

## 5. System Design Flow

```text
clarify
  -> requirements
  -> scale
  -> events/data model
  -> architecture
  -> data flow
  -> scaling/partitioning
  -> correctness
  -> failure handling
  -> monitoring/cost/security
  -> trade-offs
```

Never start with tools before requirements.

## 6. Debugging Flow

```text
impact
  -> stop bad output if needed
  -> trace source to sink
  -> compare expected vs actual
  -> isolate root cause
  -> recover
  -> prevent recurrence
```

Use this for:

- late pipeline
- wrong dashboard
- duplicate records
- Kafka lag
- Spark failure
- Airflow failure
- cost spike

## 7. Performance Flow

```text
measure baseline
  -> find bottleneck
  -> change one thing
  -> measure again
```

Common bottlenecks:

- shuffle
- skew
- scan size
- partition count
- small files
- downstream sink
- bad join
- missing partition filter

## 8. Cost Flow

```text
find top cost driver
  -> separate required spend from waste
  -> optimize biggest waste
  -> add guardrails
```

Guardrails:

- budgets
- alerts
- tags
- quotas
- retention policies
- query limits
- chargeback/showback

## 9. Behavioral Story Bank

Prepare stories for:

- production incident
- performance win
- data quality issue
- ambiguous requirement
- conflict/disagreement
- learning new tool
- mistake and recovery
- cost reduction
- ownership beyond your role

Use STAR:

```text
Situation, Task, Action, Result
```

## 10. Trade-Off Language

Use:

```text
Option A gives <benefit>, but costs <cost>.
Option B gives <benefit>, but costs <cost>.
Given <requirement>, I choose <option>.
```

Common trade-offs:

- batch vs streaming
- cost vs performance
- latency vs correctness
- simplicity vs flexibility
- normalized vs denormalized
- exact vs approximate
- hot storage vs cold storage

## 11. Unknown Answer Recovery

Use:

```text
I have not used that deeply, but I understand the problem it solves.
I would reason from similar systems and validate the exact behavior with docs, tests, and metrics.
```

Do not fake expertise.

## 12. Final Before-Interview Checklist

- I can explain two resume projects end to end.
- I can answer Spark/Kafka/Airflow fundamentals.
- I can solve SQL joins/windows/dedupe questions.
- I can design one event pipeline and one batch warehouse.
- I can debug a failed pipeline out loud.
- I can discuss performance, cost, security, and reliability.
- I have 5 behavioral stories ready.
- I can gracefully handle unknown questions.

## 13. Final Memory Lines

```text
Requirements first.
Scale second.
Architecture third.
Failure always.
Trade-offs clearly.
Honesty beats pretending.
```

