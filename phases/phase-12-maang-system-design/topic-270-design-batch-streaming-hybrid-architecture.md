# Topic 270: Design Batch + Streaming Hybrid Architecture

## 1. Goal

Design a hybrid architecture that combines streaming for fresh results and batch for accurate, complete, replayable results.

## 2. Baby Intuition

Hybrid architecture is like having a live scoreboard and an official scorebook.

The live scoreboard updates fast. The official scorebook is checked carefully and may correct the final numbers.

## 3. Requirements

Clarify:

- Which metrics need real-time freshness?
- Which metrics need official accuracy?
- How late can data arrive?
- Can users tolerate corrections?
- Is one processing path preferred or can we maintain two?

## 4. Functional Requirements

- ingest events once into a durable log/lake
- compute near-real-time aggregates
- store raw events for replay
- compute accurate batch aggregates
- reconcile stream and batch outputs
- serve both live and finalized views
- support corrections and backfills

## 5. Non-Functional Requirements

- low-latency live metrics
- accurate final results
- replayability
- idempotent writes
- clear metric versioning
- manageable operational complexity
- cost control

## 6. Capacity Estimation

Example:

```text
events: 2M/sec peak
live freshness target: under 1 minute
final accuracy target: daily finalized by 8 AM
retention: raw events for 1 year
```

The estimate tells you whether streaming, lake storage, and batch windows are sized reasonably.

## 7. Events And APIs

Event:

```json
{
  "event_id": "e1",
  "entity_id": "x1",
  "event_type": "purchase",
  "amount": 50,
  "event_time": "2026-07-02T10:00:00Z"
}
```

Serving API:

```text
GET /metrics/revenue?mode=live
GET /metrics/revenue?mode=finalized
```

## 8. Data Model

Raw:

```text
bronze_events(event_date, event_id, entity_id, event_type, payload, event_time)
```

Live:

```text
live_metric_windows(window_start, metric_name, dimensions, value, watermark_time)
```

Final:

```text
final_daily_metrics(metric_date, metric_name, dimensions, value, finalized_at)
```

## 9. High-Level Architecture

```text
events
  -> Kafka/Pub/Sub
  -> stream processor
  -> live serving store

events
  -> raw lakehouse
  -> batch processor
  -> finalized gold tables

live + final
  -> dashboard/API with freshness and finalization status
```

## 10. Data Flow

1. Producers emit events with event_id and event_time.
2. Events enter durable streaming log.
3. Stream processor computes live windows with watermarks.
4. Events also land in raw lakehouse.
5. Batch job recomputes complete daily results from raw data.
6. Reconciliation compares live and batch outputs.
7. Serving layer exposes live and finalized views.
8. Corrections/backfills update final tables and notify consumers if needed.

## 11. Deep Dive Components

Two common patterns:

| Pattern | Meaning |
|---|---|
| Lambda architecture | separate batch and speed layers |
| Kappa architecture | streaming-first with replay from log |

Hybrid design can be Lambda-like if separate batch and stream jobs exist.

Reducing duplicated logic:

- shared transformation library
- SQL definitions reused in batch and stream where possible
- metric registry
- tests comparing live vs batch outputs

## 12. Scaling And Partitioning

- Partition stream by aggregation key.
- Partition lake by event_date and event_type.
- Use incremental batch for daily/hourly recompute.
- Pre-aggregate live windows.
- Use compaction for raw and aggregate tables.
- Separate live serving compute from batch compute.

## 13. Consistency And Correctness

- Live results are fast but may be incomplete.
- Batch results are slower but final.
- Deduplicate by event_id in both paths.
- Watermarks define how long to wait for late events.
- Reconciliation catches stream bugs or missed data.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| stream job down | restore from checkpoint and replay log |
| batch job fails | keep previous final table and alert |
| live/final mismatch | investigate and recompute |
| late events | update live correction or include in batch final |
| bad code deploy | rollback and backfill from raw |

## 15. Monitoring, Cost, And Security

Monitor:

- live freshness
- stream lag
- batch completion SLA
- live vs final mismatch
- raw data completeness
- serving query latency

Cost:

- avoid duplicating expensive transforms unnecessarily
- choose which metrics truly need live path
- use batch for heavy historical recomputation
- tier old raw data

Security:

- apply same access policy to live and final stores
- protect raw event data
- audit metric access
- enforce retention and deletion workflows

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| hybrid architecture | fast plus accurate | more complexity |
| stream-only | simpler if replay works | harder historical correction sometimes |
| batch-only | cheaper and accurate | stale results |
| shared metric definitions | consistency | engineering discipline required |

## 17. Interview-Ready Final Answer

"I would use a hybrid design when the product needs both fresh live metrics and accurate finalized metrics. Events are written once to Kafka and the raw lakehouse. A stream processor computes live windowed aggregates into a serving store, while batch jobs recompute complete results from raw events into finalized gold tables. The API or dashboard exposes live and finalized modes with freshness/finalization status. I would dedupe by event_id, handle late data with watermarks, reconcile live and batch outputs, keep raw events replayable, and use shared metric definitions to reduce drift between paths."

## 18. Quick Recall

- One-line summary: Hybrid architecture gives live speed plus batch truth.
- Core tools: Kafka, stream processor, raw lakehouse, batch jobs, serving store, reconciliation.
- Main trap: two paths with different business logic.
- Memory trick: live scoreboard plus official scorebook.

