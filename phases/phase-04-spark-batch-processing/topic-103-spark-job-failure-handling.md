# Topic 103: Spark Job Failure Handling

## 1. Goal

Understand how Spark jobs fail, retry, and recover, and how to design reliable pipelines.

## 2. Baby Intuition

Spark expects some workers to fail.

If one worker drops a box, Spark gives that box to another worker.

But if the manager fails, the whole project may fail.

## 3. What It Is

- Simple definition: Spark failure handling is how Spark retries failed tasks and how engineers design jobs to recover safely.
- Technical definition: Spark provides task retry, stage retry, executor loss recovery, and lineage-based recomputation, while pipeline reliability also requires idempotent writes, checkpointing, monitoring, and rerun strategy.
- Category: Fault tolerance and operations.
- Related terms: task retry, executor lost, lineage, checkpoint, idempotency, speculative execution.

## 4. Why It Exists

Distributed jobs fail because:

- nodes crash
- executors OOM
- network fails
- bad input records exist
- shuffle files disappear
- permissions change
- storage paths conflict
- driver crashes

Spark handles some failures automatically, but not all.

## 5. Where It Fits In A Data Platform

```text
Scheduled Spark job -> failures/retries -> output tables -> monitoring/alerts
```

Production ETL needs:

- retries
- idempotent output
- logging
- alerts
- data validation
- rerun strategy

## 6. How It Works Step By Step

Task failure:

1. Executor task fails.
2. Spark retries task on same or another executor.
3. If retry succeeds, stage continues.
4. If task fails too many times, stage/job fails.

Executor failure:

1. Executor dies.
2. Spark marks tasks as failed/lost.
3. Spark reschedules tasks.
4. Cached data on executor may be lost.
5. Lost data can be recomputed from lineage if possible.

Driver failure:

1. Driver dies.
2. Application usually fails.
3. External scheduler must rerun job.

## 7. How To Use It Practically

Helpful configs:

```text
spark.task.maxFailures
spark.stage.maxConsecutiveAttempts
spark.speculation
```

Practical pipeline safety:

- write to temp path
- validate output
- atomically publish final path/table
- avoid partial overwrite issues
- make reruns idempotent
- quarantine bad records
- alert on failures

## 8. Real-World Scenario

- Product/system: Nightly customer metrics job.
- Problem: Executor OOM kills some tasks.
- How Spark helps: Retries tasks elsewhere.
- What still needs engineering: If output was partially written, rerun must not duplicate or corrupt results.

## 9. System Design Angle

Spark failure handling is not just automatic retries.

Design questions:

- Can the job be rerun safely?
- Are writes idempotent?
- What happens to partial output?
- How are bad records handled?
- What is the SLA?
- Who gets alerted?
- Can lost cached data be recomputed?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| automatic task retry | repeated failures waste time |
| lineage recomputation | long lineage can be expensive |
| executor loss recovery | lost cache may slow job |
| speculation can reduce stragglers | duplicate task work |

## 11. Failure Modes

- Failure: Bad input record always crashes task.
- Symptom: task fails repeatedly and job aborts.
- Recovery: quarantine or handle bad record.
- Prevention: validation and defensive parsing.

- Failure: Partial output from failed job.
- Symptom: duplicate/corrupt result.
- Recovery: cleanup and rerun.
- Prevention: temp paths and atomic commits.

- Failure: Shuffle fetch failure.
- Symptom: stage retry.
- Recovery: Spark recomputes missing shuffle data.
- Prevention: stable executors/storage/network.

## 12. Common Mistakes

- Mistake: Assuming task retry makes pipeline reliable.
- Why it is wrong: output side effects can still corrupt data.
- Better approach: design idempotent writes.

- Mistake: Overwriting production path directly.
- Why it is wrong: failure may leave partial output.
- Better approach: write temp then publish.

## 13. Mini Example

Safe write pattern:

```text
write /tmp/job_run_123
validate row counts
swap/publish to /curated/table/dt=2026-07-01
cleanup old temp
```

## 14. Interview Questions

1. What happens if a Spark task fails?
2. What happens if an executor fails?
3. Why is driver failure serious?
4. How do you make Spark writes idempotent?
5. What causes repeated task failures?

## 15. Interview Speak

"Spark can retry failed tasks and recover lost executor work using lineage, but production reliability also requires idempotent writes, safe output commit patterns, validation, monitoring, and rerun strategy. Driver failure usually fails the application, while executor/task failures can often be recovered automatically."

## 16. Quick Recall

- One-line summary: Spark retries tasks, but pipeline reliability is your design.
- Three keywords: retry, lineage, idempotent.
- One trap: Partial output corruption.
- One memory trick: Spark can redo work, but you must protect the final result.
