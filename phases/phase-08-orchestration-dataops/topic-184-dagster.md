# Topic 184: Dagster

## 1. Goal

Understand Dagster as a modern data orchestrator focused on data assets, testing, and observability.

## 2. Baby Intuition

Airflow often asks, "What tasks should run?"

Dagster asks more directly, "What data assets are we producing, and are they healthy?"

## 3. What It Is

- Simple definition: Dagster is a data orchestrator that models pipelines around data assets.
- Technical definition: Dagster is an open-source data orchestration platform that defines software-defined assets, jobs, schedules, sensors, resources, and checks for building observable and testable data pipelines.
- Category: Data orchestrator / data platform framework.
- Related terms: asset, op, job, resource, sensor, partition, asset check, materialization.

## 4. Why It Exists

Many teams want orchestration that is closer to data engineering software practices:

- clear data asset lineage
- testable pipeline code
- typed/configured resources
- asset-level freshness and checks
- local development experience
- partitions and backfills as first-class concepts

Dagster exists to make data pipelines feel more like reliable software systems.

## 5. Where It Fits In A Data Platform

```text
sources
  -> Dagster assets/jobs orchestrate work
  -> Spark/dbt/Python/warehouse/lakehouse compute
  -> observable data assets
```

Dagster coordinates compute and tracks produced data assets.

## 6. How It Works Step By Step

1. Engineer defines assets or ops in Python.
2. Assets declare dependencies on other assets.
3. Resources define external systems like databases, warehouses, or object storage.
4. Jobs select assets/ops to run.
5. Schedules or sensors trigger runs.
6. Dagster executes steps and records materializations.
7. UI shows asset lineage, run history, logs, and checks.

## 7. How To Use It Practically

Asset-style idea:

```python
raw_orders -> cleaned_orders -> revenue_by_day
```

Common concepts:

| Concept | Meaning |
|---|---|
| asset | data object produced by code |
| materialization | successful production/update of asset |
| resource | external dependency like DB/S3 |
| partition | time/slice-based asset section |
| asset check | validation tied to asset |

## 8. Real-World Scenario

- Product/system: Analytics engineering platform.
- Problem: Team wants clear lineage from raw orders to revenue dashboard tables.
- How Dagster helps: assets represent datasets, dependencies are visible, and checks/freshness are tied to produced assets.
- What would go wrong without asset view: team sees task success but not which data products are healthy.

## 9. System Design Angle

Use Dagster when:

- data assets and lineage matter
- testing and local development matter
- asset freshness/checks are important
- team wants software-defined pipelines
- Python-centric orchestration is acceptable

Compare carefully with Airflow:

```text
Airflow is task/DAG-centric.
Dagster is asset-centric.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| asset-first model | smaller ecosystem than Airflow |
| strong local dev/testing | learning curve |
| lineage/freshness built in | migration from Airflow takes effort |
| good software abstractions | team must adopt asset mindset |

## 11. Failure Modes

- Failure: Asset dependencies modeled incorrectly.
- Symptom: downstream asset builds from stale/missing data.
- Recovery: fix dependency graph and rematerialize.
- Prevention: asset reviews and checks.

- Failure: Resource config wrong.
- Symptom: runs fail connecting to warehouse/storage.
- Recovery: fix environment/resource config.
- Prevention: typed config and secrets management.

- Failure: Too much custom framework code.
- Symptom: pipeline hard to maintain.
- Recovery: simplify assets/jobs.
- Prevention: follow platform patterns.

## 12. Common Mistakes

- Mistake: Treating Dagster exactly like Airflow.
- Why it is wrong: Dagster's strength is data assets, not only task order.
- Better approach: model key datasets as assets.

- Mistake: Ignoring asset checks.
- Why it is wrong: run success does not guarantee data correctness.
- Better approach: attach quality checks to important assets.

## 13. Mini Example

```text
Asset graph:
raw_orders
  -> cleaned_orders
  -> revenue_daily

Each asset can have freshness, checks, and materialization history.
```

## 14. Interview Questions

1. What is Dagster?
2. How is Dagster different from Airflow?
3. What is an asset?
4. What is a materialization?
5. Why are asset checks useful?

## 15. Interview Speak

"Dagster is a modern data orchestrator with an asset-first model. Instead of only thinking about tasks, it models the datasets produced by pipelines, their dependencies, materializations, partitions, resources, freshness, and checks. That makes it strong for observable and testable data platforms."

## 16. Quick Recall

- One-line summary: Dagster orchestrates and observes data assets.
- Three keywords: asset, materialization, checks.
- One trap: Using it only as task runner.
- One memory trick: Data products first, tasks second.
