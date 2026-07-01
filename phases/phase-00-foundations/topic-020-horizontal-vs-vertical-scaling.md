# Topic 020: Horizontal vs Vertical Scaling

## Goal

Understand the two main ways to increase system capacity and why Big Data systems usually depend on horizontal scaling.

## Simple Explanation

Vertical scaling means buying a bigger machine.

Horizontal scaling means adding more machines.

Example:

```text
Vertical: one stronger server
Horizontal: ten regular servers working together
```

## Core Idea

- Definition: Vertical scaling increases resources on one machine; horizontal scaling adds more machines or nodes.
- Why it matters: Big Data workloads often exceed what one machine can handle.
- Related terms: scale up, scale out, partitioning, sharding, replication, load balancing.

## Comparison

| Dimension | Vertical Scaling | Horizontal Scaling |
|---|---|---|
| Method | add CPU/RAM/disk to one node | add more nodes |
| Simplicity | simpler | more complex |
| Limit | hardware ceiling | coordination and distributed complexity |
| Failure risk | one big node can be a bottleneck | failure can be spread across nodes |
| Cost curve | expensive at high end | often better for large scale |
| Common use | small/medium databases | Big Data, distributed systems |

## How It Is Used

Vertical scaling:

- increase database instance size
- add RAM for caching
- use faster disks
- add CPU for query processing

Horizontal scaling:

- add Kafka brokers
- add Spark executors
- add database shards
- add web servers behind a load balancer
- add storage nodes

## Big Data / System Design Angle

Big Data relies on horizontal scaling because:

- data can be partitioned
- compute can run in parallel
- storage can be distributed
- failures can be isolated
- capacity can grow incrementally

But horizontal scaling requires:

- partitioning strategy
- load balancing
- replication
- coordination
- monitoring
- handling partial failure

## Example

A table grows from 100 GB to 100 TB.

Vertical-only approach:

```text
buy a larger database server
```

Problem:

- eventually hits hardware and cost limits

Horizontal approach:

```text
partition data by customer_id or date across many nodes
```

New challenge:

- queries, joins, and transactions across partitions become harder

## Common Mistakes

- Mistake: Scaling horizontally before understanding the bottleneck.
- Better way: Measure CPU, memory, disk, network, locks, and query plans first.

- Mistake: Assuming horizontal scaling is automatic.
- Better way: Design stateless services, partition data, and handle coordination.

- Mistake: Ignoring hot partitions.
- Better way: choose partition keys that spread load evenly.

- Mistake: Scaling compute when storage layout is the issue.
- Better way: fix partitioning, file size, clustering, or indexes first.

## Interview Speak

"Vertical scaling adds resources to one machine and is simpler, but has hardware and cost limits. Horizontal scaling adds more machines and is the foundation of Big Data systems, but requires partitioning, replication, load balancing, and failure handling. I would first identify the bottleneck, then choose the scaling strategy."

## Quick Recall

- One-liner: Scale up means bigger machine; scale out means more machines.
- Keywords: partitioning, load balancing, replication.
- Trap: Adding nodes without fixing skew or bad partitioning.
