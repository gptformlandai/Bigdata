# Topic 040: Distributed Systems

## Goal

Understand what a distributed system is and why Big Data platforms are almost always distributed.

## Simple Explanation

A distributed system is many computers working together as if they are one system.

You use distributed systems when one machine is not enough for the data size, traffic, reliability, or geographic reach.

## Core Idea

- Definition: A distributed system is a collection of independent machines that communicate over a network to provide a shared service.
- Why it matters: Big Data systems need many machines for storage, compute, fault tolerance, and scale.
- Related terms: node, cluster, network, partition, replication, coordination, consensus.

## Why We Distribute Systems

Main reasons:

- store more data than one machine can hold
- process data faster in parallel
- survive machine failure
- serve users from multiple regions
- scale traffic horizontally
- isolate workloads

## What Gets Harder

Distributed systems are powerful but tricky because:

- networks fail
- messages can be delayed or duplicated
- clocks disagree
- machines crash
- retries create duplicates
- data replicas can diverge
- coordination can reduce availability

The central mental model:

```text
One machine: simpler correctness, limited scale
Many machines: larger scale, harder correctness
```

## How It Is Used

Examples:

- Kafka cluster
- Spark cluster
- HDFS
- Cassandra
- DynamoDB
- Elasticsearch
- Redis cluster
- Kubernetes
- Snowflake/BigQuery-style warehouses

## Big Data / System Design Angle

In Big Data, distribution appears in:

- storage: data split across nodes
- compute: jobs run across many workers
- messaging: topics partitioned across brokers
- metadata: leaders and consensus protect cluster state
- serving: load balancers route requests across instances

Interview trigger words:

- scale
- high availability
- fault tolerance
- cluster
- sharding
- replication
- multi-region
- throughput

## Common Mistakes

- Mistake: Thinking distributed systems are just "more servers."
- Better way: Mention coordination, failure handling, and data consistency.

- Mistake: Ignoring partial failure.
- Better way: Design assuming some nodes fail while others continue.

- Mistake: Applying single-machine assumptions.
- Better way: Assume network delay, retries, duplicates, and stale data are possible.

## Interview Speak

"A distributed system uses multiple machines to provide one service. We do this for scale, availability, and parallel processing, but we pay with complexity: partial failures, network delays, consistency trade-offs, coordination, retries, and observability."

## Quick Recall

- One-liner: Many machines cooperate to act like one system.
- Keywords: nodes, network, partial failure.
- Trap: Forgetting that partial failure is normal.
