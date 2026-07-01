# Topic 280: Performance Tuning Questions

## 1. Goal

Prepare answers for tuning Spark, SQL, Kafka, lakehouse, and warehouse workloads.

## 2. Baby Intuition

Performance tuning is finding where time or resources are wasted.

Do not randomly add machines. First find the bottleneck.

## 3. Universal Tuning Framework

Use:

1. Define the symptom.
2. Measure baseline.
3. Identify bottleneck.
4. Change one thing.
5. Measure again.
6. Keep or revert.

## 4. Spark Tuning

Check:

- Spark UI
- slow stage
- shuffle size
- data skew
- spills
- join strategy
- partition count
- cache usage
- input/output file count

Fixes:

- filter early
- select fewer columns
- broadcast small table
- salt skewed keys
- enable/use AQE
- tune partitions
- compact small files
- cache only reused data

## 5. SQL/Warehouse Tuning

Check:

- query plan
- data scanned
- partition pruning
- clustering/sort keys
- join explosion
- repeated subqueries
- materialized view opportunities

Fixes:

- add date filters
- select only needed columns
- pre-aggregate
- use proper join keys
- create materialized views
- cluster/sort by common filters
- avoid count distinct when approximate is acceptable

## 6. Kafka Tuning

Check:

- producer throughput
- batch size
- compression
- partition count
- consumer lag
- processing latency
- downstream sink
- hot partitions

Fixes:

- increase partitions for future scale
- tune batching/compression
- scale consumers if partitions allow
- improve sink writes
- choose better key distribution
- avoid excessive rebalances

## 7. Lakehouse Tuning

Check:

- small files
- bad partitioning
- too many table snapshots
- no clustering
- expensive MERGE
- metadata growth

Fixes:

- compaction
- partition evolution
- clustering/Z-order/sort
- hidden partitioning where supported
- expire old snapshots
- batch upserts
- optimize file sizes

## 8. Airflow/Orchestration Tuning

Check:

- too much work inside tasks
- scheduler overloaded
- sensors blocking workers
- task granularity
- dependency bottlenecks
- backfills overwhelming systems

Fixes:

- push heavy compute to Spark/warehouse
- use deferrable sensors
- set pools/concurrency
- split/merge tasks sensibly
- throttle backfills

## 9. Common Tuning Traps

| Trap | Better Approach |
|---|---|
| adding more nodes first | measure bottleneck first |
| caching everything | cache only reused expensive data |
| partitioning too much | avoid small files and metadata overhead |
| ignoring skew | inspect task duration distribution |
| optimizing rare query | focus on high-impact workload |

## 10. Sample Strong Answer

Question:

```text
A daily Spark job that used to take 20 minutes now takes 2 hours. What do you do?
```

Answer:

```text
I compare current and previous runs in Spark UI and pipeline metrics. I check input size, partition count, shuffle size, stage duration, skew, spills, and join plan. I also check recent code/schema/data distribution changes. If one stage is slow due to shuffle or skew, I tune join strategy, salt hot keys, pre-aggregate, or adjust partitions. I measure each change and add monitoring so the regression is caught earlier next time.
```

## 11. Interview Speak

"I tune based on evidence. I identify whether the bottleneck is scan, shuffle, skew, memory, network, sink writes, or query planning. Then I apply the smallest targeted change and compare metrics before and after."

## 12. Quick Recall

- One-line summary: Tune by measuring bottlenecks, not guessing.
- Three keywords: baseline, bottleneck, measure.
- One trap: adding cluster resources before diagnosis.
- Memory trick: find the slow pipe before buying a bigger pump.

