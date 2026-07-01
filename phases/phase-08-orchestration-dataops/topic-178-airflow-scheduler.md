# Topic 178: Airflow Scheduler

## 1. Goal

Understand the Airflow scheduler and why it is central to running DAGs.

## 2. Baby Intuition

The scheduler is the person checking the calendar and task checklist.

It decides which tasks are ready to run now.

## 3. What It Is

- Simple definition: The Airflow scheduler creates and queues task runs.
- Technical definition: The Airflow scheduler parses DAGs, creates DAG runs according to schedules, evaluates task dependencies, and submits runnable task instances to the executor.
- Category: Airflow control-plane component.
- Related terms: DAG run, task instance, executor, metadata database, schedule interval, catchup.

## 4. Why It Exists

Someone must answer:

- Is this DAG due to run?
- Which tasks are ready?
- Which tasks are waiting?
- Which tasks failed?
- Which tasks should retry?
- Which tasks can be queued?

The scheduler is that decision-maker.

## 5. Where It Fits In A Data Platform

```text
DAG files
  -> scheduler parses and creates task instances
  -> executor receives runnable tasks
  -> workers run tasks
  -> metadata DB stores state
```

## 6. How It Works Step By Step

1. Scheduler scans DAG files.
2. It parses DAG definitions.
3. It checks schedules and creates DAG runs.
4. It evaluates task dependencies for each run.
5. It identifies task instances ready to execute.
6. It submits them to the executor.
7. It updates task/DAG state in the metadata database.
8. It repeats continuously.

## 7. How To Use It Practically

Scheduler-related settings/concepts:

| Concept | Meaning |
|---|---|
| schedule | when DAG runs |
| catchup | whether to create missed historical runs |
| max active runs | how many DAG runs can run at once |
| pools | limit shared resource usage |
| concurrency | how many tasks can run |
| metadata DB | source of state |

Practical advice:

- keep DAG parse code lightweight
- avoid network calls at DAG parse time
- monitor scheduler health
- tune concurrency carefully
- avoid creating thousands of unnecessary DAGs/tasks

## 8. Real-World Scenario

- Product/system: Hourly event processing.
- Problem: The hourly DAG must run every hour and retry failed tasks.
- How scheduler helps: It creates hourly DAG runs and queues ready task instances.
- What would go wrong if down: no new scheduled tasks start.

## 9. System Design Angle

Mention scheduler when:

- tasks are not starting
- DAG runs are missing
- catchup/backfill behavior matters
- scheduling latency matters
- metadata DB load matters

Key phrase:

```text
Scheduler decides readiness; executor runs the work.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| central scheduling logic | scheduler health is critical |
| dependency-aware execution | parse performance matters |
| supports catchup/backfills | can overwhelm executor if misconfigured |
| rich state tracking | metadata DB load can grow |

## 11. Failure Modes

- Failure: Scheduler process down.
- Symptom: no new task instances queued.
- Recovery: restart scheduler.
- Prevention: health checks and HA where supported.

- Failure: Slow DAG parsing.
- Symptom: delayed scheduling.
- Recovery: optimize DAG files.
- Prevention: no heavy logic at import time.

- Failure: Catchup explosion.
- Symptom: many historical runs start unexpectedly.
- Recovery: pause/limit runs.
- Prevention: configure catchup intentionally.

## 12. Common Mistakes

- Mistake: Putting database/API calls at DAG import time.
- Why it is wrong: scheduler repeatedly parses DAG files.
- Better approach: do external calls inside tasks, not DAG definition parsing.

- Mistake: Confusing scheduler with worker.
- Why it is wrong: scheduler queues tasks; workers execute them.
- Better approach: debug scheduling and execution separately.

## 13. Mini Example

```text
09:00 scheduler creates DAG run
09:01 extract task is ready
09:01 scheduler sends extract to executor
09:02 worker runs extract
```

## 14. Interview Questions

1. What does Airflow scheduler do?
2. Scheduler vs executor?
3. What is catchup?
4. Why should DAG parse code be lightweight?
5. What happens if scheduler is down?

## 15. Interview Speak

"The Airflow scheduler parses DAGs, creates DAG runs based on schedules, evaluates dependencies, and queues runnable task instances to the executor. It is control-plane logic, so scheduler health, parse performance, metadata DB health, and catchup settings are important."

## 16. Quick Recall

- One-line summary: The scheduler decides what is ready to run.
- Three keywords: parse, DAG run, queue.
- One trap: Heavy code at DAG import time.
- One memory trick: Calendar plus checklist.
