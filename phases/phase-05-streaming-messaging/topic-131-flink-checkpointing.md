# Topic 131: Flink Checkpointing

## 1. Goal

Understand checkpointing as Flink's recovery mechanism for stateful streaming.

## 2. Baby Intuition

In a video game, checkpoints let you restart from the last saved point instead of the beginning.

Flink checkpoints save stream processing state so jobs can recover after failure.

## 3. What It Is

- Simple definition: A checkpoint is a consistent snapshot of Flink job state.
- Technical definition: Flink checkpointing periodically captures operator state and source positions in a consistent distributed snapshot for fault-tolerant recovery.
- Category: Stream processing fault tolerance.
- Related terms: state, barrier, savepoint, exactly-once, source offset, state backend.

## 4. Why It Exists

Streaming jobs run continuously.

Failures happen:

- node crash
- job restart
- deployment update
- network issue
- sink failure

Without checkpoints, stateful jobs may lose counts, duplicates, or progress.

## 5. Where It Fits In A Data Platform

```text
Flink job state + source offsets -> checkpoint storage -> restore after failure
```

Checkpoint storage could be durable storage like HDFS/S3/GCS depending on setup.

## 6. How It Works Step By Step

1. Flink triggers checkpoint.
2. Checkpoint barriers flow through streams.
3. Operators snapshot their state.
4. Source positions are recorded.
5. Snapshot is stored durably.
6. If job fails, Flink restarts from latest successful checkpoint.

## 7. How To Use It Practically

Conceptual config:

```text
checkpoint interval: every 60 seconds
checkpoint timeout: 10 minutes
checkpoint storage: durable path
```

Watch:

- checkpoint duration
- checkpoint size
- failed checkpoints
- alignment time
- checkpoint storage errors

## 8. Real-World Scenario

- Product/system: Real-time order count dashboard.
- Problem: Job crashes after counting millions of events.
- How checkpointing helps: Restores counts and source positions from checkpoint.
- What would go wrong without it: counts may restart or duplicate.

## 9. System Design Angle

Checkpointing affects:

- recovery point
- processing overhead
- sink consistency
- state backend cost
- job latency under pressure

Trade-off:

```text
frequent checkpoints -> less lost progress, more overhead
infrequent checkpoints -> less overhead, more replay after failure
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| state recovery | checkpoint overhead |
| stronger consistency | storage cost |
| less reprocessing | tuning complexity |
| safer upgrades | checkpoint failures to monitor |

## 11. Failure Modes

- Failure: checkpoint storage unavailable.
- Symptom: checkpoints fail.
- Recovery: restore storage/access.
- Prevention: durable reliable storage.

- Failure: checkpoints too slow.
- Symptom: checkpoint timeouts/backpressure.
- Recovery: tune interval/state/backend.
- Prevention: manage state size.

## 12. Common Mistakes

- Mistake: Enabling stateful processing without checkpointing.
- Why it is wrong: failure recovery is unsafe.
- Better approach: configure checkpointing.

- Mistake: Checkpoint interval too aggressive.
- Why it is wrong: overhead can slow processing.
- Better approach: tune for SLA and state size.

## 13. Mini Example

```text
checkpoint at offset 1000 with state count=500
job fails at offset 1200
restore from offset 1000 and count=500
reprocess 1001-1200
```

## 14. Interview Questions

1. What is Flink checkpointing?
2. What is saved in a checkpoint?
3. How does checkpointing support exactly-once?
4. Checkpoint vs savepoint?
5. What makes checkpoints slow?

## 15. Interview Speak

"Flink checkpointing periodically saves a consistent snapshot of operator state and source positions. On failure, the job restores from the latest successful checkpoint and resumes processing. Checkpoints are essential for stateful streaming, but state size, checkpoint interval, and storage reliability must be tuned."

## 16. Quick Recall

- One-line summary: Checkpoints are save points for Flink state and progress.
- Three keywords: snapshot, state, restore.
- One trap: Stateful streaming without checkpoints.
- One memory trick: Video game save point.
