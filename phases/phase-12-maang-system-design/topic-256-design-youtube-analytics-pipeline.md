# Topic 256: Design YouTube Analytics Pipeline

## 1. Goal

Design a pipeline that collects YouTube-style video events and produces analytics for creators, internal teams, recommendations, and business reporting.

## 2. Baby Intuition

Imagine every video interaction as a tiny receipt:

```text
user watched video X for 30 seconds
user liked video X
user searched for Y
user skipped ad Z
```

The system collects billions of receipts, cleans them, groups them, and turns them into dashboards and ML signals.

## 3. Requirements

Clarify first:

- Are we designing creator analytics, internal analytics, recommendations, or all?
- Is the dashboard real-time or delayed?
- Do we need exactly accurate numbers or approximate fast numbers?
- How long should raw events be retained?
- Do we need user-level privacy controls?

## 4. Functional Requirements

- collect playback, impression, click, like, comment, subscribe, search, and ad events
- validate and deduplicate events
- compute near-real-time counters like views per minute
- compute daily aggregates like watch time by video/channel/country/device
- store raw events for replay and ML
- serve dashboards for creators and internal teams
- provide features to recommendation and ranking systems

## 5. Non-Functional Requirements

- high write throughput
- low-latency hot metrics for trending videos
- accurate batch numbers for official reporting
- replayable data for backfills
- privacy and access control
- cost-efficient long-term storage
- reliable late-event handling

## 6. Capacity Estimation

Example interview estimate:

```text
500M daily active users
100 events/user/day
= 50B events/day

average event size = 1 KB
raw data = about 50 TB/day before compression
compressed lake storage = maybe 10-20 TB/day
```

Do not fight for exact numbers. Show that you can estimate order of magnitude and design for growth.

## 7. Events And APIs

Example playback event:

```json
{
  "event_id": "uuid",
  "event_type": "video_playback",
  "user_id": "u123",
  "video_id": "v456",
  "channel_id": "c789",
  "watch_ms": 30000,
  "device": "mobile",
  "country": "US",
  "event_time": "2026-07-02T10:00:00Z",
  "client_time": "2026-07-02T10:00:01Z"
}
```

Producer API:

```text
POST /events
body: analytics event batch
```

## 8. Data Model

Raw lake table:

```text
raw_video_events
- event_date
- event_time
- event_id
- user_id_hash
- video_id
- channel_id
- event_type
- watch_ms
- country
- device
- app_version
```

Gold aggregate:

```text
video_daily_metrics
- metric_date
- video_id
- channel_id
- country
- views
- unique_viewers
- watch_time_ms
- likes
- comments
```

## 9. High-Level Architecture

```text
clients
  -> event gateway
  -> Kafka/Pub/Sub
  -> stream processing for hot metrics
  -> OLAP store for real-time dashboards

Kafka/Pub/Sub
  -> raw object storage/lakehouse
  -> batch Spark/Flink jobs
  -> warehouse/lakehouse gold tables
  -> creator analytics, BI, ML features
```

## 10. Data Flow

1. Client batches events and sends them to the event gateway.
2. Gateway validates schema and adds server receive time.
3. Events are written to Kafka partitioned by video_id or user_id depending on use case.
4. Stream job deduplicates by event_id and computes minute-level metrics.
5. Raw events are stored in a bronze lake table.
6. Batch jobs build silver cleaned events.
7. Gold jobs build daily video/channel metrics.
8. Serving stores power dashboards, recommendations, and reporting.

## 11. Deep Dive Components

| Component | Design Choice |
|---|---|
| event gateway | validates, rate limits, authenticates app/device |
| stream processor | Flink/Spark Streaming for hot counters |
| raw lake | cheap replayable source of truth |
| lakehouse table | Iceberg/Delta/Hudi for schema evolution and corrections |
| OLAP store | Druid/Pinot/ClickHouse for dashboard queries |
| warehouse | BigQuery/Snowflake/Redshift for official analytics |

## 12. Scaling And Partitioning

- Kafka partitions by `video_id` for video-centric metrics.
- Use salting for extremely popular videos to avoid hot partitions.
- Lake partitions by event_date and maybe event_type.
- OLAP store partitions by time and distributes by video_id/channel_id.
- Batch jobs use incremental processing by event_date/hour.

Hot-video problem:

```text
one viral video can receive millions of events quickly
```

Mitigation:

- split key with salt
- aggregate locally before global aggregation
- use approximate counters for real-time views

## 13. Consistency And Correctness

- Real-time dashboard can be approximate.
- Official daily numbers should come from batch-reconciled gold tables.
- Deduplicate by event_id.
- Handle late events with watermarks and correction jobs.
- Keep raw events replayable for backfills.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| event gateway down | client retry and local buffering |
| Kafka lag | autoscale consumers and alert on lag |
| stream job failure | checkpoint restore |
| duplicate events | event_id dedupe |
| late events | watermark plus correction batch |
| bad schema | schema registry and dead letter queue |

## 15. Monitoring, Cost, And Security

Monitor:

- event ingestion rate
- Kafka lag
- stream checkpoint failures
- raw-to-gold freshness
- dashboard query latency
- duplicate rate
- late-event rate

Cost controls:

- compress raw events
- partition lake tables
- compact small files
- pre-aggregate hot dashboards
- tier old data to cheaper storage

Security:

- hash or tokenize user IDs
- restrict raw user-level data
- audit dashboard and table access
- enforce retention policies

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Lambda-style batch + stream | fast plus accurate | two paths to maintain |
| Kappa-style stream only | simpler path | replay and correction must be strong |
| OLAP serving store | fast dashboards | extra storage/cost |
| approximate real-time metrics | low latency | final numbers may change |

## 17. Interview-Ready Final Answer

"I would build an event-driven analytics platform. Clients send playback and interaction events to an event gateway, which validates and writes them to Kafka. A streaming layer computes hot metrics for trending and near-real-time dashboards, while raw events land in a lakehouse for replay. Batch jobs create cleaned silver tables and accurate daily gold aggregates. I would serve low-latency dashboards from an OLAP store and official reporting from the warehouse/lakehouse. The key design concerns are dedupe, late events, viral hot keys, replay, privacy, cost, and clear separation between approximate real-time metrics and reconciled official metrics."

## 18. Quick Recall

- One-line summary: YouTube analytics is high-volume event ingestion plus real-time and batch aggregates.
- Core tools: event gateway, Kafka, Flink/Spark, lakehouse, OLAP, warehouse.
- Main trap: treating real-time view counts as final exact numbers.
- Memory trick: tiny viewing receipts become creator dashboards and ML signals.

