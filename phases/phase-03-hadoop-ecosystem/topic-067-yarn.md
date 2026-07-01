# Topic 067: YARN

## 1. Goal

Understand YARN as Hadoop's cluster resource manager: the system that decides how CPU and memory are allocated to jobs.

## 2. Baby Intuition

Imagine a shared classroom with many students asking for desks.

YARN is the coordinator that says:

- who gets a desk
- how many desks they get
- when they must wait
- when a desk is free again

In a Hadoop cluster, desks are CPU and memory.

## 3. What It Is

- Simple definition: YARN manages cluster resources for Hadoop jobs.
- Technical definition: Yet Another Resource Negotiator is Hadoop's resource management layer that schedules applications and allocates containers across cluster nodes.
- Category: Cluster resource manager.
- Related terms: ResourceManager, NodeManager, ApplicationMaster, container, queue, scheduler.

## 4. Why It Exists

Early Hadoop tightly coupled MapReduce with cluster resource management.

That was limiting because the cluster should be able to run more than MapReduce:

- MapReduce
- Spark
- Tez
- Hive queries
- custom applications

YARN separated:

```text
resource management from processing framework
```

That allowed Hadoop clusters to become shared compute platforms.

## 5. Where It Fits In A Data Platform

```text
Users/Jobs -> YARN -> Cluster CPU/Memory -> MapReduce/Spark/Hive/Tez
```

YARN sits under processing engines.

It does not store data. HDFS stores data.

YARN decides where and how applications run.

## 6. How It Works Step By Step

Main components:

- ResourceManager: global scheduler and resource authority.
- NodeManager: runs on each worker node and manages local resources.
- ApplicationMaster: manages one application's execution.
- Container: allocated CPU/memory unit.

Job flow:

1. User submits application.
2. ResourceManager accepts it.
3. ResourceManager allocates a container for ApplicationMaster.
4. ApplicationMaster starts.
5. ApplicationMaster requests containers for tasks.
6. NodeManagers launch containers.
7. Tasks run.
8. ApplicationMaster monitors progress.
9. Resources are released when job completes.

## 7. How To Use It Practically

Useful commands:

```bash
yarn application -list
yarn application -status <application_id>
yarn logs -applicationId <application_id>
yarn application -kill <application_id>
```

Common tuning ideas:

- executor/container memory
- number of containers
- queue capacity
- CPU cores
- scheduling policy

Production mental model:

```text
If jobs are waiting, ask:
Do we lack memory?
Do we lack cores?
Is queue capacity full?
Is one user consuming the cluster?
```

## 8. Real-World Scenario

- Product/system: Shared enterprise Hadoop cluster.
- Problem: Finance, marketing, and risk teams all submit large jobs.
- How YARN helps: Allocates cluster resources fairly using queues and scheduling.
- What would go wrong without it: One team could consume all resources and starve others.

## 9. System Design Angle

YARN matters when designing shared Hadoop clusters.

Questions:

- How many teams share the cluster?
- Are workloads batch, interactive, or streaming?
- Do some jobs need priority?
- How do we prevent one job from starving others?
- How do we monitor resource usage?

YARN affects:

- throughput
- job wait time
- cluster utilization
- fairness
- cost

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| shared cluster resource management | scheduler complexity |
| supports multiple engines | tuning overhead |
| queue-based isolation | jobs may wait |
| better utilization | noisy-neighbor issues |

## 11. Failure Modes

- Failure: NodeManager fails.
- Symptom: containers on that node fail.
- Recovery: ApplicationMaster requests replacement containers.
- Prevention: monitoring and node health checks.

- Failure: ApplicationMaster fails.
- Symptom: application attempt fails.
- Recovery: YARN can retry application attempt.
- Prevention: correct retry config and logs.

- Failure: ResourceManager unavailable.
- Symptom: new applications cannot be scheduled.
- Recovery: ResourceManager HA failover.
- Prevention: HA setup.

## 12. Common Mistakes

- Mistake: Confusing YARN with HDFS.
- Why it is wrong: HDFS stores data; YARN manages compute resources.
- Better approach: Storage layer vs resource manager.

- Mistake: Giving every job huge memory.
- Why it is wrong: fewer containers fit, cluster utilization drops.
- Better approach: tune memory based on job needs.

- Mistake: Ignoring queues.
- Why it is wrong: shared clusters need fairness and isolation.
- Better approach: design queues by team/workload priority.

## 13. Mini Example

Cluster:

```text
10 nodes
each node: 64 GB RAM, 16 cores
```

YARN sees cluster capacity and allocates containers like:

```text
job A -> 20 containers
job B -> 10 containers
job C -> waits because queue is full
```

## 14. Interview Questions

1. What problem does YARN solve?
2. What is a container in YARN?
3. What is the difference between ResourceManager and NodeManager?
4. How does YARN support multiple processing engines?
5. How would you debug a job stuck in accepted state?

## 15. Interview Speak

"YARN is Hadoop's resource management layer. It separates cluster resource scheduling from processing engines, so MapReduce, Spark, Hive on Tez, and other applications can share the same cluster. ResourceManager schedules globally, NodeManagers manage worker resources, and ApplicationMasters coordinate individual applications."

## 16. Quick Recall

- One-line summary: YARN manages CPU and memory for Hadoop cluster jobs.
- Three keywords: ResourceManager, NodeManager, container.
- One trap: Confusing YARN with storage.
- One memory trick: HDFS stores files; YARN hands out compute seats.
