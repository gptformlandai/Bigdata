# Topic 130: Flink State

## 1. Goal

Understand state as Flink's memory of past events.

## 2. Baby Intuition

If you want to count how many purchases a user made today, you must remember the current count.

That memory is state.

## 3. What It Is

- Simple definition: State is information a stream processor remembers while processing events.
- Technical definition: Flink state is fault-tolerant data maintained by operators, often keyed by event key, and checkpointed for recovery.
- Category: Stateful stream processing.
- Related terms: keyed state, operator state, state backend, TTL, checkpoint.

## 4. Why It Exists

Many streaming problems need memory:

- counts per user
- last location per driver
- current account balance
- recent events for fraud pattern
- deduplication event ids
- window aggregates

Without state, Flink could only process each event independently.

## 5. Where It Fits In A Data Platform

```text
event -> keyed operator -> state lookup/update -> output
```

State sits inside Flink operators and is saved through checkpoints.

## 6. How It Works Step By Step

Example: count events per user.

1. Event arrives with `user_id`.
2. Flink routes event to key group for that user.
3. Operator reads current count from state.
4. Operator increments count.
5. Operator writes updated count to state.
6. Operator emits result if needed.
7. Checkpoint saves state for recovery.

## 7. How To Use It Practically

State types conceptually:

- value state: one value per key
- list state: list per key
- map state: map per key
- reducing/aggregating state

Important practices:

- set TTL when state should expire
- monitor state size
- avoid unbounded state
- choose state backend carefully

## 8. Real-World Scenario

- Product/system: Fraud detection.
- Problem: Need count of failed payments per user in last 10 minutes.
- How state helps: Flink stores recent per-user failure counts.
- What would go wrong without it: every event would be processed without context.

## 9. System Design Angle

State affects:

- memory/storage
- checkpoint duration
- recovery time
- correctness
- scaling

Ask:

- what key is state stored by?
- how long does state live?
- how large can state grow?
- how is state restored after failure?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| context-aware processing | state size management |
| deduplication and joins | checkpoint overhead |
| windowed/rolling metrics | recovery time |
| real-time features | TTL design |

## 11. Failure Modes

- Failure: unbounded state growth.
- Symptom: slow checkpoints/OOM/storage growth.
- Recovery: add TTL or cleanup.
- Prevention: design lifecycle.

- Failure: wrong keying.
- Symptom: incorrect aggregations.
- Recovery: fix keyBy logic and reprocess.
- Prevention: define business key carefully.

## 12. Common Mistakes

- Mistake: Forgetting state cleanup.
- Why it is wrong: state grows forever.
- Better approach: use TTL/windows/cleanup.

- Mistake: Keying by high-skew key.
- Why it is wrong: one task holds too much state.
- Better approach: inspect key distribution.

## 13. Mini Example

```text
key=user_1
state=count=3
new event arrives
state=count=4
```

## 14. Interview Questions

1. What is Flink state?
2. Keyed state vs operator state?
3. Why does state need checkpointing?
4. What is state TTL?
5. What happens if state grows too large?

## 15. Interview Speak

"Flink state is the remembered context used by operators, usually keyed by entity. It enables counts, deduplication, joins, windows, and fraud rules. State must be checkpointed for recovery and managed with TTL/cleanup because unbounded state hurts memory, checkpoint time, and recovery."

## 16. Quick Recall

- One-line summary: State is Flink's memory.
- Three keywords: keyed, checkpoint, TTL.
- One trap: Unbounded state.
- One memory trick: Streaming memory per key.
