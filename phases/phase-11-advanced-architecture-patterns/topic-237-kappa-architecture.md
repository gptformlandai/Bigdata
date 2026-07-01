# Topic 237: Kappa Architecture

## 1. Goal

Understand Kappa architecture as a stream-first alternative to Lambda architecture.

## 2. Baby Intuition

Kappa architecture says:

```text
Use one streaming pipeline for live data and replay history through it when needed.
```

Instead of two teams, one well-tested team handles both current and replayed events.

## 3. What It Is

- Simple definition: Kappa architecture uses one streaming pipeline for real-time and historical reprocessing.
- Technical definition: Kappa architecture stores immutable events in a durable log and processes them through a single stream processing code path for both live processing and replay/backfill.
- Category: Stream-first architecture pattern.
- Related terms: event log, replay, Kafka, Flink, stream processor, backfill, immutable events.

## 4. Why It Exists

Lambda architecture can be hard because it has two code paths:

- batch logic
- streaming logic

Kappa architecture tries to simplify by using one stream processing path.

If the logic changes, replay the event log through the new version.

## 5. Where It Fits In A Data Platform

```text
events
  -> durable event log
  -> stream processor
  -> serving tables/views

historical rebuild:
same log -> same stream processor -> rebuilt outputs
```

## 6. How It Works Step By Step

1. Events are written to a durable append-only log.
2. Stream processor consumes live events.
3. Processor updates output tables/views/features.
4. Raw log is retained long enough for replay.
5. When logic changes, create a new consumer/job.
6. Replay old events through the same processing code.
7. Swap or publish rebuilt output.

## 7. How To Use It Practically

Good fit:

- event-first systems
- Kafka/Pub/Sub/Event Hubs source of truth
- stream processing logic is manageable
- replay is possible and affordable
- one code path is valuable

Common tools:

- Kafka/Kinesis/Pub/Sub/Event Hubs
- Flink
- Kafka Streams
- Spark Structured Streaming
- lakehouse sink
- OLAP serving store

## 8. Real-World Scenario

- Product/system: Real-time fraud feature computation.
- Problem: Features must update quickly and occasionally need recomputation after logic changes.
- How Kappa helps: all transaction events are retained; feature pipeline can replay from the log.
- What would go wrong without replay: bugs in feature logic require painful manual rebuilds.

## 9. System Design Angle

Use Kappa when:

- event log can retain enough history
- streaming engine handles required correctness
- single code path is preferred
- replay time/cost is acceptable

Avoid when:

- huge history is cheaper/easier to recompute in batch
- data comes mainly as files not events
- stream processor cannot handle complex historical joins

## 10. Trade-offs

| Pros | Cons |
|---|---|
| one processing code path | replay can be expensive |
| simpler than Lambda | requires durable event log |
| good for event-first systems | historical batch joins can be hard |
| consistent live/replay logic | retention limits matter |

## 11. Failure Modes

- Failure: Event log retention too short.
- Symptom: cannot replay old history.
- Recovery: rebuild from data lake if available.
- Prevention: retention based on replay SLA.

- Failure: Non-idempotent sink.
- Symptom: replay creates duplicates.
- Recovery: clean/rebuild output.
- Prevention: idempotent writes/upserts.

- Failure: Stream logic cannot handle schema evolution.
- Symptom: replay fails on old events.
- Recovery: add compatibility handling.
- Prevention: schema registry and versioning.

## 12. Common Mistakes

- Mistake: Saying Kappa means no batch jobs anywhere.
- Why it is wrong: many platforms still use batch for reporting, compaction, or audits.
- Better approach: Kappa means the core event processing path is stream/replay based.

- Mistake: Forgetting replay cost.
- Why it is wrong: replaying months of events may be expensive.
- Better approach: estimate replay throughput and retention.

## 13. Mini Example

```text
Kafka transactions topic
  -> Flink fraud feature job
  -> online feature store

New feature logic:
  replay Kafka topic into new feature table
```

## 14. Interview Questions

1. What is Kappa architecture?
2. How is it different from Lambda architecture?
3. Why is a durable log important?
4. What makes replay hard?
5. When would Kappa not fit?

## 15. Interview Speak

"Kappa architecture uses a durable event log and one stream processing code path for both live processing and replay. It reduces Lambda's duplicate batch/stream logic but depends on retention, replay cost, idempotent sinks, and schema evolution handling."

## 16. Quick Recall

- One-line summary: Kappa is one stream pipeline plus replay.
- Three keywords: log, stream, replay.
- One trap: Retention too short for rebuilds.
- One memory trick: One road for live traffic and replay traffic.
