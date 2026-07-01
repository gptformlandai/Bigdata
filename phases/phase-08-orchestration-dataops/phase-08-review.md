# Phase 8 Review: Orchestration And DataOps

## 1. Phase Summary

Phase 8 explains how data pipelines become production systems.

The core idea:

```text
pipelines need order, schedules, retries, tests, contracts, monitoring, alerts, ownership, and incident response
```

If you remember only one sentence:

```text
DataOps is the discipline of making data pipelines reliable, testable, observable, and safely deployable.
```

## 2. Big Picture

```text
pipeline code
  -> CI/CD
  -> orchestrator
  -> compute systems
  -> data quality checks
  -> observability
  -> alerts
  -> incident response
```

The orchestrator coordinates work.

The compute engine processes data.

The DataOps layer makes the system reliable.

## 3. Airflow Core Concepts

| Concept | Meaning | Why It Matters |
|---|---|---|
| Airflow | workflow orchestrator | schedules and coordinates jobs |
| DAG | directed acyclic dependency graph | defines task order |
| scheduler | decides what is ready to run | creates DAG/task runs |
| executor | runs/dispatches tasks | controls execution environment |
| sensor | waits for external condition | handles file/table/task readiness |
| backfill | rerun history | repairs missing/wrong past data |
| retry | rerun transient failure | improves reliability |
| SLA | measurable promise | defines freshness/completion expectations |

## 4. Orchestrator Comparison

| Tool | Best Mental Model | Strong Fit | Watch Out |
|---|---|---|---|
| Airflow | task/DAG scheduler | mature scheduled batch workflows | not a heavy compute engine |
| Dagster | data asset orchestrator | lineage, asset checks, software-defined data assets | team must adopt asset thinking |
| Prefect | Pythonic flow orchestrator | flexible Python workflows and simple operations | needs deployment standards |
| dbt | SQL transformation framework | warehouse/lakehouse analytics models | not ingestion or full orchestration |

Quick memory:

```text
Airflow -> task order
Dagster -> data assets
Prefect -> Python flows
dbt -> SQL models
```

## 5. Production Pipeline Checklist

For every important pipeline, define:

- owner
- schedule or trigger
- upstream dependencies
- downstream consumers
- retry policy
- timeout
- SLA/freshness target
- data quality checks
- backfill strategy
- rollback strategy
- monitoring signals
- alert route
- runbook

## 6. DAG Design Rules

Good DAGs:

- express important dependencies clearly
- have idempotent tasks
- avoid hidden dependencies inside scripts
- keep parse-time code lightweight
- use retries and timeouts
- separate heavy compute from orchestration
- have clear ownership

Bad DAG smells:

- one task called `run_everything`
- API/database calls at import time
- no retry policy
- no timeouts
- no data quality checks
- everything in one giant DAG

## 7. Backfills

Backfills rerun historical partitions.

Use when:

- old data is wrong
- pipeline failed for previous dates
- business logic changed
- a new table needs history
- late data arrived

Backfill safety:

```text
idempotent writes
defined date range
source availability
resource limits
downstream recomputation
validation after rerun
```

## 8. Retries

Retries are good for:

- temporary network failures
- cloud API timeouts
- warehouse capacity issues
- transient worker problems

Retries are bad for:

- deterministic bad data
- invalid credentials
- broken SQL syntax
- non-idempotent writes

Strong line:

> Retry transient failures, not broken logic.

## 9. SLAs And Freshness

Task success is not enough.

Important data products need:

- freshness target
- completion deadline
- quality target
- owner
- alert policy
- business impact definition

Example:

```text
daily_revenue must be ready by 08:00 with quality checks passed
```

## 10. dbt Mental Model

dbt transforms data already inside a warehouse/lakehouse.

Flow:

```text
sources -> staging -> intermediate -> marts -> dashboards
```

dbt gives:

- modular SQL models
- dependency graph through `ref()`
- tests
- docs
- lineage
- materializations
- CI-friendly workflows

dbt is not mainly:

- an ingestion tool
- a streaming engine
- a full workflow orchestrator

## 11. CI/CD For Data

CI/CD should check:

- Python syntax/lint
- DAG import/parse
- dbt compile
- dbt tests
- SQL lint/syntax
- unit tests
- sample integration tests
- schema/data quality checks
- deployment config

Main goal:

```text
bad pipeline code should fail before production
```

## 12. Data Pipeline Testing

Test categories:

| Test | Example |
|---|---|
| unit | transformation function maps values correctly |
| schema | columns and types are expected |
| not null | primary keys are present |
| unique | ids are not duplicated |
| relationship | facts join to dimensions |
| range | amount >= 0 |
| freshness | table updated on time |
| regression | key metric did not unexpectedly drop |

Strong line:

> Pipeline success does not equal data correctness.

## 13. Data Contracts

Data contracts define producer promises.

Include:

- schema
- field meanings
- owner
- quality rules
- freshness
- compatibility policy
- PII/security classification
- change process

Contracts move quality closer to producers.

## 14. Observability

Data observability monitors:

- freshness
- volume
- schema changes
- quality
- lineage
- anomalies
- task duration
- query/job cost

Great Expectations is explicit rules.

Monte Carlo/Datafold-style tools add broader metadata, anomaly detection, lineage, impact analysis, and incident workflows.

## 15. Monitoring Vs Alerting

Monitoring:

```text
collect and display signals
```

Alerting:

```text
notify the right owner when action is needed
```

Good alerts are:

- actionable
- owned
- severity-based
- deduplicated
- rich with context
- linked to runbooks/logs

Bad alerts say only:

```text
task failed
```

## 16. Incident Response

Data incident flow:

```text
detect -> acknowledge -> assess impact -> mitigate -> recover -> validate -> communicate -> postmortem
```

Common mitigations:

- rollback deployment
- restore previous table version
- quarantine bad data
- pause downstream publishing
- rerun failed task
- backfill affected partitions
- communicate staleness to users

## 17. Common Interview Questions

1. What is Airflow?
2. What is a DAG?
3. Scheduler vs executor?
4. What are sensors?
5. What is a backfill?
6. Why is idempotency important?
7. What is an SLA for data?
8. Airflow vs Dagster vs Prefect?
9. What is dbt?
10. How do you test pipelines?
11. What are data contracts?
12. What is data observability?
13. Great Expectations use case?
14. How do you design useful alerts?
15. How do you respond to a data incident?

## 18. Strong System Design Answer

Question:

> Design a production data pipeline platform for daily and hourly analytics.

Strong answer:

"I would use an orchestrator like Airflow, Dagster, or Prefect to coordinate pipeline dependencies, schedules, retries, sensors, backfills, and SLAs. Heavy processing would run in Spark, dbt, warehouse SQL, or Kubernetes jobs rather than inside the orchestrator itself.

For reliability, every critical pipeline would have idempotent tasks, timeouts, retry policy, data quality checks, ownership, and a backfill strategy. Pipeline code would go through CI/CD with DAG import tests, dbt compile/tests, unit tests, and deployment gates.

For operations, I would monitor task state, duration, retries, freshness, volume, schema changes, quality checks, lag, and cost. Alerts would be routed by owner and severity with runbook links. For incidents, the response would include impact assessment, mitigation, rollback or backfill, validation, communication, and postmortem actions."

## 19. Hands-On Project

Build a mini DataOps pipeline locally:

1. Create a fake daily orders CSV.
2. Build a Python DAG dependency graph.
3. Add a task that validates required fields.
4. Add retry behavior for a flaky task.
5. Add a data contract check.
6. Add a freshness check based on timestamp.
7. Add alert severity routing.
8. Write a small incident runbook for a failed daily revenue table.

What this teaches:

- DAG order
- retries
- contracts
- quality checks
- alerts
- incident thinking

## 20. Quick Revision Cards

| Prompt | Answer |
|---|---|
| Airflow? | task/DAG workflow orchestrator |
| DAG? | directed acyclic task dependency graph |
| Scheduler? | decides ready tasks and creates runs |
| Executor? | runs or dispatches tasks |
| Sensor? | waits for external condition |
| Backfill? | rerun historical data |
| Retry? | rerun transient failure safely |
| SLA? | measurable data reliability promise |
| Dagster? | asset-first orchestrator |
| Prefect? | Pythonic flow orchestrator |
| dbt? | tested version-controlled SQL transformations |
| Data contract? | producer-consumer data promise |
| Observability? | data health monitoring |
| Great Expectations? | explicit data validation rules |
| Alerting? | actionable notification to owner |
| Incident response? | detect, mitigate, recover, learn |
