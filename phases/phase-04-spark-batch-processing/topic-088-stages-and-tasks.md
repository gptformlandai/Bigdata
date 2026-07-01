# Topic 088: Stages And Tasks

## 1. Goal

Understand how Spark breaks a job into stages and tasks.

## 2. Baby Intuition

A Spark job is like building a house.

- Job: build the house.
- Stage: foundation, walls, roof.
- Task: each worker's specific piece of a stage.

## 3. What It Is

- Simple definition: Stages are groups of work; tasks are the smallest units run on partitions.
- Technical definition: Spark divides a job's DAG into stages at shuffle boundaries, and each stage contains tasks that operate on data partitions.
- Category: Spark execution unit.
- Related terms: job, stage, task, partition, shuffle, task retry.

## 4. Why It Exists

Spark needs to:

- parallelize work
- manage dependencies
- retry failed pieces
- schedule work efficiently
- track progress

Stages and tasks give Spark a manageable execution structure.

## 5. Where It Fits In A Data Platform

```text
Action -> Job -> Stages -> Tasks -> Executors
```

This hierarchy appears in Spark UI.

## 6. How It Works Step By Step

Example:

```python
df.filter("amount > 100").groupBy("customer_id").count()
```

Execution:

1. Action `count()` triggers a job.
2. Filter can run before shuffle.
3. GroupBy requires shuffle.
4. Spark creates stages separated by shuffle.
5. Each stage has tasks.
6. Each task processes one partition.

## 7. How To Use It Practically

In Spark UI:

- Jobs tab: actions triggered
- Stages tab: stage duration and shuffle
- Tasks: slow tasks, failed tasks, skew

Important metrics:

- task duration
- input size
- shuffle read/write
- spill memory/disk
- failed tasks
- scheduler delay

## 8. Real-World Scenario

- Product/system: Daily aggregation job.
- Problem: One stage takes 95 percent of runtime.
- How stages/tasks help: Spark UI shows slow stage and skewed tasks.
- What would go wrong without this model: debugging would be guesswork.

## 9. System Design Angle

Stages and tasks help explain:

- parallelism
- bottlenecks
- retries
- skew
- shuffle cost
- executor utilization

If a job has 10,000 partitions, it can create many tasks.

If a job has 10 partitions, it may underuse the cluster.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| fine-grained parallelism | scheduling overhead |
| task retry | too many tiny tasks hurt |
| progress visibility | tuning partition count needed |
| stage-level debugging | shuffle stages can dominate runtime |

## 11. Failure Modes

- Failure: One task much slower.
- Symptom: stage stuck near 99 percent.
- Recovery: investigate skew or bad node.
- Prevention: balance partition sizes.

- Failure: Too many tiny tasks.
- Symptom: scheduler overhead.
- Recovery: coalesce/repartition appropriately.
- Prevention: control file and partition counts.

- Failure: Task repeatedly fails.
- Symptom: job aborts after retry limit.
- Recovery: inspect logs and bad data.
- Prevention: data validation and robust logic.

## 12. Common Mistakes

- Mistake: Thinking one Spark job means one task.
- Why it is wrong: a job has stages and many tasks.
- Better approach: understand execution hierarchy.

- Mistake: Ignoring slowest tasks.
- Why it is wrong: stage completes when all tasks finish.
- Better approach: look for skew and stragglers.

## 13. Mini Example

```text
Stage has 100 partitions.
Spark creates 100 tasks.
Cluster runs 20 at a time.
```

## 14. Interview Questions

1. What is a stage?
2. What is a task?
3. What creates a stage boundary?
4. How does partition count relate to task count?
5. How do you debug a slow stage?

## 15. Interview Speak

"An action triggers a Spark job. Spark splits the DAG into stages at shuffle boundaries, and each stage contains tasks, usually one task per partition. Executors run tasks in parallel. Slow stages often indicate shuffle, skew, spills, or bad partitioning."

## 16. Quick Recall

- One-line summary: Job -> stages -> tasks.
- Three keywords: stage, task, partition.
- One trap: Ignoring straggler tasks.
- One memory trick: Job is project; tasks are individual assignments.
