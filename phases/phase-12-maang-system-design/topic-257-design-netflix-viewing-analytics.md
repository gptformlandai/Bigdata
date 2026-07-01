# Topic 257: Design Netflix Viewing Analytics

## 1. Goal

Design a pipeline that tracks viewing behavior, streaming quality, content performance, and recommendation signals for a Netflix-style platform.

## 2. Baby Intuition

Netflix analytics answers:

```text
what did people watch,
how long did they watch,
where did playback fail,
and what should we recommend next?
```

It is not only business analytics. It also helps streaming quality and personalization.

## 3. Requirements

Clarify:

- Are we tracking viewing analytics, QoE analytics, recommendations, or finance/content reporting?
- How quickly should metrics update?
- Do we need household/account/device-level analysis?
- How long should watch history be retained?
- How strict are privacy controls?

## 4. Functional Requirements

- collect play, pause, resume, seek, stop, completion, buffering, error, and rating events
- compute title-level metrics like starts, completions, watch hours, drop-off points
- compute quality metrics like buffering ratio and playback error rate
- feed recommendation features
- support experimentation and A/B test analysis
- support content licensing and business reporting

## 5. Non-Functional Requirements

- very high ingestion throughput
- near-real-time quality monitoring
- accurate daily reporting
- user privacy and regional compliance
- replayable history for model training
- low-latency feature generation for recommendations

## 6. Capacity Estimation

Example:

```text
250M users
2 viewing sessions/user/day
200 telemetry events/session
= 100B telemetry events/day

event size about 0.5 KB to 1 KB
raw data about 50-100 TB/day before compression
```

Playback telemetry can be much higher than simple "video started" events because players report heartbeat and QoE details.

## 7. Events And APIs

Important events:

- playback_started
- playback_heartbeat
- playback_paused
- playback_completed
- buffering_started
- buffering_ended
- playback_error
- rating_submitted

Example:

```json
{
  "event_id": "e1",
  "profile_id": "p1",
  "title_id": "t1",
  "session_id": "s1",
  "event_type": "playback_heartbeat",
  "position_sec": 420,
  "bitrate_kbps": 3500,
  "buffer_ms": 0,
  "device_type": "tv",
  "country": "US",
  "event_time": "2026-07-02T10:00:00Z"
}
```

## 8. Data Model

Bronze:

```text
raw_playback_events(event_date, event_time, event_id, profile_id_hash, title_id, session_id, event_type, payload)
```

Silver:

```text
viewing_sessions(session_id, profile_id_hash, title_id, start_time, end_time, watch_seconds, completed, device_type, country)
```

Gold:

```text
title_daily_metrics(metric_date, title_id, country, starts, completed_views, watch_hours, avg_completion_rate)
```

Feature table:

```text
profile_title_features(profile_id_hash, title_id, last_watch_time, watch_seconds_30d, completed_flag)
```

## 9. High-Level Architecture

```text
player apps
  -> telemetry gateway
  -> Kafka/Pub/Sub
  -> real-time QoE stream processing
  -> operational dashboards/alerts

Kafka/Pub/Sub
  -> lakehouse raw events
  -> sessionization jobs
  -> gold content metrics
  -> recommendation features and experimentation tables
```

## 10. Data Flow

1. Player emits session and telemetry events.
2. Gateway validates event schema and rate limits bad clients.
3. Stream processor computes buffering/error metrics within minutes.
4. Raw events are stored in the lakehouse.
5. Batch job sessionizes events into viewing sessions.
6. Aggregates are produced by title, region, device, and experiment.
7. Feature pipelines update recommendation features.
8. Dashboards and ML systems consume gold data.

## 11. Deep Dive Components

Sessionization is the hard part.

Rules may include:

- group events by session_id if available
- infer session break after inactivity timeout
- handle app crash and resume
- handle multiple devices under same account
- remove bot/test/internal events

Quality analytics needs:

- buffering ratio
- startup delay
- error rate
- bitrate changes
- CDN/ISP/device dimensions

## 12. Scaling And Partitioning

- Partition Kafka by profile_id or session_id for sessionization.
- Partition lake by event_date and event_type.
- Cluster/query optimize by title_id, country, device_type.
- Store title-level aggregates in OLAP/warehouse.
- Use approximate distinct counts for unique viewers at large scale.

## 13. Consistency And Correctness

- QoE alerts can be near-real-time and approximate.
- Content reporting should be batch-reconciled.
- Deduplicate repeated telemetry by event_id.
- Late heartbeat events should update affected sessions.
- Keep raw events for replay when sessionization logic changes.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| mobile client offline | local buffer and retry |
| duplicate heartbeats | event_id/session dedupe |
| stream lag | alert on QoE freshness |
| bad player release | app_version-level anomaly alerts |
| incorrect sessionization | replay raw events into corrected silver table |

## 15. Monitoring, Cost, And Security

Monitor:

- telemetry volume by app version
- playback error rate
- buffering ratio
- stream lag
- sessionization freshness
- recommendation feature freshness

Cost:

- sample ultra-frequent telemetry if safe
- compress and partition raw events
- keep raw data in cheaper storage after hot period
- precompute common content dashboards

Security:

- hash profile/user identifiers
- protect viewing history as sensitive behavioral data
- restrict raw data access
- audit access for experimentation and BI

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| detailed heartbeat telemetry | strong QoE insight | high volume and cost |
| sessionized silver table | easier analytics | complex late-event correction |
| real-time QoE processing | fast outage detection | operational complexity |
| batch content reporting | accurate numbers | slower freshness |

## 17. Interview-Ready Final Answer

"I would separate Netflix analytics into playback telemetry ingestion, real-time QoE monitoring, lakehouse-based sessionization, and batch/ML serving. Player apps emit viewing and quality events to a telemetry gateway and Kafka. Stream processing computes buffering, startup delay, and error metrics for alerting, while raw events land in the lakehouse. Batch jobs build viewing sessions and title-level aggregates, and feature pipelines feed recommendations. The hardest parts are sessionization, duplicate/late events, telemetry volume, privacy, and separating near-real-time operational metrics from reconciled business metrics."

## 18. Quick Recall

- One-line summary: Netflix analytics tracks watch behavior plus playback quality.
- Core tools: telemetry gateway, Kafka, stream QoE, lakehouse, sessionization, feature store.
- Main trap: ignoring playback heartbeat volume and sessionization complexity.
- Memory trick: viewing analytics plus quality thermometer.

