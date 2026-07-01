# Topic 260: Design Amazon Clickstream Pipeline

## 1. Goal

Design a pipeline that collects e-commerce browsing and shopping behavior for analytics, personalization, search, ads, and business reporting.

## 2. Baby Intuition

Clickstream is the trail of footsteps inside an online store.

It tells us:

```text
what users viewed,
what they searched,
what they added to cart,
what they bought,
and where they dropped off
```

## 3. Requirements

Clarify:

- Are we tracking web/app events, purchases, search, ads, or all?
- How real-time must personalization be?
- Do we need session-level funnels?
- Which events are business-critical?
- What privacy and consent rules apply?

## 4. Functional Requirements

- collect page view, product view, search, add-to-cart, checkout, purchase, ad click, and recommendation click events
- build user sessions and funnels
- compute product/category metrics
- feed personalization and recommendation models
- support search ranking and ad attribution
- provide business dashboards and experiment analysis

## 5. Non-Functional Requirements

- high throughput with traffic spikes
- low-latency personalization signals
- accurate purchase and attribution metrics
- replayable raw events
- dedupe and bot filtering
- privacy, consent, and retention controls

## 6. Capacity Estimation

Example:

```text
300M daily visitors
80 events/visitor/day
= 24B events/day

event size about 1 KB
= about 24 TB/day before compression
```

Peak traffic during sales can be several times normal traffic, so design for bursts.

## 7. Events And APIs

Product view:

```json
{
  "event_id": "e1",
  "user_id": "u1",
  "session_id": "s1",
  "event_type": "product_view",
  "product_id": "sku123",
  "category_id": "c10",
  "source": "search",
  "device": "mobile",
  "event_time": "2026-07-02T10:00:00Z"
}
```

Purchase event:

```json
{
  "event_id": "e2",
  "order_id": "o1",
  "user_id": "u1",
  "items": [{"product_id": "sku123", "qty": 1, "price": 49.99}],
  "event_time": "2026-07-02T10:05:00Z"
}
```

## 8. Data Model

Raw:

```text
raw_clickstream_events(event_date, event_time, event_id, user_id_hash, session_id, event_type, payload)
```

Silver:

```text
clean_clickstream_events(event_date, user_id_hash, session_id, product_id, event_type, source, device)
```

Gold:

```text
product_daily_metrics(metric_date, product_id, views, carts, purchases, conversion_rate)
```

Session funnel:

```text
shopping_sessions(session_id, user_id_hash, first_seen, last_seen, viewed_count, cart_count, purchased_flag)
```

## 9. High-Level Architecture

```text
web/mobile/storefront
  -> tracking SDK/event gateway
  -> Kafka/Kinesis
  -> stream features and personalization updates
  -> online feature store/cache

Kafka/Kinesis
  -> lakehouse raw and clean tables
  -> batch sessionization and funnels
  -> warehouse/OLAP dashboards
  -> ML training datasets
```

## 10. Data Flow

1. Client SDK sends event batches.
2. Gateway validates schema, consent, and source.
3. Events enter Kafka/Kinesis.
4. Stream jobs update recent user/product features.
5. Raw events land in the lakehouse.
6. Batch jobs clean bots, dedupe events, and build sessions.
7. Gold aggregates power dashboards.
8. ML pipelines train recommendations, search ranking, and ad models.

## 11. Deep Dive Components

Sessionization:

- group by user_id/cookie and inactivity timeout
- handle anonymous-to-logged-in identity stitching carefully
- avoid merging users incorrectly
- keep consent and privacy rules in mind

Attribution:

- purchase may happen after many views/clicks
- choose attribution model: last click, first click, multi-touch
- store source/campaign/recommendation context

## 12. Scaling And Partitioning

- Partition stream by user_id for sessionization.
- Partition lake by event_date and event_type.
- Cluster by product_id, category_id, campaign_id for analytics.
- Use autoscaling ingestion for sales events.
- Precompute product/category funnels.

## 13. Consistency And Correctness

- Purchases are more important than page views.
- Use stronger validation for order/purchase events.
- Deduplicate by event_id and order_id.
- Handle late purchase events in attribution windows.
- Batch-reconcile revenue with source-of-truth order database.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| client offline | local buffer and retry |
| traffic spike | autoscale gateway and partitions |
| duplicate purchase event | dedupe by order_id/event_id |
| bot traffic | detection and filtering |
| schema break | schema registry and DLQ |
| late conversion | update attribution windows |

## 15. Monitoring, Cost, And Security

Monitor:

- event rate by type
- gateway errors
- stream lag
- bot rate
- sessionization freshness
- purchase reconciliation mismatch

Cost:

- sample low-value debug events if needed
- keep purchase/order events complete
- partition, compact, and compress lake data
- aggregate common funnels

Security:

- enforce consent flags
- tokenize user identifiers
- restrict raw behavioral data
- audit access
- support deletion workflows

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| collect detailed clickstream | rich personalization | privacy and cost |
| real-time features | fast recommendations | streaming complexity |
| batch sessionization | accurate funnels | delayed dashboards |
| client-side tracking | broad visibility | duplicates/ad blockers/data quality issues |

## 17. Interview-Ready Final Answer

"I would build Amazon clickstream as a high-throughput event pipeline. Web and mobile SDKs send product views, searches, cart, checkout, and purchase events to an event gateway and Kafka/Kinesis. Streaming jobs update recent user and product features for personalization, while raw events land in a lakehouse. Batch jobs dedupe, remove bots, sessionize events, build funnels, and reconcile purchases with the order database. Gold tables power product dashboards, attribution, experiments, and ML training. I would pay special attention to traffic spikes, purchase correctness, consent, identity stitching, dedupe, bot filtering, and cost control."

## 18. Quick Recall

- One-line summary: Clickstream turns online shopping footsteps into analytics and ML signals.
- Core tools: SDK, event gateway, Kafka/Kinesis, stream features, lakehouse, warehouse.
- Main trap: treating purchase events with the same looseness as page views.
- Memory trick: online store footsteps.

