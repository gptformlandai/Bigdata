# Topic 281: Cost Optimization Questions

## 1. Goal

Prepare to discuss cloud and data platform cost optimization in interviews.

## 2. Baby Intuition

Cost optimization means getting the same business value with less waste.

It is not just "make everything cheaper." It is:

```text
spend money where freshness, correctness, or performance truly matter
and reduce waste everywhere else
```

## 3. Cost Areas In Big Data

- storage
- compute
- streaming infrastructure
- warehouse queries
- orchestration
- observability/logging
- data transfer
- over-retention
- duplicate datasets
- idle clusters

## 4. Storage Cost Questions

Optimize by:

- compression
- columnar formats
- partition pruning
- lifecycle policies
- cold storage tiers
- deleting expired snapshots
- removing unused duplicate data

Strong line:

```text
I separate hot, warm, and cold data instead of storing everything at the most expensive tier.
```

## 5. Compute Cost Questions

Optimize by:

- autoscaling
- right-sizing clusters
- using spot/preemptible for retryable jobs
- turning off idle clusters
- incremental processing
- avoiding unnecessary backfills
- optimizing slow jobs

## 6. Warehouse Query Cost Questions

Check:

- bytes scanned
- partition filter usage
- clustering/sort keys
- materialized views
- repeated dashboard queries
- expensive count distinct
- too many ad hoc users on large raw tables

Fix:

- certified aggregate tables
- query limits
- dashboard caches
- precomputed marts
- user education

## 7. Streaming Cost Questions

Streaming is valuable when freshness matters.

Optimize by:

- only streaming metrics/features that need freshness
- batching writes to sinks
- avoiding tiny micro-batches
- right-sizing partitions
- using efficient serialization/compression
- monitoring idle consumers

## 8. Observability Cost Questions

Logs and metrics can become expensive.

Control by:

- sampling noisy debug logs
- limiting metric cardinality
- using retention tiers
- avoiding user_id/request_id metric labels
- indexing only useful log fields

## 9. Cost Optimization Framework

Use:

1. Identify top cost drivers.
2. Separate necessary spend from waste.
3. Optimize largest waste first.
4. Measure savings and impact.
5. Add guardrails to prevent regression.

Guardrails:

- budgets
- alerts
- quotas
- chargeback/showback
- tagging
- query limits

## 10. Common Interview Prompts

1. Your warehouse bill doubled. What do you check?
2. Spark cluster is expensive. How do you reduce cost?
3. Logs are too expensive. What do you do?
4. Streaming job costs too much. How do you decide if streaming is needed?
5. How do you design cost visibility for many teams?

## 11. Sample Strong Answer

Question:

```text
BigQuery/Snowflake cost suddenly increased. What do you do?
```

Answer:

```text
I first identify which users, queries, warehouses, datasets, or dashboards caused the increase. Then I check bytes scanned, partition pruning, repeated schedules, materialized view opportunities, and whether a query started scanning raw tables. I would add query limits, improve clustering/partitioning, create aggregate marts for common dashboards, and set budget alerts or chargeback tags to prevent recurrence.
```

## 12. Quick Recall

- One-line summary: Cost optimization removes waste while preserving required freshness, correctness, and performance.
- Three keywords: measure, tier, right-size.
- One trap: cutting cost by breaking reliability.
- Memory trick: optimize value per dollar.

