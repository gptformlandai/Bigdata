# Topic 052: Backpressure

## Goal

Understand how systems protect themselves when producers send data faster than consumers can handle.

## Simple Explanation

Backpressure is a system saying:

```text
Slow down. I cannot keep up.
```

Without it, queues grow, memory fills, latency explodes, and systems crash.

## Core Idea

- Definition: Backpressure is flow control that prevents overload by slowing producers or limiting intake.
- Why it matters: Distributed systems often have different producer and consumer speeds.
- Related terms: queue, buffer, consumer lag, rate limiting, load shedding, throttling.

## How Overload Happens

Example:

```text
producer sends 100K events/sec
consumer processes 40K events/sec
```

Difference:

```text
60K events/sec backlog growth
```

Eventually:

- queue grows
- memory grows
- latency rises
- retries increase
- failures cascade

## Backpressure Techniques

- bounded queues
- rate limiting
- consumer lag monitoring
- throttling producers
- pausing reads
- load shedding
- autoscaling consumers
- batching
- prioritization

## Big Data / System Design Angle

Backpressure is critical in:

- Kafka consumers
- Spark streaming
- Flink pipelines
- API ingestion
- log processing
- CDC pipelines
- queue workers

Healthy design:

```text
detect overload -> slow intake -> preserve stability -> recover backlog
```

## Example

Kafka consumer lag:

```text
latest broker offset: 1,000,000
consumer committed offset: 700,000
lag: 300,000 messages
```

High lag means consumers are behind.

## Common Mistakes

- Mistake: Unlimited queues.
- Better way: Bound queues and decide what happens when full.

- Mistake: Autoscaling without fixing bottleneck.
- Better way: identify CPU, I/O, downstream dependency, partition count, or skew.

- Mistake: Treating lag as always bad.
- Better way: small temporary lag can be normal; sustained growing lag is dangerous.

## Interview Speak

"Backpressure protects a system when input exceeds processing capacity. I would monitor queue depth or consumer lag, use bounded buffers, throttle producers, autoscale consumers, batch work, or shed low-priority load. Without backpressure, overload becomes memory pressure, latency spikes, and cascading failure."

## Quick Recall

- One-liner: Backpressure is controlled slowing under overload.
- Keywords: lag, queue, throttle.
- Trap: Unlimited buffering.
