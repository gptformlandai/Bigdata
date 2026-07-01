# Topic 063: NameNode And DataNode

## 1. Goal

Understand the two main HDFS roles: NameNode manages metadata, DataNodes store actual data blocks.

## 2. Baby Intuition

Imagine a library.

- The librarian knows where every book is located.
- The shelves physically hold the books.

In HDFS:

- NameNode is the librarian.
- DataNodes are the shelves.

## 3. What It Is

- Simple definition: NameNode tracks file metadata; DataNodes store file blocks.
- Technical definition: The NameNode manages the HDFS namespace and block mapping, while DataNodes store and serve blocks and report health to the NameNode.
- Category: HDFS architecture components.
- Related terms: namespace, block report, heartbeat, fsimage, edit log, standby NameNode.

## 4. Why It Exists

HDFS needs to answer two separate questions:

```text
What files exist?
Where are their blocks stored?
```

The NameNode handles those questions.

DataNodes handle the heavy work:

```text
store bytes
serve reads
accept writes
replicate blocks
```

This separation keeps metadata control centralized while storage scales across many machines.

## 5. Where It Fits In A Data Platform

```text
Client / Hive / Spark / MapReduce
  -> asks NameNode for metadata
  -> reads/writes actual blocks from DataNodes
```

The NameNode is part of the storage control plane.

The DataNodes are part of the storage data plane.

## 6. How It Works Step By Step

Read path:

1. Client asks NameNode: "Where are blocks for `/data/orders.csv`?"
2. NameNode returns block locations.
3. Client reads blocks directly from DataNodes.
4. DataNodes stream block bytes to client.

Write path:

1. Client asks NameNode to create file.
2. NameNode chooses DataNodes for block replicas.
3. Client writes block to first DataNode.
4. First DataNode pipelines replica to next DataNode.
5. DataNodes acknowledge successful writes.
6. NameNode records metadata.

Health path:

1. DataNodes send heartbeats to NameNode.
2. DataNodes send block reports.
3. If heartbeat stops, NameNode marks DataNode dead.
4. Missing replicas are recreated elsewhere.

## 7. How To Use It Practically

Useful commands:

```bash
hdfs dfsadmin -report
hdfs fsck / -blocks -locations
hdfs dfs -ls /
```

What to look for:

- live DataNodes
- dead DataNodes
- under-replicated blocks
- missing blocks
- storage capacity

## 8. Real-World Scenario

- Product/system: Enterprise Hadoop data lake.
- Problem: Thousands of files are stored across hundreds of servers.
- How NameNode/DataNode helps: NameNode knows metadata; DataNodes scale storage.
- What would go wrong without it: Clients would not know where file blocks live, and failure recovery would be chaotic.

## 9. System Design Angle

NameNode is a critical component.

Old Hadoop had a single NameNode risk. Modern clusters use high availability:

```text
Active NameNode + Standby NameNode
```

DataNodes can be many because storage must scale horizontally.

Design considerations:

- NameNode memory limits number of files/blocks.
- DataNode failures are expected.
- Block reports and heartbeats drive recovery.
- HA avoids NameNode single point of failure.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| simple metadata authority | NameNode is critical |
| scalable data storage | metadata memory pressure |
| easier block tracking | small files hurt |
| automatic failure detection | heartbeat/report overhead |

## 11. Failure Modes

- Failure: DataNode stops heartbeating.
- Symptom: NameNode marks it dead.
- Recovery: blocks are re-replicated from surviving replicas.
- Prevention: monitoring, replication, rack awareness.

- Failure: NameNode unavailable.
- Symptom: clients cannot create/open files.
- Recovery: failover to standby NameNode.
- Prevention: HA setup and metadata checkpoints.

- Failure: NameNode memory pressure.
- Symptom: slow metadata operations or risk of outage.
- Recovery: reduce file/block count, increase memory.
- Prevention: avoid small files.

## 12. Common Mistakes

- Mistake: Thinking NameNode stores all file data.
- Why it is wrong: NameNode stores metadata; DataNodes store bytes.
- Better approach: Say NameNode tracks namespace and block locations.

- Mistake: Ignoring NameNode memory.
- Why it is wrong: Every file and block uses metadata.
- Better approach: compact small files and plan metadata capacity.

## 13. Mini Example

```text
/data/orders.csv
  block_1 -> DataNode A, DataNode B, DataNode C
  block_2 -> DataNode B, DataNode D, DataNode E
```

NameNode stores this map.

DataNodes store the actual block bytes.

## 14. Interview Questions

1. What does NameNode store?
2. What does DataNode store?
3. How does NameNode detect DataNode failure?
4. Why is NameNode HA important?
5. Why do small files affect NameNode?

## 15. Interview Speak

"In HDFS, NameNode manages metadata like namespace and block locations, while DataNodes store actual blocks. Clients ask NameNode for locations, then read/write directly to DataNodes. DataNodes send heartbeats and block reports, and NameNode handles re-replication when nodes fail."

## 16. Quick Recall

- One-line summary: NameNode knows where data is; DataNodes hold the data.
- Three keywords: metadata, blocks, heartbeat.
- One trap: Saying NameNode stores the full data.
- One memory trick: NameNode is the map; DataNodes are the storage.
