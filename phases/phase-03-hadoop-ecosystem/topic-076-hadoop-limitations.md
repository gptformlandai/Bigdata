# Topic 076: Hadoop Limitations

## 1. Goal

Understand Hadoop's weaknesses so you know when not to use classic Hadoop and why newer systems became popular.

## 2. Baby Intuition

Hadoop was a powerful truck for moving huge loads.

But not every problem needs a truck.

If you need fast city delivery, interactive exploration, or constant small updates, Hadoop can feel heavy and slow.

## 3. What It Is

- Simple definition: Hadoop limitations are the areas where classic Hadoop struggles.
- Technical definition: Traditional Hadoop clusters are optimized for large batch processing over distributed files, but have limitations around latency, small files, operational complexity, iterative processing, real-time workloads, and random updates.
- Category: Architecture trade-off.
- Related terms: batch latency, small files, NameNode bottleneck, MapReduce overhead, operational burden.

## 4. Why This Topic Exists

Architect-level thinking means not just knowing tools, but knowing when they are the wrong tool.

Hadoop solved huge batch storage and processing problems, but later workloads needed:

- faster queries
- easier operations
- real-time streaming
- iterative machine learning
- cloud-native storage
- ACID table updates
- simpler developer experience

## 5. Where It Fits In A Data Platform

Classic Hadoop is strongest here:

```text
Large batch files -> HDFS -> batch processing -> batch outputs
```

It struggles more here:

```text
real-time APIs
interactive dashboards
frequent row updates
small-file-heavy pipelines
low-latency ML features
```

## 6. Main Limitations

### 1. High Latency

MapReduce jobs have startup overhead and write intermediate data to disk.

Bad fit:

```text
user-facing query needs response in 100 ms
```

### 2. Small Files Problem

HDFS metadata lives in NameNode memory.

Millions of tiny files create metadata pressure and inefficient processing.

### 3. Operational Complexity

Running Hadoop clusters requires managing:

- HDFS
- YARN
- NameNode HA
- DataNode health
- queues
- security
- upgrades
- capacity

### 4. Poor Random Updates

HDFS is not designed for frequent in-place row updates.

### 5. Iterative Workloads Are Slow

MapReduce writes to disk between stages.

ML and graph workloads often need repeated passes over data.

### 6. Real-Time Streaming Is Not Native

Classic Hadoop is batch-first.

Streaming needs other systems like Kafka, Flink, Spark Streaming, or cloud stream processors.

## 7. How To Handle These Limitations

| Limitation | Better Approach |
|---|---|
| slow iterative jobs | Spark |
| real-time events | Kafka/Flink/Spark Structured Streaming |
| small files | compaction, larger files, table formats |
| interactive SQL | Presto/Trino, Impala, warehouses |
| random row access | HBase/Cassandra/DynamoDB |
| cloud storage | S3/GCS/ADLS + lakehouse |
| ACID tables | Iceberg/Delta/Hudi |

## 8. Real-World Scenario

- Product/system: Real-time fraud detection.
- Problem: Need to score transactions within milliseconds/seconds.
- Why Hadoop struggles: Batch jobs are too slow and HDFS is not serving-oriented.
- Better choice: Kafka for ingestion, stream processor for scoring, fast key-value store for features.

## 9. System Design Angle

In interviews, do not say:

```text
Use Hadoop for everything Big Data.
```

Say:

```text
If this is large batch analytics, Hadoop-style storage/processing can fit.
If latency or streaming is required, I would consider Spark, Flink, Kafka, lakehouse, or warehouse tools.
```

This shows maturity.

## 10. Trade-offs

| What Hadoop Gives | What Hadoop Struggles With |
|---|---|
| cheap distributed batch scale | low-latency serving |
| durable replicated storage | small files |
| mature ecosystem | operational complexity |
| high-throughput processing | iterative/interactive workloads |

## 11. Failure Modes

- Failure: NameNode overloaded by tiny files.
- Symptom: slow metadata operations or instability.
- Recovery: compact files.
- Prevention: write larger files and use efficient formats.

- Failure: Cluster queue congestion.
- Symptom: jobs stuck waiting.
- Recovery: tune YARN queues and capacity.
- Prevention: workload isolation and scheduling.

- Failure: MapReduce jobs too slow for business SLA.
- Symptom: reports miss deadlines.
- Recovery: optimize or migrate to Spark/warehouse.
- Prevention: choose engine based on latency requirement.

## 12. Common Mistakes

- Mistake: Assuming Hadoop is obsolete and useless.
- Why it is wrong: concepts and many legacy systems still matter.
- Better approach: learn Hadoop concepts and understand modern evolution.

- Mistake: Choosing Hadoop for real-time APIs.
- Why it is wrong: Hadoop is batch/file oriented.
- Better approach: use serving databases, caches, and streaming systems.

## 13. Mini Example

Bad fit:

```text
Need latest user recommendation in 50 ms -> Hadoop batch job
```

Better fit:

```text
Nightly recompute recommendations for 100M users -> Hadoop/Spark batch
```

## 14. Interview Questions

1. What are Hadoop's main limitations?
2. Why are small files bad in HDFS?
3. Why is MapReduce slow for iterative workloads?
4. When would you avoid Hadoop?
5. What modern tools solved Hadoop limitations?

## 15. Interview Speak

"Classic Hadoop is strong for large-scale batch storage and processing, but it struggles with low-latency serving, small files, operational complexity, random updates, and iterative workloads. I would use Hadoop concepts for batch-scale reasoning but choose Spark, Kafka, Flink, warehouses, or lakehouse tools when requirements demand lower latency or better developer experience."

## 16. Quick Recall

- One-line summary: Hadoop is powerful for batch scale but heavy for low-latency and interactive workloads.
- Three keywords: batch, small files, operations.
- One trap: Using Hadoop for every Big Data problem.
- One memory trick: Hadoop is a truck, not a bike.
