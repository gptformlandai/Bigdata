# Topic 065: Replication Factor

## 1. Goal

Understand HDFS replication factor and how it protects data from machine and disk failures.

## 2. Baby Intuition

If an important document exists in only one place, losing that place loses the document.

So you make copies and store them in different places.

HDFS does the same with blocks.

## 3. What It Is

- Simple definition: Replication factor is the number of copies HDFS keeps for each block.
- Technical definition: HDFS replication factor controls how many block replicas are stored across DataNodes, commonly 3 by default.
- Category: Fault tolerance and durability setting.
- Related terms: replica, under-replicated block, rack awareness, DataNode failure.

## 4. Why It Exists

Hadoop assumes machines fail.

Replication exists because:

- disks fail
- DataNodes crash
- racks can lose power/network
- jobs still need to read data
- data loss is unacceptable

Instead of relying on perfect hardware, HDFS stores extra copies.

## 5. Where It Fits In A Data Platform

```text
File -> HDFS blocks -> replicated block copies -> DataNodes/racks
```

Replication is part of HDFS storage reliability.

Processing tools like MapReduce, Hive, and Spark benefit because they can read from another replica if one node is unavailable.

## 6. How It Works Step By Step

With replication factor 3:

1. File is split into blocks.
2. Each block is stored on 3 DataNodes.
3. NameNode tracks all replica locations.
4. DataNodes send heartbeats and block reports.
5. If one DataNode fails, NameNode detects missing replicas.
6. NameNode schedules new replicas on healthy nodes.

Example:

```text
block_1 replicas:
  DataNode A
  DataNode B
  DataNode C
```

If DataNode B fails:

```text
block_1 replicas:
  DataNode A
  DataNode C
  DataNode D  # new replica
```

## 7. How To Use It Practically

Set replication when uploading or changing files:

```bash
hdfs dfs -setrep -w 3 /data/orders
hdfs dfs -stat %r /data/orders/file.csv
```

Check under-replicated blocks:

```bash
hdfs fsck / -blocks
hdfs dfsadmin -report
```

Common defaults:

```text
replication factor = 3
```

## 8. Real-World Scenario

- Product/system: Enterprise log archive.
- Problem: Logs must survive disk and node failure.
- How replication helps: Each block has multiple copies, so a single failure does not lose data.
- What would go wrong without it: One disk failure could permanently lose part of a file.

## 9. System Design Angle

Replication factor affects:

- durability
- availability
- storage cost
- write network traffic
- read flexibility

Trade-off:

```text
higher replication -> safer reads and durability -> more storage and network cost
```

For critical data, use adequate replication.

For temporary intermediate data, lower replication may sometimes be acceptable.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| tolerate node failure | extra storage cost |
| more read locations | more write network traffic |
| better durability | longer re-replication after failures |
| rack-level safety with rack awareness | placement complexity |

## 11. Failure Modes

- Failure: Under-replicated blocks.
- Symptom: fewer copies than desired.
- Recovery: NameNode schedules replication.
- Prevention: enough disk capacity and healthy DataNodes.

- Failure: Missing blocks.
- Symptom: no replica exists for a block.
- Recovery: restore from backup if available.
- Prevention: replication, backups, monitoring.

- Failure: All replicas on same rack.
- Symptom: rack outage can lose availability.
- Recovery: re-replicate across racks.
- Prevention: rack awareness.

## 12. Common Mistakes

- Mistake: Thinking replication is backup.
- Why it is wrong: replication protects against hardware failure, but bad deletes/corruption can replicate too.
- Better approach: use backups/snapshots for disaster recovery.

- Mistake: Setting replication too high blindly.
- Why it is wrong: storage and network cost increase.
- Better approach: match replication to data criticality.

## 13. Mini Example

1 TB logical data with replication factor 3:

```text
logical data: 1 TB
physical storage used: about 3 TB
```

Before compression and storage overhead.

## 14. Interview Questions

1. What is replication factor?
2. Why is 3 a common replication factor?
3. What happens when a block is under-replicated?
4. Is replication the same as backup?
5. How does replication affect storage cost?

## 15. Interview Speak

"Replication factor controls how many copies of each HDFS block exist. A common value is 3, which lets HDFS survive node or disk failure by reading another replica and re-replicating missing copies. The trade-off is storage and network overhead."

## 16. Quick Recall

- One-line summary: Replication factor is how many block copies HDFS keeps.
- Three keywords: replicas, durability, storage cost.
- One trap: Calling replication a full backup strategy.
- One memory trick: One block, three copies, fewer panic attacks.
