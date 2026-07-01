# Topic 279: Debugging Production Pipeline Questions

## 1. Goal

Learn how to answer production debugging questions calmly and systematically.

## 2. Baby Intuition

Debugging is detective work under pressure.

Your answer should show:

```text
I protect users first.
I find the failing layer.
I recover safely.
I prevent it from happening again.
```

## 3. General Incident Framework

Use:

1. Assess impact.
2. Stop bad output if needed.
3. Check recent changes.
4. Trace source to sink.
5. Compare expected vs actual.
6. Recover with retry/replay/backfill/rollback.
7. Communicate status.
8. Add prevention.

## 4. Pipeline Is Late

Check:

- source data arrival
- scheduler status
- task logs
- cluster capacity
- upstream dependencies
- Kafka lag
- warehouse/query slowness
- recent deployments

Strong answer:

```text
I first determine whether data is late at the source, stuck in ingestion, slow in processing, or blocked during publish.
```

## 5. Dashboard Numbers Are Wrong

Check:

- metric definition
- source data completeness
- filter/date logic
- duplicate events
- late events
- join explosion
- recent code changes
- whether live or finalized data is shown

Recovery:

- mark dashboard stale/wrong if user-facing
- rollback or fix logic
- recompute affected partitions
- explain impact window

## 6. Row Count Dropped Suddenly

Possible causes:

- source failed
- schema changed
- filter became too strict
- partition missing
- join turned into inner join accidentally
- upstream delete
- permissions issue

Debug:

```text
compare row counts by source, partition, and pipeline stage
```

## 7. Duplicate Records Appeared

Possible causes:

- retry wrote non-idempotently
- missing dedupe key
- CDC replay applied twice
- bad join many-to-many
- backfill overlapped with scheduled job

Fix:

- dedupe by stable key
- add idempotent merge
- isolate backfill output
- add uniqueness tests

## 8. Kafka Consumer Lag Is Growing

Check:

- lag by partition
- consumer errors
- processing latency
- downstream sink slowness
- hot partition
- rebalance loop
- traffic spike

Recovery:

- scale consumers if partitions allow
- optimize processing
- fix downstream bottleneck
- pause non-critical consumers if needed

## 9. Spark Job Fails Or Is Slow

Check:

- Spark UI
- slow stage
- shuffle size
- skew
- executor OOM
- driver OOM
- bad join
- small files

Recovery:

- tune partitions
- broadcast small table
- salt skewed keys
- filter/project early
- increase resources only after diagnosis

## 10. Airflow DAG Failed

Check:

- task logs
- upstream dependency
- source freshness
- executor/worker health
- retry status
- recent code/config change

Recovery:

- retry idempotent task
- rerun partition
- mark delayed if source missing
- trigger backfill

## 11. Prevention Patterns

- freshness checks
- row count checks
- uniqueness tests
- schema contracts
- DLQs
- idempotent writes
- replayable raw data
- runbooks
- alerts based on user impact
- postmortems

## 12. Interview Speak

"I would first assess impact and prevent bad data from spreading. Then I would trace the pipeline source to sink, checking freshness, logs, row counts, schema changes, lag, and recent deployments. Recovery depends on the root cause: retry if idempotent, replay from raw data, backfill affected partitions, or rollback bad code. After recovery, I would add monitoring/tests to prevent recurrence."

## 13. Quick Recall

- One-line summary: Debugging means impact, isolate, recover, prevent.
- Three keywords: impact, trace, replay.
- One trap: retrying blindly without idempotency.
- Memory trick: protect users, then investigate.

