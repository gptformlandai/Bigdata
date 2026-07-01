# Topic 005: Compression: gzip, snappy, zstd

## Goal

Understand why compression matters and how common compression algorithms trade CPU for storage and network savings.

## Simple Explanation

Compression makes data smaller.

It is like folding clothes before packing a suitcase. You save space, but you spend some effort folding and unfolding. In systems, that effort is CPU time.

## Core Idea

- Definition: Compression encodes data using fewer bytes.
- Why it matters: Smaller data usually means lower storage cost, less network transfer, and faster disk reads.
- Related terms: codec, compression ratio, decompression, splittable files, CPU cost.

## Common Codecs

| Codec | Compression Ratio | Speed | Common Use |
|---|---|---|---|
| gzip | high | slower | archival, simple compressed files |
| snappy | moderate | very fast | Spark, Kafka, Parquet, low-latency pipelines |
| zstd | high | fast | modern analytics, logs, lakehouse tables |

## How It Is Used

Compression appears in:

- Kafka messages
- Parquet and ORC files
- log files
- object storage datasets
- network transfer
- backups and archives

Practical choices:

- Use snappy when speed matters.
- Use gzip when compatibility and compression ratio matter more than speed.
- Use zstd when you want strong compression with good speed and your tools support it.

## Big Data / System Design Angle

Compression can improve performance because distributed systems are often limited by disk and network, not CPU.

But compression is not free:

- writing compressed data uses CPU
- reading compressed data requires decompression
- some compressed formats are harder to split for parallel processing

Important idea:

```text
smaller data -> less I/O and network
more compression -> more CPU
```

## Example

If a pipeline writes 10 TB/day uncompressed and compression reduces it by 70 percent:

```text
10 TB/day -> 3 TB/day stored
```

That saves:

- storage cost
- network cost
- query scan cost

But it adds:

- CPU while writing
- CPU while reading

## Common Mistakes

- Mistake: Thinking maximum compression is always best.
- Better way: Balance compression ratio with CPU and latency.

- Mistake: Compressing tiny files individually.
- Better way: Fix tiny files first, then compress larger analytical files.

- Mistake: Ignoring tool compatibility.
- Better way: Confirm the codec works with Spark, Hive, Trino, Kafka, or your warehouse engine.

## Interview Speak

"Compression reduces storage, network, and scan cost, but adds CPU overhead. For Big Data analytics I would commonly use Parquet with snappy or zstd. For archival data I might choose stronger compression. The right codec depends on whether the bottleneck is CPU, disk, network, cost, or latency."

## Quick Recall

- One-liner: Compression saves bytes but spends CPU.
- Keywords: gzip, snappy, zstd.
- Trap: Choosing the strongest compression without considering latency and CPU.
