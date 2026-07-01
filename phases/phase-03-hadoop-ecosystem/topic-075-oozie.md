# Topic 075: Oozie

## 1. Goal

Understand Oozie as Hadoop's classic workflow scheduler for coordinating jobs.

## 2. Baby Intuition

A data pipeline is often many steps:

```text
import data -> clean data -> aggregate data -> export report
```

Oozie is like a coordinator that says:

```text
run step 2 only after step 1 succeeds
```

## 3. What It Is

- Simple definition: Oozie schedules and coordinates Hadoop jobs.
- Technical definition: Apache Oozie is a workflow scheduler system for managing Hadoop jobs such as MapReduce, Hive, Pig, Sqoop, and shell actions.
- Category: Workflow orchestration.
- Related terms: workflow, coordinator, bundle, action, DAG, schedule, dependency.

## 4. Why It Exists

Real data pipelines are not one job.

They need:

- dependencies
- schedules
- retries
- failure handling
- parameterized dates
- multi-step workflows

Before tools like Oozie, teams used cron and scripts, which became hard to manage.

## 5. Where It Fits In A Data Platform

```text
Schedule/Trigger -> Oozie -> Sqoop/Hive/MapReduce jobs -> HDFS outputs
```

Oozie is orchestration, not storage or processing.

It coordinates tools that do the work.

## 6. How It Works Step By Step

Workflow:

1. Define actions in XML.
2. Define dependencies between actions.
3. Submit workflow to Oozie.
4. Oozie starts first action.
5. If it succeeds, Oozie starts next action.
6. If it fails, Oozie follows error path or retries.
7. Workflow completes or fails.

Coordinator:

- runs workflows on a schedule
- supports data availability conditions

## 7. How To Use It Practically

Workflow shape:

```text
start
  -> sqoop_import
  -> hive_transform
  -> export_report
  -> end
```

Oozie command examples:

```bash
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -run
oozie job -info <job_id>
oozie job -kill <job_id>
```

Modern note:

```text
Airflow, Dagster, Prefect, and cloud orchestrators are more common today.
```

## 8. Real-World Scenario

- Product/system: Nightly sales reporting pipeline.
- Problem: Import DB tables, run Hive transformations, and publish report every morning.
- How Oozie helps: Coordinates steps, retries failures, and runs on schedule.
- What would go wrong without it: Cron scripts become fragile and dependency handling is manual.

## 9. System Design Angle

Oozie is useful when:

- Hadoop jobs need scheduling
- multiple steps depend on each other
- jobs run daily/hourly
- data availability matters

Design questions:

- What triggers the workflow?
- What happens if data arrives late?
- What retries are safe?
- Is each step idempotent?
- How are failures alerted?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| job dependency management | XML verbosity |
| scheduled workflows | older ecosystem |
| Hadoop integration | less flexible than modern orchestrators |
| retries and error paths | operational complexity |

## 11. Failure Modes

- Failure: Upstream data missing.
- Symptom: workflow waits or fails.
- Recovery: rerun after data lands.
- Prevention: data availability checks.

- Failure: Step fails midway.
- Symptom: downstream actions do not run.
- Recovery: retry/rerun from failed action.
- Prevention: idempotent steps and validation.

- Failure: Oozie server issue.
- Symptom: workflows not starting or status unavailable.
- Recovery: restart/failover.
- Prevention: monitoring.

## 12. Common Mistakes

- Mistake: Making jobs non-idempotent.
- Why it is wrong: retries can duplicate outputs.
- Better approach: write to temp paths and atomically publish.

- Mistake: No alerting.
- Why it is wrong: failed workflows may go unnoticed.
- Better approach: alerts and SLAs.

## 13. Mini Example

Pipeline:

```text
01_import_orders
  -> 02_clean_orders
  -> 03_aggregate_daily_revenue
  -> 04_export_dashboard_table
```

Oozie manages the order.

## 14. Interview Questions

1. What problem does Oozie solve?
2. How is Oozie different from Hive or MapReduce?
3. What is a workflow scheduler?
4. Why should pipeline steps be idempotent?
5. What modern tools often replace Oozie?

## 15. Interview Speak

"Oozie is a Hadoop workflow scheduler. It coordinates jobs like Sqoop, Hive, and MapReduce with dependencies, schedules, retries, and failure paths. It is an orchestration tool, not a processing engine. Modern teams often use Airflow or managed orchestrators for similar workflows."

## 16. Quick Recall

- One-line summary: Oozie schedules and coordinates Hadoop jobs.
- Three keywords: workflow, schedule, dependency.
- One trap: Confusing orchestration with processing.
- One memory trick: Oozie is the traffic controller for Hadoop jobs.
