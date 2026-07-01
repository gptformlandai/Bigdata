# Phase 12: MAANG-Level System Design

Phase 12 turns the earlier concepts into full interview-style Big Data system designs.

The mental model is:

```text
clarify product goal
  -> collect events
  -> estimate scale
  -> choose ingestion, storage, processing, and serving
  -> design for correctness, latency, cost, security, and failure
  -> explain trade-offs clearly
```

This phase is not about memorizing one perfect architecture. It is about learning how to reason like a data platform engineer.

## Topics

| # | Topic | Status |
|---:|---|---|
| 256 | Design YouTube analytics pipeline | Complete |
| 257 | Design Netflix viewing analytics | Complete |
| 258 | Design Uber real-time location pipeline | Complete |
| 259 | Design LinkedIn feed analytics | Complete |
| 260 | Design Amazon clickstream pipeline | Complete |
| 261 | Design fraud detection system | Complete |
| 262 | Design real-time ad analytics | Complete |
| 263 | Design log aggregation system | Complete |
| 264 | Design metrics monitoring system | Complete |
| 265 | Design recommendation feature pipeline | Complete |
| 266 | Design data lake for an enterprise | Complete |
| 267 | Design data warehouse for finance reporting | Complete |
| 268 | Design CDC pipeline from MySQL to lakehouse | Complete |
| 269 | Design real-time dashboard system | Complete |
| 270 | Design batch + streaming hybrid architecture | Complete |

## Phase Goal

By the end of this phase, you should be able to:

- clarify requirements before drawing architecture
- estimate event volume and storage roughly
- choose Kafka/Kinesis/Pub/Sub style ingestion when needed
- choose lakehouse, warehouse, OLAP, search, metrics, and feature-store serving layers
- explain batch vs streaming decisions
- reason about partitioning, scaling, ordering, dedupe, and late data
- discuss reliability, cost, security, and monitoring like a senior engineer
- give crisp interview-ready final answers

## Reusable Interview Flow

Use this order for every design:

1. Clarify requirements.
2. Define functional and non-functional requirements.
3. Estimate scale.
4. Define events/APIs.
5. Choose data model.
6. Draw high-level architecture.
7. Explain data flow.
8. Deep dive ingestion, processing, storage, and serving.
9. Explain partitioning and scaling.
10. Explain consistency and failure handling.
11. Add monitoring, cost, and security.
12. Finish with trade-offs and alternatives.

## Examples

Run these small helpers after reading the related topics:

| Example | Related Topics | What It Shows |
|---|---|---|
| `examples/topic_256_event_volume_estimator.py` | 256, 260, 262 | rough event and storage estimation |
| `examples/topic_258_location_partitioning_demo.py` | 258 | geohash-like location partitioning intuition |
| `examples/topic_264_slo_burn_rate_demo.py` | 264, 269 | alerting based on error-budget burn |
| `examples/topic_268_cdc_merge_plan_demo.py` | 268 | merge planning for inserts, updates, and deletes |

## Suggested Study Flow

1. Read Topics 256-260 for user/product analytics systems.
2. Read Topics 261-265 for real-time risk, ads, logs, metrics, and ML feature systems.
3. Read Topics 266-270 for enterprise platform and hybrid architecture designs.
4. Practice each design aloud in 10 minutes.
5. Finish with `phase-12-review.md`.

