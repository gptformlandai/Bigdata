# Topic 042: Partitioning / Sharding

## Goal

Understand how systems split data across machines to scale storage and throughput.

## Simple Explanation

Partitioning means dividing a large dataset into smaller pieces.

Sharding usually means distributing those pieces across different machines.

## Core Idea

- Definition: Partitioning splits data into subsets; sharding places those subsets across nodes.
- Why it matters: One machine cannot store or process unlimited data.
- Related terms: shard key, partition key, hot partition, range partitioning, hash partitioning, rebalancing.

## Common Strategies

| Strategy | How It Works | Strength | Risk |
|---|---|---|---|
| Hash partitioning | hash key maps to partition | even distribution | range queries harder |
| Range partitioning | key ranges map to partitions | efficient range scans | hot ranges |
| Time partitioning | date/time maps to partition | great for logs/events | latest partition can be hot |
| Tenant partitioning | tenant/customer id maps to partition | isolation | large tenant skew |

## How It Works

Example by customer id:

```text
hash(customer_id) % number_of_shards -> shard number
```

Data flow:

1. Choose partition key.
2. Compute target partition.
3. Route write to that partition.
4. Query either one partition or many partitions.

## Big Data / System Design Angle

Partitioning is one of the most important scaling choices.

Good partitioning:

- spreads load evenly
- keeps common queries efficient
- limits blast radius
- enables parallelism

Bad partitioning:

- creates hot shards
- makes queries scan too much data
- complicates joins and transactions
- makes rebalancing painful

Interview trigger words:

- data too large for one machine
- high write throughput
- hot users/tenants
- multi-tenant system
- time-series data
- Kafka partitions
- database sharding

## Example

Clickstream table partitioned by date:

```text
s3://lake/clicks/dt=2026-07-01/
s3://lake/clicks/dt=2026-07-02/
```

Query with partition pruning:

```sql
SELECT COUNT(*)
FROM clicks
WHERE dt = '2026-07-01';
```

The engine can skip other dates.

## Common Mistakes

- Mistake: Choosing a low-cardinality key.
- Better way: Use keys with enough distinct values to spread load.

- Mistake: Ignoring access patterns.
- Better way: Partition based on common filters and write patterns.

- Mistake: Creating hot partitions.
- Better way: detect skew and use salting, better keys, or adaptive strategies.

## Interview Speak

"Partitioning splits data so storage and work can scale horizontally. The hardest part is choosing the partition key. It should distribute load evenly while supporting common queries. I would watch for hot partitions, cross-shard joins, rebalancing, and transaction complexity."

## Quick Recall

- One-liner: Partitioning splits data; sharding spreads it across machines.
- Keywords: partition key, hot shard, rebalancing.
- Trap: Picking a key that matches one query but destroys load distribution.
