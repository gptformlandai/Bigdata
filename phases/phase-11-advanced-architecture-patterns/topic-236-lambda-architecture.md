# Topic 236: Lambda Architecture

## 1. Goal

Understand Lambda architecture as a pattern that combines batch and streaming systems.

## 2. Baby Intuition

Lambda architecture is like having two teams produce the same answer.

One team gives a quick estimate from live data. Another team later computes the accurate answer from all historical data.

## 3. What It Is

- Simple definition: Lambda architecture uses both batch and speed layers.
- Technical definition: Lambda architecture combines a batch layer for accurate historical recomputation, a speed layer for low-latency updates, and a serving layer that merges results for queries.
- Category: Hybrid batch + streaming architecture.
- Related terms: batch layer, speed layer, serving layer, recomputation, eventual correctness, data lake.

## 4. Why It Exists

Some systems need both:

- fast answers from recent events
- correct answers from complete historical data

Streaming can be fast but may have late events, duplicates, or approximations.

Batch can be accurate and replayable but slower.

Lambda architecture exists to get both freshness and correctness.

## 5. Where It Fits In A Data Platform

```text
events
  -> raw immutable storage
  -> batch layer computes full historical truth
  -> speed layer computes recent updates
  -> serving layer merges batch + speed views
```

## 6. How It Works Step By Step

1. All events are stored immutably in a raw data lake/log.
2. Batch layer periodically recomputes trusted views from all data.
3. Speed layer processes new events immediately.
4. Serving layer exposes queryable views.
5. Queries combine historical batch results with recent speed results.
6. When batch catches up, old speed-layer results can be replaced.

## 7. How To Use It Practically

Example stack:

| Layer | Possible Tools |
|---|---|
| raw storage | S3/GCS/ADLS/HDFS |
| speed layer | Kafka + Flink/Spark Streaming |
| batch layer | Spark/dbt/warehouse jobs |
| serving layer | Druid/Pinot/ClickHouse/warehouse/Redis |

Good fit:

- real-time dashboards that need later correction
- ad analytics
- fraud metrics
- operational monitoring with historical rebuilds

## 8. Real-World Scenario

- Product/system: Ad campaign analytics.
- Problem: Advertisers need clicks now, but final billable metrics must be corrected for duplicates and late events.
- How Lambda helps: speed layer shows near-real-time clicks; batch layer later recomputes accurate billable metrics.
- What would go wrong without it: either dashboards are stale or live metrics become final truth too early.

## 9. System Design Angle

Use Lambda architecture when:

- low latency and exact historical correctness both matter
- streaming results need reconciliation
- full replay/recompute is required
- late events and duplicates are common

Avoid when:

- one streaming system can provide correctness alone
- business can tolerate batch delay
- duplicate logic cost is too high

## 10. Trade-offs

| Pros | Cons |
|---|---|
| fresh and correct views | duplicate batch/stream logic |
| replayable raw history | operational complexity |
| handles late corrections | serving merge logic |
| strong auditability | higher cost |

## 11. Failure Modes

- Failure: Batch and stream logic diverge.
- Symptom: live and final metrics disagree unexpectedly.
- Recovery: compare and reconcile.
- Prevention: shared logic/tests where possible.

- Failure: Speed layer lag.
- Symptom: live dashboard stale.
- Recovery: scale/tune stream processor.
- Prevention: lag/freshness monitoring.

- Failure: Batch layer fails.
- Symptom: final correction never arrives.
- Recovery: rerun batch/backfill.
- Prevention: orchestration and data quality checks.

## 12. Common Mistakes

- Mistake: Building Lambda architecture by default.
- Why it is wrong: two code paths are expensive to maintain.
- Better approach: use it only when both freshness and recomputation are truly needed.

- Mistake: Letting live metrics become official financial truth.
- Why it is wrong: streaming data may be late or duplicated.
- Better approach: use batch reconciliation for final truth.

## 13. Mini Example

```text
click events
  -> Flink updates live campaign dashboard
  -> Spark nightly recomputes final campaign metrics
  -> serving layer shows live + reconciled values
```

## 14. Interview Questions

1. What is Lambda architecture?
2. What are batch, speed, and serving layers?
3. Why is Lambda architecture complex?
4. When would you choose it?
5. How do you handle metric disagreement?

## 15. Interview Speak

"Lambda architecture uses a speed layer for low-latency results and a batch layer for accurate replayable historical computation. I would use it when both freshness and final correctness matter, while being careful about duplicate logic, reconciliation, and operational cost."

## 16. Quick Recall

- One-line summary: Lambda architecture combines streaming freshness with batch correctness.
- Three keywords: batch, speed, serving.
- One trap: Duplicate logic drift.
- One memory trick: Fast estimate now, audited truth later.
