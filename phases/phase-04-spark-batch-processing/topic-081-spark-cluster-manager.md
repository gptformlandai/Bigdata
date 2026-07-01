# Topic 081: Spark Cluster Manager

## 1. Goal

Understand what a Spark cluster manager does and how Spark gets resources to run jobs.

## 2. Baby Intuition

Spark needs workers, CPU, and memory.

The cluster manager is the person who assigns seats in a classroom:

```text
this Spark job gets these machines, this much memory, and this many cores
```

## 3. What It Is

- Simple definition: A cluster manager gives Spark resources.
- Technical definition: A Spark cluster manager allocates CPU and memory resources for Spark drivers and executors across a cluster.
- Category: Resource management.
- Related terms: YARN, Kubernetes, Spark Standalone, Mesos, executor allocation, queue.

## 4. Why It Exists

Multiple applications may share the same cluster.

Spark needs something to decide:

- where executors run
- how much memory each gets
- how many cores are assigned
- which job waits
- what happens when nodes fail

Spark itself is the compute engine. The cluster manager provides resources.

## 5. Where It Fits In A Data Platform

```text
spark-submit -> Cluster Manager -> Driver/Executors -> Data Processing
```

Common cluster managers:

- YARN
- Kubernetes
- Spark Standalone
- older: Mesos

Cloud platforms may hide this behind managed services.

## 6. How It Works Step By Step

YARN example:

1. User runs `spark-submit --master yarn`.
2. YARN receives application request.
3. Driver starts in client or cluster mode.
4. Spark requests executors.
5. YARN allocates containers.
6. Executors start inside containers.
7. Spark runs tasks.
8. Resources are released after completion.

Kubernetes example:

1. Spark creates driver pod.
2. Driver creates executor pods.
3. Kubernetes schedules pods on nodes.
4. Executors run tasks.
5. Pods terminate when job completes.

## 7. How To Use It Practically

Examples:

```bash
spark-submit --master local[*] job.py
spark-submit --master yarn --deploy-mode cluster job.py
spark-submit --master k8s://https://api-server job.py
spark-submit --master spark://host:7077 job.py
```

Deploy modes:

- client mode: driver runs where submit command runs
- cluster mode: driver runs inside the cluster

Production preference often:

```text
cluster mode for scheduled production jobs
```

## 8. Real-World Scenario

- Product/system: Shared data platform.
- Problem: Many Spark jobs run from different teams.
- How cluster manager helps: Allocates resources, enforces queues/limits, and launches executors.
- What would go wrong without it: Jobs would fight for resources manually and cluster utilization would be chaotic.

## 9. System Design Angle

Cluster manager affects:

- job startup time
- resource isolation
- autoscaling
- cost
- failure recovery
- deployment model

Questions:

- Is Spark running on YARN, Kubernetes, or managed platform?
- Are jobs batch or long-running?
- Are there team queues?
- Is dynamic allocation enabled?
- How is cost controlled?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| shared resource allocation | configuration complexity |
| isolation between jobs | queue wait time |
| easier executor management | platform-specific debugging |
| autoscaling options | startup overhead |

## 11. Failure Modes

- Failure: No resources available.
- Symptom: job stuck waiting.
- Recovery: wait, reduce resource request, free cluster capacity.
- Prevention: queue limits and capacity planning.

- Failure: Driver in client mode disconnects.
- Symptom: app may fail if client machine dies.
- Recovery: rerun in cluster mode.
- Prevention: use cluster mode for production.

- Failure: Executor allocation too small.
- Symptom: slow job.
- Recovery: tune executors/cores/partitions.
- Prevention: baseline workload sizing.

## 12. Common Mistakes

- Mistake: Confusing Spark with cluster manager.
- Why it is wrong: Spark runs computation; cluster manager allocates resources.
- Better approach: separate compute engine from resource manager.

- Mistake: Running production scheduled jobs in fragile client mode.
- Why it is wrong: driver depends on submit machine.
- Better approach: use cluster mode when appropriate.

## 13. Mini Example

```text
Spark job requests:
  5 executors
  4 cores each
  8 GB memory each

Cluster manager decides:
  which nodes run those executors
```

## 14. Interview Questions

1. What does Spark cluster manager do?
2. What cluster managers can Spark run on?
3. Client mode vs cluster mode?
4. What happens if resources are unavailable?
5. How does Kubernetes run Spark executors?

## 15. Interview Speak

"Spark uses a cluster manager to allocate resources for the driver and executors. The cluster manager could be YARN, Kubernetes, Standalone, or a managed service. Spark handles execution logic, while the cluster manager handles CPU/memory allocation and placement."

## 16. Quick Recall

- One-line summary: Cluster manager gives Spark CPU and memory.
- Three keywords: YARN, Kubernetes, executors.
- One trap: Confusing Spark compute with resource allocation.
- One memory trick: Spark asks; cluster manager assigns.
