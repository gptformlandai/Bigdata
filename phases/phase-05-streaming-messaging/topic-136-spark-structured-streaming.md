# Topic 136: Spark Structured Streaming

## 1. Goal

Understand Spark Structured Streaming as Spark's high-level streaming API built on DataFrames.

## 2. Baby Intuition

Batch Spark processes a fixed table.

Structured Streaming treats a stream like a table that keeps growing.

You write DataFrame-like logic once, and Spark continuously updates results as new data arrives.

## 3. What It Is

- Simple definition: Structured Streaming is Spark's DataFrame-based streaming engine.
- Technical definition: Spark Structured Streaming is a scalable stream processing engine built on Spark SQL that processes unbounded data as incremental micro-batches or continuous execution, using DataFrame/Dataset APIs.
- Category: Stream processing engine/API.
- Related terms: micro-batch, trigger, checkpoint location, watermark, output mode, streaming query.

## 4. Why It Exists

Spark users wanted streaming without learning a totally separate API.

Structured Streaming exists to:

- use DataFrame/Spark SQL concepts for streams
- process Kafka/file streams
- support windowed aggregations
- maintain checkpoints
- write streaming outputs
- unify batch and streaming logic

## 5. Where It Fits In A Data Platform

```text
Kafka / files
  -> Spark Structured Streaming
  -> console/Kafka/data lake/table/database
```

Common sources:

- Kafka
- files landing in storage
- rate source for tests

Common sinks:

- Kafka
- files
- Delta/lakehouse tables
- memory/console for debugging

## 6. How It Works Step By Step

1. Define streaming source.
2. Apply DataFrame transformations.
3. Define output sink.
4. Set checkpoint location.
5. Start streaming query.
6. Spark processes new data in triggers/micro-batches.
7. Progress is checkpointed.
8. On failure, query resumes from checkpoint.

## 7. How To Use It Practically

Kafka read example:

```python
events = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "clicks")
    .load()
)
```

Write stream:

```python
query = (
    events.writeStream
    .format("parquet")
    .option("path", "/data/clicks_out")
    .option("checkpointLocation", "/checkpoints/clicks")
    .outputMode("append")
    .start()
)
```

Important:

```text
checkpointLocation is required for reliable recovery.
```

## 8. Real-World Scenario

- Product/system: Near-real-time click dashboard.
- Problem: Need update metrics every minute from Kafka click events.
- How Structured Streaming helps: Reads Kafka and runs DataFrame aggregations continuously.
- What would go wrong without checkpointing: failure may duplicate or lose progress.

## 9. System Design Angle

Structured Streaming is good when:

- team already uses Spark
- DataFrame API is preferred
- micro-batch latency is acceptable
- integration with lakehouse tables matters
- streaming and batch logic should be similar

Flink may be better when:

- very low latency is required
- complex event-time/stateful processing dominates
- advanced streaming operations are central

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| DataFrame API for streams | micro-batch latency |
| batch/stream unification | checkpoint management |
| Spark ecosystem integration | state tuning |
| easy Kafka/lake integration | not always as low-latency as Flink |

## 11. Failure Modes

- Failure: missing checkpoint.
- Symptom: restart may reprocess from wrong place.
- Recovery: configure checkpoint and restart carefully.
- Prevention: durable checkpoint location.

- Failure: state grows too large.
- Symptom: slow batches and checkpoint pressure.
- Recovery: watermark/TTL/filter.
- Prevention: manage stateful operations.

- Failure: sink not idempotent.
- Symptom: duplicate writes after retry.
- Recovery: dedupe/transactional sink.
- Prevention: idempotent output design.

## 12. Common Mistakes

- Mistake: Treating streaming query like one-time batch job.
- Why it is wrong: it runs continuously and needs checkpoint/monitoring.
- Better approach: operate it like a service.

- Mistake: No watermark for stateful windows.
- Why it is wrong: state can grow forever.
- Better approach: event-time watermarking.

## 13. Mini Example

```text
Kafka clicks -> Structured Streaming -> 1-minute window counts -> dashboard table
```

## 14. Interview Questions

1. What is Spark Structured Streaming?
2. What is micro-batch processing?
3. Why is checkpoint location important?
4. Structured Streaming vs Flink?
5. What are output modes?

## 15. Interview Speak

"Spark Structured Streaming is Spark's DataFrame-based streaming API. It treats streams as continuously growing tables and processes them incrementally, often using micro-batches. It is strong when teams already use Spark and want batch/stream API unification, but checkpointing, state, watermarks, and sink idempotency are critical."

## 16. Quick Recall

- One-line summary: Structured Streaming is Spark DataFrames on unbounded data.
- Three keywords: micro-batch, checkpoint, watermark.
- One trap: Running stateful streams without checkpoint/watermark.
- One memory trick: A table that keeps growing.
