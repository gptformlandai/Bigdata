# Topic 265: Design Recommendation Feature Pipeline

## 1. Goal

Design a pipeline that produces features for recommendation models using user behavior, item metadata, and real-time context.

## 2. Baby Intuition

Recommendations need memory.

The system must remember:

```text
what the user likes,
what items are popular,
what similar users did,
and what is happening right now
```

## 3. Requirements

Clarify:

- Are features for training, online serving, or both?
- What freshness is required?
- Are recommendations for videos, products, jobs, posts, or ads?
- Do we need real-time user behavior?
- How do we avoid data leakage in training?

## 4. Functional Requirements

- ingest user interaction events
- ingest item/content metadata
- compute user, item, and user-item features
- maintain offline historical features for training
- maintain online fresh features for serving
- support point-in-time correct training datasets
- monitor freshness, quality, and drift

## 5. Non-Functional Requirements

- low-latency online feature lookup
- high-throughput feature computation
- strong training-serving consistency
- replayable pipelines
- versioned feature definitions
- privacy-aware user history
- scalable storage for sparse features

## 6. Capacity Estimation

Example:

```text
1B users
100M items
50B interaction events/day

online serving may need:
user features under 10 ms
item features under 10 ms
```

Large recommendation systems often separate candidate generation features from ranking features.

## 7. Events And APIs

Interaction event:

```json
{
  "user_id": "u1",
  "item_id": "i1",
  "event_type": "click",
  "dwell_ms": 12000,
  "source": "home_feed",
  "event_time": "2026-07-02T10:00:00Z"
}
```

Feature serving API:

```text
GET /features?entity=user:u1&feature_set=ranking_v3
```

## 8. Data Model

Feature examples:

```text
user_features:
- categories_clicked_7d
- avg_dwell_30d
- purchases_90d

item_features:
- item_popularity_1h
- item_ctr_7d
- content_embedding

user_item_features:
- user_seen_item_before
- affinity_score
```

Offline store:

```text
feature_values(entity_id, feature_name, feature_value, feature_time)
```

Online store:

```text
entity_id -> latest feature vector
```

## 9. High-Level Architecture

```text
events + item metadata
  -> Kafka + lakehouse
  -> batch feature jobs
  -> offline feature store
  -> training datasets

events
  -> stream feature jobs
  -> online feature store
  -> recommendation serving/ranking
```

## 10. Data Flow

1. User events are ingested into Kafka and lakehouse.
2. Item metadata flows from catalog/content systems.
3. Batch jobs compute historical aggregates and embeddings.
4. Stream jobs compute fresh counters like clicks in last 10 minutes.
5. Offline feature store keeps historical feature values.
6. Online feature store keeps latest serving values.
7. Model training performs point-in-time joins.
8. Serving system fetches online features for ranking.

## 11. Deep Dive Components

Point-in-time correctness:

- training example at time T can only use features known at or before T
- prevents future data leakage

Training-serving consistency:

- same feature definition should be used offline and online when possible
- version feature logic

Feature freshness:

- define freshness SLA per feature
- not all features need real-time updates

## 12. Scaling And Partitioning

- Partition user features by user_id.
- Partition item features by item_id.
- Use stream state keyed by user_id/item_id.
- Store offline features partitioned by feature_date and feature_set.
- Cache hot item features.
- Precompute heavy embeddings offline.

## 13. Consistency And Correctness

- Online features may be eventually consistent.
- Training data must avoid future leakage.
- Feature definitions should be versioned.
- Backfills must not silently change model training without tracking version.
- Use freshness checks before model serving.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| online feature stale | fallback to default/popular recommendations |
| stream feature job down | alert on freshness and use batch features |
| bad feature definition | rollback feature version |
| training leakage | rebuild dataset point-in-time correctly |
| online store down | cache/defaults/degraded serving |

## 15. Monitoring, Cost, And Security

Monitor:

- feature freshness
- null/default rate
- feature distribution drift
- online lookup latency
- training-serving skew
- model quality metrics

Cost:

- compute only useful features
- expire unused features
- compact offline store
- cache hot online features

Security:

- protect user behavior features
- restrict sensitive features
- track lineage and owners
- support deletion/privacy workflows

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| real-time features | fresh personalization | streaming complexity |
| batch features | stable and cheaper | less fresh |
| many features | model signal richness | cost and overfitting risk |
| online feature store | low-latency serving | operational overhead |

## 17. Interview-Ready Final Answer

"I would build recommendation features with both offline and online paths. Raw interaction events and item metadata land in Kafka and the lakehouse. Batch jobs compute historical user/item features into an offline feature store for training, while streaming jobs update fresh counters in an online feature store for serving. Training datasets must use point-in-time joins to avoid leakage, and serving must use versioned feature definitions to reduce training-serving skew. I would monitor freshness, null rates, drift, lookup latency, and feature ownership, with fallback recommendations if online features are stale."

## 18. Quick Recall

- One-line summary: Recommendation feature pipelines turn behavior and metadata into reusable ML signals.
- Core tools: Kafka, lakehouse, batch jobs, stream jobs, offline/online feature store.
- Main trap: future data leakage in training.
- Memory trick: recommendation memory bank.

