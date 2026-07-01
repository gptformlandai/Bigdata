# Topic 259: Design LinkedIn Feed Analytics

## 1. Goal

Design a pipeline that analyzes feed impressions, clicks, reactions, comments, shares, follows, dwell time, and ranking performance.

## 2. Baby Intuition

A feed is a constant experiment.

The system needs to know:

```text
what content was shown,
what users did with it,
and whether the ranking system made good choices
```

## 3. Requirements

Clarify:

- Are we analyzing user engagement, creator analytics, ads, or ranking quality?
- Do we need per-user history or aggregate metrics?
- How fast should feedback reach ranking models?
- Do we need experiment analysis?
- What privacy rules apply to professional/social graph data?

## 4. Functional Requirements

- collect feed impression and engagement events
- preserve ranking context for each impression
- compute CTR, dwell time, reactions, comments, shares
- support A/B experiment analysis
- generate features for feed ranking
- detect spam/low-quality engagement
- provide dashboards by author, content type, region, experiment, and ranking model

## 5. Non-Functional Requirements

- high event throughput
- near-real-time ranking feedback
- accurate experiment metrics
- strong dedupe and ordering per impression
- privacy-aware user data handling
- replay for feature/model changes

## 6. Capacity Estimation

Example:

```text
200M daily active users
100 feed items shown/user/day
= 20B impression events/day

engagement events maybe 1-5B/day
raw volume roughly tens of TB/day
```

Impressions dominate volume because every scroll creates many shown-item events.

## 7. Events And APIs

Impression event:

```json
{
  "impression_id": "imp1",
  "user_id": "u1",
  "post_id": "p1",
  "rank_position": 4,
  "ranking_model": "feed_ranker_v12",
  "experiment_id": "exp42",
  "surface": "home_feed",
  "event_time": "2026-07-02T10:00:00Z"
}
```

Engagement event:

```json
{
  "event_type": "reaction",
  "impression_id": "imp1",
  "user_id": "u1",
  "post_id": "p1",
  "event_time": "2026-07-02T10:01:05Z"
}
```

## 8. Data Model

Silver impression table:

```text
feed_impressions(event_date, impression_id, user_id_hash, post_id, author_id, rank_position, model_version, experiment_id)
```

Silver engagement table:

```text
feed_engagements(event_date, impression_id, user_id_hash, post_id, event_type, dwell_ms)
```

Gold metrics:

```text
feed_daily_metrics(metric_date, model_version, experiment_id, content_type, impressions, clicks, reactions, ctr, avg_dwell_ms)
```

## 9. High-Level Architecture

```text
web/mobile feed
  -> event gateway
  -> Kafka
  -> stream joins impressions + engagement
  -> real-time ranking feedback/features

Kafka
  -> lakehouse
  -> batch experiment metrics
  -> warehouse/OLAP dashboards
  -> feature store for ranking
```

## 10. Data Flow

1. Feed service logs ranking context when items are shown.
2. Client logs impressions and engagement.
3. Gateway validates schema and identity.
4. Stream job joins engagement to impression context by impression_id.
5. Near-real-time features update ranking systems.
6. Raw and cleaned events are stored in lakehouse.
7. Batch jobs compute experiment and feed quality metrics.
8. Dashboards show engagement by model, segment, content type, and author.

## 11. Deep Dive Components

Ranking context is critical.

Without it, you cannot answer:

- which model ranked the item?
- what position was it shown at?
- was user in an experiment?
- what candidate source produced it?
- what features were used?

Store enough context to debug ranking without logging sensitive raw feature payloads unnecessarily.

## 12. Scaling And Partitioning

- Partition stream by impression_id for joins.
- Store lake data by event_date and event_type.
- Cluster by experiment_id, model_version, post_id.
- Use approximate distinct counts for unique viewers.
- Precompute experiment aggregates for common cuts.

## 13. Consistency And Correctness

- Engagement can arrive after impression.
- Use windows and late-event handling.
- Deduplicate by event_id or impression_id plus event_type.
- Experiment assignment must be stable.
- Official A/B metrics should be batch-reconciled.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| missing impression context | store engagement in quarantine and backfill if possible |
| duplicate client events | dedupe by event_id |
| late engagement | update affected windows/aggregates |
| bad experiment tag | validate against experiment registry |
| stream join state grows | TTL state by engagement window |

## 15. Monitoring, Cost, And Security

Monitor:

- impression rate
- engagement rate
- join success rate
- late engagement rate
- experiment coverage
- ranking feature freshness

Cost:

- avoid storing huge ranking payloads in every event
- store heavy context separately if needed
- compact and partition event tables

Security:

- hash user IDs
- restrict graph and user-level data
- audit access to feed behavior data
- enforce retention and deletion requirements

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| log detailed ranking context | strong debugging | high volume and privacy risk |
| real-time feedback | faster model adaptation | complexity and noise |
| batch experiment metrics | accurate decisions | slower learning |
| impression-level joins | precise CTR/dwell | stream state cost |

## 17. Interview-Ready Final Answer

"I would design LinkedIn feed analytics around impression-level tracking. The feed service and client emit impression and engagement events with ranking context such as model version, rank position, and experiment ID. Kafka carries the events to stream jobs that join engagements to impressions for real-time feedback and feature updates. Raw and cleaned events land in a lakehouse, where batch jobs compute accurate experiment, engagement, and feed quality metrics. The key concerns are preserving ranking context, deduping client events, handling late engagement, protecting user data, and separating fast feedback from official experiment analysis."

## 18. Quick Recall

- One-line summary: Feed analytics connects what was shown with what users did.
- Core tools: event gateway, Kafka, stream join, lakehouse, feature store, experiment warehouse.
- Main trap: forgetting ranking context on impressions.
- Memory trick: every feed item needs a report card.

