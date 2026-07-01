# Topic 275: Airflow Interview Questions

## 1. Goal

Prepare Airflow answers around DAGs, scheduling, retries, backfills, sensors, executors, and pipeline reliability.

## 2. Baby Intuition

Airflow is a workflow conductor.

It does not process Big Data itself. It schedules and coordinates jobs that process data elsewhere.

## 3. Must-Know Airflow Concepts

- DAG
- task
- operator
- scheduler
- executor
- worker
- sensor
- retry
- backfill
- catchup
- SLA
- XCom
- connection
- variable

## 4. Common Questions And Strong Answers

| Question | Strong Answer |
|---|---|
| What is Airflow? | orchestration tool for scheduling and monitoring workflows |
| What is a DAG? | directed acyclic graph of tasks and dependencies |
| Scheduler vs executor? | scheduler decides what should run; executor runs/dispatches tasks |
| What is backfill? | running pipeline for historical dates |
| What are sensors? | tasks that wait for external conditions |

## 5. DAG Design Questions

Good DAG design:

- tasks are idempotent
- tasks have clear boundaries
- retries are safe
- dependencies are explicit
- heavy compute runs outside Airflow
- each task logs useful context

Avoid:

- one giant task
- too many tiny tasks without reason
- non-idempotent writes
- storing large data in XCom
- dynamic DAGs that change unpredictably

## 6. Scheduling Questions

Important terms:

- schedule interval
- data interval
- execution date/logical date
- catchup
- start_date

Strong line:

```text
Airflow schedules data intervals, so a daily DAG usually processes the previous completed day.
```

## 7. Retry And Backfill Questions

Retries:

- handle transient failures
- require idempotent tasks
- should use reasonable delay/backoff

Backfills:

- rerun historical partitions
- require partitioned/idempotent writes
- should avoid overwhelming source/warehouse

## 8. Sensors And Dependencies

Sensors wait for:

- file arrival
- table partition availability
- external task completion
- API condition

Better practices:

- use deferrable sensors when possible
- avoid long-running worker-blocking sensors
- set timeouts
- alert when upstream data is late

## 9. Failure Questions

Common production issues:

- task failure
- DAG not scheduled
- stuck sensor
- worker unavailable
- source data late
- backfill overload
- wrong dependency

Debug flow:

```text
check DAG schedule
check task logs
check upstream dependencies
check worker/executor
check source freshness
check recent code/config changes
```

## 10. Airflow And Data Quality

Airflow should orchestrate checks:

- source arrived
- row count expected
- schema valid
- null/duplicate checks
- freshness check
- publish gate

Do not publish gold data if critical checks fail.

## 11. Practical Interview Questions

1. What makes a DAG reliable?
2. How do retries interact with idempotency?
3. How do you backfill safely?
4. What is a sensor and what can go wrong?
5. Why should heavy compute not run inside Airflow workers?
6. How do you handle late source data?
7. How do you monitor Airflow pipelines?

## 12. Sample Strong Answer

Question:

```text
Your Airflow DAG failed overnight. What do you do?
```

Answer:

```text
I first check which task failed and whether downstream data was published. Then I inspect task logs, upstream data availability, recent code/config changes, and worker/executor health. If it is transient and the task is idempotent, I retry. If source data is late, I delay publish and notify consumers. After recovery, I add prevention such as better freshness checks, retries, timeout, or alerting.
```

## 13. Quick Recall

- One-line summary: Airflow orchestrates data workflows; it is not the compute engine.
- Three keywords: DAG, scheduler, idempotency.
- One trap: putting heavy Spark-like computation inside Airflow tasks.
- Memory trick: conductor, not orchestra.

