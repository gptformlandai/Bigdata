# Topic 249: Recommendation Data Pipelines

## 1. Goal

Understand data pipelines that power recommendation systems.

## 2. Baby Intuition

Recommendation pipelines learn from behavior.

They watch what users view, click, buy, like, skip, and search, then turn those signals into candidate items and ranking features.

## 3. What It Is

- Simple definition: Recommendation pipelines collect signals and prepare data for recommendation models.
- Technical definition: Recommendation data pipelines ingest user-item interactions, content/catalog metadata, context, and feedback signals to build training data, features, candidate sets, embeddings, and serving stores for recommender systems.
- Category: ML/product data pipeline.
- Related terms: clickstream, candidate generation, ranking, embeddings, feature store, feedback loop, negative sampling.

## 4. Why It Exists

Recommendations need fresh and historical signals:

- views
- clicks
- purchases
- watch time
- likes/dislikes
- skips
- search queries
- item metadata
- user context

Raw events must become training examples and serving features.

## 5. Where It Fits In A Data Platform

```text
user events + item catalog
  -> data lake/lakehouse
  -> feature/training pipelines
  -> candidate generation and ranking models
  -> online serving store/cache
  -> recommendation API
```

## 6. How It Works Step By Step

1. Collect user interaction events.
2. Validate and dedupe events.
3. Join with item/user/context metadata.
4. Build historical training datasets.
5. Compute offline features/embeddings.
6. Generate candidates.
7. Rank candidates using model features.
8. Serve recommendations online.
9. Log impressions/clicks/conversions for feedback.

## 7. How To Use It Practically

Important datasets:

| Dataset | Purpose |
|---|---|
| interactions | user-item behavior |
| item catalog | item metadata |
| user features | preferences/context |
| embeddings | vector representations |
| candidates | possible recommendations |
| labels | clicked/bought/watched outcome |
| impressions | what was shown |

Good practices:

- log impressions, not just clicks
- avoid data leakage
- account for position bias
- refresh popular/trending features
- monitor feedback loops

## 8. Real-World Scenario

- Product/system: Video recommendations.
- Problem: Recommend videos based on watch history, freshness, and popularity.
- How pipeline helps: events build user/item features, embeddings, candidates, and ranking training data.
- What would go wrong without impressions: model cannot know what users saw but ignored.

## 9. System Design Angle

Recommendation pipeline requirements:

- event volume
- freshness needs
- offline training frequency
- online serving latency
- cold start strategy
- feedback loop monitoring
- privacy controls

Common architecture:

```text
Kafka events -> lakehouse -> batch training/features
             -> stream features -> online store
             -> recommendation serving API
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| personalized experience | complex feedback loops |
| uses rich behavior data | privacy concerns |
| improves engagement | training-serving skew |
| supports ranking experiments | online serving complexity |

## 11. Failure Modes

- Failure: Missing impression logs.
- Symptom: biased training data.
- Recovery: add impression logging.
- Prevention: event design review.

- Failure: Stale catalog.
- Symptom: recommend unavailable items.
- Recovery: refresh catalog/index.
- Prevention: freshness monitoring.

- Failure: Feedback loop bias.
- Symptom: same popular items dominate.
- Recovery: exploration/diversity controls.
- Prevention: monitor recommendation diversity.

## 12. Common Mistakes

- Mistake: Training only on clicks.
- Why it is wrong: clicks alone miss what was shown and ignored.
- Better approach: log impressions and outcomes.

- Mistake: Ignoring cold start.
- Why it is wrong: new users/items have little history.
- Better approach: use content/popularity/context fallback.

## 13. Mini Example

```text
User watched item A and B
  -> update user embedding/features
  -> candidate generator finds similar items
  -> ranker scores candidates
  -> API returns top recommendations
```

## 14. Interview Questions

1. What data powers recommendations?
2. Why log impressions?
3. Candidate generation vs ranking?
4. How do online/offline features fit?
5. How do you handle cold start?

## 15. Interview Speak

"Recommendation data pipelines collect user-item interactions, impressions, outcomes, item metadata, and context. They produce training data, features, embeddings, candidate sets, and online serving data. I would design for freshness, cold start, privacy, feedback loops, and training-serving consistency."

## 16. Quick Recall

- One-line summary: Recommendation pipelines turn behavior into candidates, features, and ranking data.
- Three keywords: interactions, candidates, ranking.
- One trap: No impression logging.
- One memory trick: Learn from what users saw, clicked, and skipped.
