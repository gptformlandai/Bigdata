# Phase 11 Review: Advanced Architecture Patterns

## 1. Phase Summary

Phase 11 connects earlier tools into real production architecture patterns.

The core idea:

```text
source systems create events and data
  -> architecture patterns move and organize them
  -> serving systems power analytics, ML, search, fraud, metrics, and logs
  -> reliability practices keep everything trusted
```

If you remember only one sentence:

```text
Advanced data architecture is about choosing the right flow, consistency model, serving layer, and failure strategy for the product need.
```

## 2. Big Architecture Shapes

| Pattern | Main Idea | Best For |
|---|---|---|
| Lambda | batch layer + speed layer + serving layer | exact batch plus low-latency views |
| Kappa | streaming-first, replay from log | event-driven systems with replayable streams |
| Medallion | bronze -> silver -> gold | lakehouse data organization |
| Bronze/Silver/Gold | raw -> cleaned -> business-ready | clear data quality progression |

Quick distinction:

```text
Lambda keeps separate batch and stream paths.
Kappa tries to simplify by using one streaming path.
Medallion organizes data quality layers.
```

## 3. Database Change And Event Patterns

| Pattern | Problem Solved | Watch Out |
|---|---|---|
| CDC | move database changes downstream | deletes, ordering, schema changes |
| Debezium | CDC from database logs into Kafka | connector lag and snapshots |
| Outbox | avoid database/event dual-write bug | duplicate publishes |
| Saga | coordinate distributed transactions | compensation complexity |
| Event sourcing | store changes as events | replay/versioning complexity |
| CQRS | separate write model and read model | eventual consistency |

Strong memory:

```text
CDC moves database changes.
Outbox reliably publishes service events.
Saga coordinates multi-step business workflows.
```

## 4. ML And Product Pipelines

| Pipeline | Needs |
|---|---|
| feature store | offline history, online serving, point-in-time correctness |
| real-time feature pipeline | freshness, low latency, state, replay |
| search analytics | indexing, ranking signals, query/click events |
| recommendation pipeline | user/item/events, candidates, ranking, feedback |
| fraud detection | velocity features, risk scoring, fallback, audit trail |

Interview line:

```text
For ML pipelines, I would separate feature generation, feature serving, model scoring, monitoring, and feedback labels.
```

## 5. Observability And Time Data

| Platform | Main Use | Key Risk |
|---|---|---|
| metrics platform | numeric health over time | high-cardinality labels |
| logging platform | searchable event detail | cost and sensitive data leakage |
| time-series analytics | timestamped trend analysis | hot partitions and late data |

Quick distinction:

```text
Metrics tell what changed.
Logs explain why.
Time-series analytics studies timestamped behavior over time.
```

## 6. Platform-Scale Concerns

Multi-tenant platform concerns:

- tenant data isolation
- tenant-aware access control
- quotas and rate limits
- noisy neighbor protection
- per-tenant cost attribution
- onboarding/offboarding
- deletion and retention

Reliability concerns:

- freshness
- completeness
- correctness
- latency
- availability
- idempotency
- replay/backfill
- monitoring and alerting
- incident response

Strong line:

```text
Monitor both pipeline health and data health.
```

## 7. Common Interview Traps

| Trap | Better Thinking |
|---|---|
| saying Lambda is always best | mention complexity and Kappa alternative |
| ignoring deletes in CDC | design tombstone/delete handling |
| assuming Outbox prevents duplicates | consumers still need idempotency |
| building feature store without point-in-time correctness | protect against training leakage |
| using user_id as a metric label | avoid cardinality explosion |
| securing tenants only in dashboards | enforce at storage/query layer |
| monitoring only job success | also monitor data quality and freshness |

## 8. Design Checklist

For any Phase 11 architecture question, ask:

- Is this batch, streaming, or hybrid?
- What is the source of truth?
- Do updates/deletes matter?
- What is the serving latency requirement?
- What consistency does the user need?
- Can the system replay data?
- How are duplicates handled?
- How are schema changes handled?
- What are the SLOs?
- What does the user observe during failure?

## 9. Fast Recall

```text
Lambda = batch + stream.
Kappa = stream + replay.
Medallion = raw + cleaned + business-ready.
CDC = database changes.
Outbox = reliable event publish.
Saga = distributed workflow compensation.
Feature store = consistent ML features.
Metrics = numbers.
Logs = detailed events.
Reliability = fresh, complete, valid, available data.
```

## 10. Mini Capstone Prompt

> Design a real-time fraud detection platform for card transactions.

Strong answer should mention:

- Kafka transaction events
- CDC for customer/account context
- streaming velocity features
- offline and online feature stores
- fraud scoring service
- rules fallback
- audit log of decisions
- metrics and logs
- replay/backfill
- freshness and latency SLOs
- false-positive monitoring

