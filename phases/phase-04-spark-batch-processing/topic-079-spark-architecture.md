# Topic 079: Spark Architecture

## 1. Goal

Understand the main parts of Spark architecture and how a Spark application runs on a cluster.

## 2. Baby Intuition

Think of Spark like a construction project.

- Driver is the site manager.
- Executors are workers.
- Cluster manager gives workers and resources.
- Tasks are small pieces of work.
- Storage systems hold input/output materials.

## 3. What It Is

- Simple definition: Spark architecture describes how Spark coordinates work across driver, executors, and cluster resources.
- Technical definition: A Spark application consists of a driver process and executor processes running on a cluster, with resources allocated by a cluster manager and work broken into jobs, stages, and tasks.
- Category: Distributed compute architecture.
- Related terms: driver, executor, cluster manager, job, stage, task, partition.

## 4. Why It Exists

Spark must solve several problems:

- split large data into parallel work
- schedule tasks on many machines
- manage memory and CPU
- recover failed tasks
- coordinate data movement
- write final output reliably

One machine cannot do this for massive data, so Spark uses a cluster architecture.

## 5. Where It Fits In A Data Platform

```text
Storage -> Spark Driver/Executors -> Output Storage
                ^
          Cluster Manager
```

Spark architecture connects:

- code written by developer
- cluster resources
- distributed input data
- distributed output data

## 6. How It Works Step By Step

Application flow:

1. User submits Spark application.
2. Driver starts and runs the main program.
3. Driver creates SparkSession/SparkContext.
4. Driver contacts cluster manager.
5. Cluster manager launches executors.
6. Driver builds execution plan.
7. Driver sends tasks to executors.
8. Executors read data and process partitions.
9. Executors may shuffle data between each other.
10. Output is written to storage.

Architecture:

```text
Driver
  -> asks cluster manager for executors
  -> schedules tasks
  -> tracks progress

Executors
  -> run tasks
  -> store cached data
  -> report status
```

## 7. How To Use It Practically

Spark config examples:

```bash
--num-executors 8
--executor-cores 4
--executor-memory 8g
--driver-memory 4g
```

Useful UI concepts:

- Jobs tab
- Stages tab
- Tasks
- Storage tab
- SQL tab
- Executors tab

Production habit:

```text
Always inspect Spark UI when learning performance.
```

## 8. Real-World Scenario

- Product/system: Customer 360 ETL.
- Problem: Join orders, clicks, profiles, and support tickets.
- How architecture helps: Driver plans work; executors process partitions in parallel; cluster manager allocates resources.
- What would go wrong without it: One machine would not have enough CPU/memory/disk to process all datasets.

## 9. System Design Angle

Spark architecture affects:

- parallelism
- cost
- failure recovery
- memory pressure
- network shuffle
- job reliability

Design questions:

- how much data?
- how many partitions?
- how many executors?
- what memory per executor?
- what is the shuffle size?
- where is data stored?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| parallel compute | coordination overhead |
| task retry | driver/executor tuning |
| scalable jobs | shuffle network cost |
| rich APIs | debugging distributed failures |

## 11. Failure Modes

- Failure: Driver OOM.
- Symptom: whole app fails.
- Recovery: rerun with safer code/memory.
- Prevention: avoid collect and huge driver-side objects.

- Failure: Executor OOM.
- Symptom: tasks retry or executors lost.
- Recovery: tune partitions/memory.
- Prevention: avoid skew and large per-task data.

- Failure: Cluster manager cannot allocate resources.
- Symptom: application stuck waiting.
- Recovery: free resources or adjust configs.
- Prevention: queue/capacity planning.

## 12. Common Mistakes

- Mistake: Thinking executors decide the plan.
- Why it is wrong: driver plans and schedules; executors run tasks.
- Better approach: separate driver coordination from executor execution.

- Mistake: Giving one executor all memory/cores.
- Why it is wrong: can reduce parallelism and increase GC pressure.
- Better approach: size executors based on workload and cluster.

## 13. Mini Example

```text
1 driver
4 executors
4 cores per executor

Maximum concurrent tasks roughly = 16
```

Each task processes one partition at a time.

## 14. Interview Questions

1. Explain Spark architecture.
2. What does the driver do?
3. What does an executor do?
4. What is the role of cluster manager?
5. How does Spark recover from executor failure?

## 15. Interview Speak

"A Spark application has a driver and executors. The driver runs the main program, builds the plan, and schedules tasks. Executors run tasks on data partitions and store cached data. A cluster manager like YARN, Kubernetes, or Standalone allocates resources."

## 16. Quick Recall

- One-line summary: Driver plans; executors run; cluster manager allocates.
- Three keywords: driver, executor, task.
- One trap: Sending too much data to driver.
- One memory trick: Manager plans the work, workers do the work.
