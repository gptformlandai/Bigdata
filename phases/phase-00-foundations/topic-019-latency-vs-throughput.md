# Topic 019: Latency vs Throughput

## Goal

Understand the difference between speed for one request and capacity across many requests.

## Simple Explanation

Latency is how long one thing takes.

Throughput is how many things you can complete per unit of time.

Example:

```text
Latency: one food delivery takes 25 minutes.
Throughput: the restaurant completes 200 orders per hour.
```

## Core Idea

- Definition: Latency measures time per operation; throughput measures operations per time.
- Why it matters: Systems can be low-latency, high-throughput, both, or neither.
- Related terms: p50, p95, p99, QPS, RPS, TPS, batch size, backpressure.

## Key Metrics

| Metric | Meaning |
|---|---|
| p50 latency | median request time |
| p95 latency | 95 percent of requests finish within this time |
| p99 latency | tail latency; worst user experience for 1 percent |
| QPS/RPS | queries/requests per second |
| TPS | transactions per second |
| MB/s or GB/s | data throughput |

## How It Is Used

Examples:

- API latency: `p95 < 200 ms`
- Kafka throughput: `100 MB/s`
- Spark job runtime: `30 minutes`
- Warehouse query latency: `p95 < 10 seconds`
- Batch pipeline SLA: `complete by 7 AM`

## Big Data / System Design Angle

Batch systems often optimize throughput:

- process TBs efficiently
- tolerate minutes or hours
- use large batches and parallelism

Serving systems often optimize latency:

- respond quickly to users
- use indexes, caches, precomputation
- avoid large scans

Streaming systems balance both:

- process high event volume
- keep end-to-end delay low

## Trade-offs

| Optimization | Helps | Can Hurt |
|---|---|---|
| Larger batches | throughput | latency |
| Caching | latency | freshness/complexity |
| More parallelism | throughput | coordination/cost |
| Compression | network throughput/cost | CPU latency |
| Strong consistency | correctness | latency/availability |

## Example

System A:

```text
10 ms latency, 100 requests/sec
```

System B:

```text
500 ms latency, 100,000 requests/sec
```

Neither is universally better. A fraud API may prefer System A. A nightly ETL job may prefer System B.

## Common Mistakes

- Mistake: Saying "fast" without defining latency or throughput.
- Better way: State the metric and percentile.

- Mistake: Optimizing average latency only.
- Better way: Look at p95 and p99 tail latency.

- Mistake: Using real-time architecture for daily reporting.
- Better way: Match freshness and latency requirements to business need.

## Interview Speak

"Latency is time per operation, while throughput is operations or data volume per unit time. For user-facing APIs I care about p95 and p99 latency. For Big Data pipelines I often care about throughput and SLA. Design choices like batching, caching, indexing, and parallelism depend on which metric matters most."

## Quick Recall

- One-liner: Latency is time for one; throughput is amount per time.
- Keywords: p95, QPS, batch.
- Trap: Optimizing average latency while p99 is terrible.
