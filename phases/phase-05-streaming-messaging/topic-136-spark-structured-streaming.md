# Topic 136: Spark Structured Streaming

## 1. Goal

Understand Spark Structured Streaming as Spark's high-level streaming API using DataFrame/SQL concepts.

## 2. Baby Intuition

Structured Streaming lets you write streaming logic like a table query.

Spark keeps updating the result as new data arrives.

Think:

```text
same DataFrame style, but input table keeps growing
```

## 3. What It Is

- Simple definition: Spark Structured Streaming processes streaming data with DataFrames.
- Technical definition: Spark Structured Streaming is a scalable stream processing engine built on Spark SQL/DataFrames that treats streams as unbounded tables and executes queries incrementally, often in micro-batches.
- Category: Stream processing API.
- Related terms: micro-batch, trigger, checkpoint, watermark, output mode, sink.

## 4. Why It Exists

Teams already using Spark wanted streaming with:

- DataFrame API
- Spark SQL
- integration with batch code
- Kafka sources
- file/lakehouse sinks
- easier streaming model

Structured Streaming gives one API style for batch and streaming.

## 5. Where It Fits In A Data Platform

```text
Kafka/files -> Spark Structured Streaming -> Delta/Iceberg/Kafka/DB/dashboard
```

Common use:

- near-real-time ETL
- streaming ingestion to lakehouse
- incremental aggregations
- Kafka-to-table pipelines

## 6. How It Works Step By Step

1. Define streaming source.
2. Apply DataFrame transformations.
3. Define sink and output mode.
4. Start query.
5. Spark processes new data incrementally.
6. Checkpoint tracks progress/state.
7. Query keeps running.

Example idea:

```python
events = spark.readStream.format("kafka").load()
```

## 7. How To Use It Practically

Kafka read shape:

```python
raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "orders")
    .load()
)
```

Write shape:

```python
query = (
    result.writeStream
    .format("parquet")
    .option("path", "/data/output")
    .option("checkpointLocation", "/checkpoints/orders")
    .outputMode("append")
    .start()
)
```

Checkpoint is mandatory for reliable production streaming.

## 8. Real-World Scenario

- Product/system: Streaming lakehouse ingestion.
- Problem: Continuously load Kafka order events into curated tables.
- How Structured Streaming helps: Uses Spark DataFrame logic and checkpoints to write incremental outputs.
- What would go wrong without checkpoints: failures may duplicate or skip data.

## 9. System Design Angle

Choose Structured Streaming when:

- team already uses Spark
- near-real-time is enough
- data lands in lakehouse
- DataFrame/SQL API is desired

Flink may be better when:

- very low latency
- complex event-time processing
- advanced stateful streaming

## 10. Failure Modes

- Failure: checkpoint deleted.
- Symptom: query may restart incorrectly or duplicate.
- Recovery: rebuild carefully.
- Prevention: durable checkpoint path.

- Failure: sink slow.
- Symptom: micro-batches take longer and lag grows.
- Recovery: optimize sink/batch size/resources.
- Prevention: monitor batch duration.

- Failure: state grows.
- Symptom: memory/checkpoint growth.
- Recovery: watermark/TTL/window cleanup.
- Prevention: design state lifecycle.

## 11. Common Mistakes

- Mistake: Treating streaming query like one-time batch.
- Why it is wrong: it runs continuously.
- Better approach: monitor it as a service.

- Mistake: No checkpoint location.
- Why it is wrong: recovery is unsafe.
- Better approach: always configure durable checkpointing.

## 12. Interview Speak

"Spark Structured Streaming treats a stream as an unbounded table and lets us use DataFrame/Spark SQL operations incrementally. It is strong for near-real-time ETL into lakes/lakehouses, especially for Spark teams. Checkpointing, watermarks, output mode, and sink behavior are critical for correctness."

## 13. Quick Recall

- One-line summary: Structured Streaming is Spark DataFrames for unbounded data.
- Three keywords: micro-batch, checkpoint, output mode.
- One trap: Missing checkpoint.
- One memory trick: A table that keeps receiving rows.
