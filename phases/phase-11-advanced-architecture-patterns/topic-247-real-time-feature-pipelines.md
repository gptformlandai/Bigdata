# Topic 247: Real-Time Feature Pipelines

## 1. Goal

Understand pipelines that compute ML features from live events.

## 2. Baby Intuition

Real-time feature pipelines keep ML model signals fresh.

If fraud risk depends on the last 5 minutes of activity, yesterday's batch feature is not enough.

## 3. What It Is

- Simple definition: Real-time feature pipelines compute and serve features from streaming data.
- Technical definition: A real-time feature pipeline ingests events, computes low-latency aggregations or transformations, and writes fresh feature values to an online feature store for model serving.
- Category: Streaming ML data pipeline.
- Related terms: stream processing, online feature store, freshness, window, feature TTL, fraud detection, recommendation.

## 4. Why It Exists

Some ML predictions need current behavior:

- recent failed logins
- transaction velocity
- live click intent
- current inventory
- active session behavior
- recent merchant risk

Batch features may be stale for these use cases.

## 5. Where It Fits In A Data Platform

```text
events
  -> Kafka/Kinesis/Pub/Sub/Event Hubs
  -> Flink/Spark Streaming/Dataflow
  -> online feature store
  -> model serving API
```

Offline store still keeps history for training.

## 6. How It Works Step By Step

1. Applications emit events.
2. Stream processor reads events.
3. Processor validates schemas.
4. Processor computes windows/aggregates.
5. Features are written to online store by entity key.
6. Model serving reads latest features.
7. Monitoring tracks lag, freshness, quality, and drift.

## 7. How To Use It Practically

Feature examples:

| Feature | Window |
|---|---|
| transactions_last_5_min | sliding window |
| failed_logins_last_10_min | tumbling/sliding |
| clicks_last_session | session window |
| average_cart_value_last_1_hour | rolling window |

Design decisions:

- entity key
- event time vs processing time
- late event handling
- TTL
- online store latency
- backfill/offline parity

## 8. Real-World Scenario

- Product/system: Card fraud detection.
- Problem: Model needs transaction velocity in last 5 minutes.
- How pipeline helps: stream processor updates user/card velocity features in online store before scoring.
- What would go wrong without it: model misses rapid fraud bursts.

## 9. System Design Angle

Use real-time feature pipelines when:

- prediction needs fresh signals
- model serving latency is low
- events arrive continuously
- feature windows are short

Be careful with:

- training-serving skew
- late events
- duplicate events
- online store hot keys
- feature freshness SLAs

## 10. Trade-offs

| Pros | Cons |
|---|---|
| fresh model signals | streaming complexity |
| better real-time decisions | online store cost |
| supports fraud/recommendations | late/duplicate handling |
| low-latency serving | monitoring required |

## 11. Failure Modes

- Failure: Feature pipeline lag.
- Symptom: model sees stale signals.
- Recovery: scale/tune stream processor.
- Prevention: freshness alerts.

- Failure: Duplicate events.
- Symptom: inflated counts.
- Recovery: dedupe/replay.
- Prevention: event IDs and idempotent state.

- Failure: Offline/online mismatch.
- Symptom: model training differs from serving.
- Recovery: align transformations.
- Prevention: shared feature definitions and tests.

## 12. Common Mistakes

- Mistake: Computing real-time features without offline history.
- Why it is wrong: model training needs historical feature values.
- Better approach: maintain offline store/backfill path.

- Mistake: Ignoring TTL.
- Why it is wrong: model may use very old "latest" feature.
- Better approach: expire or default stale features.

## 13. Mini Example

```text
transaction event
  -> Flink updates card_txn_count_5m
  -> Redis/online feature store
  -> fraud model reads feature
```

## 14. Interview Questions

1. What is a real-time feature pipeline?
2. Why do fraud models need fresh features?
3. How do you handle late events?
4. What is feature freshness?
5. How do offline and online stores stay consistent?

## 15. Interview Speak

"A real-time feature pipeline uses streaming events to compute low-latency features and write them to an online feature store. I would design around entity keys, windows, event time, duplicates, late events, TTLs, freshness monitoring, and offline/online consistency."

## 16. Quick Recall

- One-line summary: Real-time feature pipelines keep ML serving signals fresh.
- Three keywords: streaming, online store, freshness.
- One trap: No offline history for training.
- One memory trick: Model needs today's pulse, not yesterday's report.
