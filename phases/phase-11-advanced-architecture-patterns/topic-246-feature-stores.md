# Topic 246: Feature Stores

## 1. Goal

Understand feature stores as systems for managing ML features consistently.

## 2. Baby Intuition

A feature store is like a shared pantry for ML signals.

Instead of every model team cooking the same feature differently, features are defined, stored, reused, and served consistently.

## 3. What It Is

- Simple definition: A feature store manages ML features for training and serving.
- Technical definition: A feature store is a platform for defining, computing, storing, discovering, versioning, and serving features for machine learning models in offline and online contexts.
- Category: ML data platform component.
- Related terms: feature, offline store, online store, point-in-time correctness, feature freshness, training-serving skew.

## 4. Why It Exists

ML models need features like:

- user purchases in last 7 days
- average transaction amount
- login frequency
- merchant risk score
- item popularity

Without a feature store:

- teams duplicate feature logic
- training and serving compute features differently
- features are hard to discover
- freshness is unclear
- point-in-time leakage happens

## 5. Where It Fits In A Data Platform

```text
raw events/tables
  -> feature pipelines
  -> offline feature store for training
  -> online feature store for low-latency serving
  -> ML models
```

## 6. How It Works Step By Step

1. Define feature and owner.
2. Build batch or streaming feature pipeline.
3. Store historical features offline.
4. Store latest/serving features online if needed.
5. Train models using point-in-time correct features.
6. Serve models using online features.
7. Monitor freshness, drift, and quality.

## 7. How To Use It Practically

Feature store pieces:

| Component | Purpose |
|---|---|
| feature registry | discover definitions |
| offline store | historical training data |
| online store | low-latency serving |
| transformation logic | compute features |
| metadata | owner, freshness, lineage |
| monitoring | quality/drift/freshness |

Good feature requirements:

- clear entity key
- timestamp/event time
- freshness SLA
- transformation definition
- training-serving consistency

## 8. Real-World Scenario

- Product/system: Fraud ML platform.
- Problem: Many models need user transaction counts and merchant risk features.
- How feature store helps: shared features are computed once, reused for training, and served online for real-time scoring.
- What would go wrong without it: each model computes features differently and gets inconsistent results.

## 9. System Design Angle

Use feature stores when:

- multiple ML teams reuse features
- online and offline consistency matters
- real-time serving needs low latency
- point-in-time correctness matters
- feature governance is needed

Avoid when:

- one simple offline model has few features
- no online serving is needed
- team is too early and overhead is not justified

## 10. Trade-offs

| Pros | Cons |
|---|---|
| reusable features | platform complexity |
| training-serving consistency | feature ownership needed |
| point-in-time support | storage and serving cost |
| governance/lineage | freshness monitoring required |

## 11. Failure Modes

- Failure: Training-serving skew.
- Symptom: model performs well offline but poorly online.
- Recovery: align feature logic.
- Prevention: shared feature definitions.

- Failure: Data leakage.
- Symptom: model uses future information in training.
- Recovery: rebuild training dataset.
- Prevention: point-in-time joins.

- Failure: Stale online features.
- Symptom: real-time model uses old signals.
- Recovery: fix feature pipeline.
- Prevention: freshness alerts.

## 12. Common Mistakes

- Mistake: Ignoring event time in training data.
- Why it is wrong: model may learn from future data.
- Better approach: point-in-time correct feature generation.

- Mistake: Building online store before needing online serving.
- Why it is wrong: unnecessary complexity.
- Better approach: start with offline features if batch ML is enough.

## 13. Mini Example

```text
entity: user_id
feature: purchases_last_7_days
offline: historical values for training
online: latest value for model API
freshness: under 5 minutes
```

## 14. Interview Questions

1. What is a feature store?
2. Offline vs online feature store?
3. What is training-serving skew?
4. What is point-in-time correctness?
5. When is a feature store overkill?

## 15. Interview Speak

"A feature store manages ML feature definitions, metadata, offline historical values, and online low-latency values. It helps reuse features, avoid training-serving skew, enforce point-in-time correctness, and monitor feature freshness and quality."

## 16. Quick Recall

- One-line summary: Feature stores manage ML features for training and serving.
- Three keywords: offline, online, point-in-time.
- One trap: Future data leakage.
- One memory trick: Shared pantry for ML signals.
