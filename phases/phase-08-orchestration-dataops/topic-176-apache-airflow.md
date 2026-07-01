# Topic 176: Apache Airflow

## 1. Goal

Understand Apache Airflow as a workflow orchestrator for data pipelines.

## 2. Baby Intuition

Airflow is like a manager for data jobs.

It does not usually do the heavy data processing itself. It decides what should run, when it should run, in what order, and what should happen if something fails.

## 3. What It Is

- Simple definition: Apache Airflow schedules and orchestrates workflows made of tasks.
- Technical definition: Airflow is an open-source workflow orchestration platform where pipelines are defined as Python DAGs and executed according to schedules, dependencies, retries, and runtime state.
- Category: Data workflow orchestrator.
- Related terms: DAG, task, scheduler, executor, operator, sensor, backfill, retry, SLA.

## 4. Why It Exists

Data platforms have many jobs:

- extract from databases
- load files to S3/HDFS
- run Spark jobs
- transform warehouse tables
- validate data quality
- refresh dashboards
- notify teams

These jobs must run in the right order. Cron can start one script, but it becomes painful when workflows have dependencies, retries, logs, history, and visibility.

Airflow exists to manage that complexity.

## 5. Where It Fits In A Data Platform

```text
Sources
  -> Airflow orchestrates ingestion/transforms/tests
  -> Spark/dbt/warehouse/lakehouse jobs do the actual work
  -> outputs feed dashboards, ML, reporting, products
```

Airflow is the coordinator, not usually the compute engine.

## 6. How It Works Step By Step

1. Engineers write a DAG in Python.
2. DAG defines tasks and dependencies.
3. Scheduler reads DAG files and creates task instances for scheduled runs.
4. Executor sends task instances to workers.
5. Workers run operators, such as Python, Bash, Spark, Kubernetes, dbt, or warehouse jobs.
6. Metadata database stores task state.
7. UI shows success, failure, logs, duration, and history.
8. Failed tasks can retry or alert.

Core flow:

```text
DAG file -> scheduler -> executor -> worker -> metadata DB/UI
```

## 7. How To Use It Practically

Small conceptual DAG:

```python
extract_orders >> validate_orders >> transform_orders >> refresh_dashboard
```

Common operators:

- PythonOperator
- BashOperator
- SparkSubmitOperator
- KubernetesPodOperator
- ExternalTaskSensor
- SQL operators

Good DAG habits:

- keep tasks idempotent
- avoid heavy processing inside scheduler code
- use clear task names
- set retries and timeouts
- test locally where possible
- monitor failures and duration

## 8. Real-World Scenario

- Product/system: Daily sales analytics pipeline.
- Problem: Sales data must load, validate, transform, and publish before business dashboards open.
- How Airflow helps: It schedules tasks, enforces dependencies, retries transient failures, and shows pipeline status.
- What would go wrong without it: scripts run out of order, failures are invisible, and dashboards may show stale data.

## 9. System Design Angle

Mention Airflow when:

- workflows have dependencies
- batch pipelines must run on schedule
- retries/backfills matter
- data jobs need observability
- many systems must be coordinated

Clarify:

- schedule/frequency
- task dependencies
- retry policy
- compute engine
- idempotency
- monitoring/alerts
- backfill needs

## 10. Trade-offs

| Pros | Cons |
|---|---|
| mature ecosystem | scheduler/executor tuning needed |
| Python DAGs | dynamic DAG misuse can hurt |
| strong UI/history | not ideal for very low-latency event workflows |
| retries/backfills | workers/executors must be operated |
| many integrations | task idempotency is still your job |

## 11. Failure Modes

- Failure: Scheduler down.
- Symptom: new task instances are not scheduled.
- Recovery: restart scheduler.
- Prevention: HA/monitoring.

- Failure: Worker capacity too low.
- Symptom: queued tasks pile up.
- Recovery: scale workers.
- Prevention: capacity planning.

- Failure: Non-idempotent task retries.
- Symptom: duplicate records or side effects.
- Recovery: clean data and rerun carefully.
- Prevention: make tasks idempotent.

## 12. Common Mistakes

- Mistake: Doing huge data processing inside Airflow Python tasks.
- Why it is wrong: Airflow should orchestrate heavy compute, not become the compute cluster.
- Better approach: trigger Spark, dbt, warehouse, or Kubernetes jobs.

- Mistake: Using Airflow like real-time streaming.
- Why it is wrong: Airflow is strongest for scheduled/batch workflows.
- Better approach: use Kafka/Flink/streaming systems for low-latency streams.

## 13. Mini Example

```text
Airflow task:
start Spark job

Spark job:
process 10 TB data

Airflow watches state, retries, logs, and alerts.
```

## 14. Interview Questions

1. What is Airflow?
2. What is a DAG?
3. What does the scheduler do?
4. What does the executor do?
5. Why should tasks be idempotent?

## 15. Interview Speak

"Airflow is a workflow orchestrator for scheduled data pipelines. I use it to define DAGs, task dependencies, retries, backfills, and alerts. Airflow coordinates work, while heavy processing should run in engines like Spark, dbt, warehouses, or Kubernetes jobs."

## 16. Quick Recall

- One-line summary: Airflow coordinates data jobs in order and on schedule.
- Three keywords: DAG, scheduler, executor.
- One trap: Treating Airflow as the heavy compute engine.
- One memory trick: Airflow is the data job manager.
