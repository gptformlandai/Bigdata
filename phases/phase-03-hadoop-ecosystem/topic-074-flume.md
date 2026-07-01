# Topic 074: Flume

## 1. Goal

Understand Flume as a Hadoop-era tool for collecting and moving streaming log data into HDFS.

## 2. Baby Intuition

Imagine many application servers producing log lines all day.

Flume is like a network of pipes that collects those logs and pours them into Hadoop storage.

## 3. What It Is

- Simple definition: Flume collects, aggregates, and moves log/event data into Hadoop.
- Technical definition: Apache Flume is a distributed service for efficiently collecting, aggregating, and transporting large amounts of streaming event data, commonly into HDFS or HBase.
- Category: Data ingestion/log collection tool.
- Related terms: source, channel, sink, agent, event, HDFS sink.

## 4. Why It Exists

Large systems generate logs continuously.

Teams needed a way to:

- collect logs from many servers
- buffer them
- handle temporary failures
- write them into HDFS
- scale ingestion

Before Flume, teams often used custom log copy scripts, which were fragile.

## 5. Where It Fits In A Data Platform

```text
Application logs -> Flume agents -> HDFS/HBase -> Hive/MapReduce/Spark
```

Flume is an ingestion layer.

It often sits before Hadoop storage.

## 6. How It Works Step By Step

Flume agent has three main parts:

- Source: receives data.
- Channel: buffers data.
- Sink: writes data to destination.

Flow:

1. Source receives event, such as a log line.
2. Event is stored in channel.
3. Sink reads event from channel.
4. Sink writes event to HDFS/HBase/another destination.
5. If sink fails, channel can buffer until recovery depending on channel type.

Simple:

```text
source -> channel -> sink
```

## 7. How To Use It Practically

Flume config shape:

```properties
agent.sources = src
agent.channels = ch
agent.sinks = sink

agent.sources.src.type = exec
agent.sources.src.command = tail -F /var/log/app.log

agent.channels.ch.type = memory

agent.sinks.sink.type = hdfs
agent.sinks.sink.hdfs.path = hdfs://cluster/logs/app/%Y/%m/%d

agent.sources.src.channels = ch
agent.sinks.sink.channel = ch
```

Important:

- memory channel is faster but less durable
- file channel is slower but more durable

## 8. Real-World Scenario

- Product/system: Web server log analytics.
- Problem: Thousands of servers produce access logs continuously.
- How Flume helps: Agents collect logs and write them into HDFS by date/hour.
- What would go wrong without it: Logs may be copied inconsistently, late, or lost during failures.

## 9. System Design Angle

Flume is useful for:

- log ingestion
- Hadoop landing zones
- simple streaming event movement

Less common in modern systems where teams use:

- Kafka
- Fluentd/Fluent Bit
- Logstash
- cloud logging agents
- Kinesis/Pub/Sub/Event Hubs

Design questions:

- Is loss acceptable?
- How much buffering is needed?
- What happens if HDFS is down?
- How are files rolled by time/size?
- How do we avoid tiny files?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| simple log ingestion to Hadoop | older ecosystem tool |
| source-channel-sink model | config complexity |
| buffering | durability depends on channel |
| HDFS integration | small file risk |

## 11. Failure Modes

- Failure: Sink cannot write to HDFS.
- Symptom: channel fills.
- Recovery: sink resumes later if channel has capacity.
- Prevention: durable channel and monitoring.

- Failure: Memory channel crash.
- Symptom: buffered events lost.
- Recovery: accept loss or replay from source if possible.
- Prevention: file channel for stronger durability.

- Failure: Too many small HDFS files.
- Symptom: NameNode pressure and slow queries.
- Recovery: compact files.
- Prevention: configure rolling intervals/sizes carefully.

## 12. Common Mistakes

- Mistake: Using memory channel for critical logs.
- Why it is wrong: crash can lose buffered events.
- Better approach: use file channel or stronger ingestion system.

- Mistake: Rolling HDFS files too frequently.
- Why it is wrong: creates many tiny files.
- Better approach: tune file roll size and interval.

## 13. Mini Example

Flume mental model:

```text
tail app.log -> buffer events -> write to HDFS path by date
```

## 14. Interview Questions

1. What problem does Flume solve?
2. What are source, channel, and sink?
3. What is the difference between memory and file channel?
4. How can Flume create small files?
5. What modern tools are often used instead of Flume?

## 15. Interview Speak

"Flume is a Hadoop-era ingestion tool for collecting and moving log/event data into HDFS or HBase. Its core model is source, channel, and sink. It is useful for log pipelines, but durability depends on the channel type and file rolling must be configured carefully to avoid small files."

## 16. Quick Recall

- One-line summary: Flume moves logs/events into Hadoop through source, channel, and sink.
- Three keywords: source, channel, sink.
- One trap: Forgetting channel durability.
- One memory trick: Flume is a log pipe into HDFS.
