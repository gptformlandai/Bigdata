# Topic 072: HBase

## 1. Goal

Understand HBase as a NoSQL database on top of Hadoop-style storage for large-scale random reads and writes.

## 2. Baby Intuition

HDFS is great for huge files, but bad for changing one small row quickly.

HBase is like putting a fast key-based table layer on top of the Hadoop ecosystem.

If HDFS is a warehouse of big files, HBase is a giant sorted cabinet where you can quickly find a row by key.

## 3. What It Is

- Simple definition: HBase is a distributed NoSQL database for huge tables.
- Technical definition: Apache HBase is a distributed, column-family-oriented database inspired by Google Bigtable, commonly backed by HDFS, supporting random real-time reads and writes at large scale.
- Category: NoSQL wide-column store.
- Related terms: row key, column family, region, RegionServer, HFile, WAL, ZooKeeper.

## 4. Why It Exists

HDFS is optimized for:

- large files
- sequential reads
- write once/read many
- batch processing

But some systems need:

- lookup one user quickly
- update one row
- read recent values by key
- store sparse tables with billions of rows

HBase exists to provide random access over huge datasets.

## 5. Where It Fits In A Data Platform

```text
Applications / Batch jobs / Streams
  -> HBase
  -> HDFS-backed storage
```

HBase can serve:

- operational lookups
- feature lookup
- counters
- time-series-like data
- sparse wide tables

It is not primarily a SQL analytics warehouse.

## 6. How It Works Step By Step

Key ideas:

- data is sorted by row key
- rows are split into regions
- regions are served by RegionServers
- writes go to write-ahead log and memory
- data is flushed into immutable HFiles
- compaction merges files over time

Write flow:

1. Client writes row key and columns.
2. RegionServer receives write.
3. Write goes to WAL for durability.
4. Write goes to MemStore in memory.
5. MemStore flushes to HFiles.
6. Compaction later merges files.

Read flow:

1. Client asks for row key.
2. Request routes to RegionServer owning that key range.
3. RegionServer checks memory and HFiles.
4. Result is returned.

## 7. How To Use It Practically

HBase shell examples:

```bash
create 'users', 'profile'
put 'users', 'user_1', 'profile:name', 'Aravind'
put 'users', 'user_1', 'profile:city', 'Hyderabad'
get 'users', 'user_1'
scan 'users'
```

Important design choice:

```text
row key design is everything
```

Bad row key can create hot regions.

## 8. Real-World Scenario

- Product/system: User activity lookup service.
- Problem: Need to fetch recent user activity by user id quickly from billions of records.
- How HBase helps: Stores rows by key and serves random reads at scale.
- What would go wrong without it: HDFS/Hive would require scanning files, which is too slow for lookup use cases.

## 9. System Design Angle

Choose HBase-like systems when:

- dataset is huge
- random key-based read/write is needed
- schema is sparse/flexible
- access pattern is known by row key

Avoid when:

- you need rich SQL joins
- you need complex ad hoc analytics
- you need simple small relational data
- row key access pattern is unclear

Modern related systems:

- Bigtable
- Cassandra
- DynamoDB
- Cloud Bigtable

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| random reads/writes at scale | row-key design complexity |
| huge sparse tables | limited relational features |
| horizontal scaling | operational complexity |
| high write throughput | compaction/tuning overhead |

## 11. Failure Modes

- Failure: Hot region.
- Symptom: one RegionServer overloaded.
- Recovery: split region or redesign key.
- Prevention: avoid monotonically increasing hot keys.

- Failure: RegionServer failure.
- Symptom: regions temporarily unavailable.
- Recovery: regions reassigned to other servers.
- Prevention: replication and monitoring.

- Failure: Compaction pressure.
- Symptom: read/write latency spikes.
- Recovery: tune compaction and resources.
- Prevention: capacity planning.

## 12. Common Mistakes

- Mistake: Designing row key as timestamp only.
- Why it is wrong: new writes hit same region.
- Better approach: use salting/reverse timestamp/composite keys depending on access pattern.

- Mistake: Using HBase like a relational database.
- Why it is wrong: joins and SQL-style modeling are not its strength.
- Better approach: model around query patterns.

## 13. Mini Example

Good mental model:

```text
row key: user_id#reverse_timestamp
```

This supports:

```text
get recent events for one user
```

## 14. Interview Questions

1. Why was HBase created if HDFS already exists?
2. What is a row key in HBase?
3. What is a hot region?
4. How is HBase different from Hive?
5. When would you choose HBase vs a warehouse?

## 15. Interview Speak

"HBase is a distributed wide-column NoSQL database for random reads and writes at massive scale. It is useful when HDFS/Hive scans are too slow for key-based access. The most important design decision is row key design, because poor keys can create hot regions and uneven load."

## 16. Quick Recall

- One-line summary: HBase gives key-based random access over huge distributed tables.
- Three keywords: row key, RegionServer, column family.
- One trap: Using HBase for ad hoc SQL analytics.
- One memory trick: HDFS scans big files; HBase finds rows by key.
