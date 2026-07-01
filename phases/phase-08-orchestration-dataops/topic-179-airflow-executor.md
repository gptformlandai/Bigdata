# Topic 179: Airflow Executor

## 1. Goal

Understand Airflow executors and how they control where tasks actually run.

## 2. Baby Intuition

The scheduler says, "This task is ready."

The executor says, "Here is where and how we will run it."

## 3. What It Is

- Simple definition: An Airflow executor runs or dispatches scheduled tasks.
- Technical definition: An Airflow executor is the component that takes queued task instances from the scheduler and executes them locally, on workers, or through external systems depending on executor type.
- Category: Airflow execution component.
- Related terms: LocalExecutor, CeleryExecutor, KubernetesExecutor, worker, queue, task instance.

## 4. Why It Exists

Airflow needs flexible execution:

- small local development
- medium shared workers
- large distributed clusters
- isolated Kubernetes pods
- different queues for different workloads

The executor lets Airflow separate scheduling from task execution.

## 5. Where It Fits In A Data Platform

```text
scheduler
  -> executor
  -> local process / Celery worker / Kubernetes pod / other runtime
  -> task logs and state
```

## 6. How It Works Step By Step

1. Scheduler marks task instance ready.
2. Scheduler sends it to executor.
3. Executor places task in the chosen runtime.
4. Worker/process/pod runs task code.
5. Task reports success/failure.
6. State is stored in metadata DB.
7. Scheduler uses state to unblock downstream tasks.

## 7. How To Use It Practically

Common executors:

| Executor | Simple Meaning | Fit |
|---|---|---|
| SequentialExecutor | one task at a time | local/testing only |
| LocalExecutor | parallel tasks on one machine | small deployments |
| CeleryExecutor | distributed workers via queue | scalable classic Airflow |
| KubernetesExecutor | one pod per task | isolated cloud-native tasks |

Practical design:

- use worker queues for workload separation
- tune parallelism and concurrency
- avoid overloading shared databases/APIs
- choose Kubernetes for strong isolation when needed

## 8. Real-World Scenario

- Product/system: Enterprise Airflow deployment.
- Problem: Some tasks are lightweight SQL checks; others launch heavy Spark jobs.
- How executor helps: route tasks through distributed workers or isolated pods while scheduler manages dependencies.
- What would go wrong without capacity planning: tasks queue for hours or overload workers.

## 9. System Design Angle

Discuss executor choice based on:

- task volume
- isolation needs
- cloud/Kubernetes availability
- operational skill
- latency requirements
- cost
- workload types

Key phrase:

```text
Executor choice affects scalability, isolation, and operational complexity.
```

## 10. Trade-offs

| Executor Style | Pros | Cons |
|---|---|---|
| local | simple | limited scale/isolation |
| Celery | scalable workers | queue/broker operations |
| Kubernetes | task isolation | pod startup and cluster complexity |
| sequential | easy dev | not production scale |

## 11. Failure Modes

- Failure: Worker down.
- Symptom: queued/running tasks stuck or fail.
- Recovery: restart/replace worker.
- Prevention: worker health monitoring.

- Failure: Queue backlog.
- Symptom: tasks wait long before running.
- Recovery: scale workers/increase concurrency.
- Prevention: capacity planning.

- Failure: Kubernetes pod startup slow.
- Symptom: high task latency.
- Recovery: optimize images/resources.
- Prevention: right executor for workload.

## 12. Common Mistakes

- Mistake: Scaling scheduler when executor capacity is the bottleneck.
- Why it is wrong: tasks may be queued because workers are full.
- Better approach: check scheduler, executor queue, and worker metrics separately.

- Mistake: Using one worker pool for all workloads.
- Why it is wrong: heavy jobs can starve small checks.
- Better approach: separate queues/pools by workload.

## 13. Mini Example

```text
Scheduler:
task validate_orders is ready

Executor:
send validate_orders to worker queue

Worker:
run task and report success
```

## 14. Interview Questions

1. What is an Airflow executor?
2. Scheduler vs executor?
3. LocalExecutor vs CeleryExecutor?
4. KubernetesExecutor trade-offs?
5. How do you debug queued tasks?

## 15. Interview Speak

"The scheduler decides which tasks are ready, and the executor decides how those tasks are run. Executor choice affects scale and isolation: LocalExecutor is simple, CeleryExecutor uses distributed workers, and KubernetesExecutor can run isolated pods per task."

## 16. Quick Recall

- One-line summary: Executor runs or dispatches Airflow tasks.
- Three keywords: worker, queue, runtime.
- One trap: Confusing scheduling delay with worker capacity.
- One memory trick: Scheduler assigns; executor dispatches.
