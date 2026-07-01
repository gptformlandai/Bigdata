# Topic 116: Kafka ISR

## 1. Goal

Understand ISR, the in-sync replicas that are eligible for safe leader election and acknowledgments.

## 2. Baby Intuition

If three students copy notes from the teacher, only students who are caught up are trusted to continue teaching if the teacher leaves.

Those caught-up students are the ISR.

## 3. What It Is

- Simple definition: ISR is the set of replicas that are caught up with the leader.
- Technical definition: ISR, or in-sync replicas, is the set of partition replicas that are sufficiently up-to-date with the leader according to Kafka's replication rules.
- Category: Kafka replication reliability.
- Related terms: leader, follower, min.insync.replicas, acks, under-replicated partition.

## 4. Why It Exists

Not all replicas are equally safe.

A follower may be:

- down
- slow
- network partitioned
- behind the leader

Kafka needs to know which replicas are safe enough for acknowledgments and leader election.

## 5. Where It Fits In A Data Platform

```text
Partition replicas
  -> leader
  -> in-sync followers
  -> out-of-sync followers
```

ISR is checked during reliable writes and failover.

## 6. How It Works Step By Step

1. Leader receives records.
2. Followers replicate records.
3. Followers that keep up remain in ISR.
4. Followers that fall behind leave ISR.
5. If leader fails, new leader should be chosen from ISR.
6. Producer acks may depend on ISR count.

## 7. How To Use It Practically

Important configs:

```properties
acks=all
min.insync.replicas=2
```

Meaning:

```text
Producer gets success only when enough in-sync replicas have the write.
```

Monitor:

- under-replicated partitions
- ISR shrink/expand rate
- offline partitions

## 8. Real-World Scenario

- Product/system: Order events.
- Problem: Need to avoid acknowledging writes when only one broker has data.
- How ISR helps: `acks=all` plus `min.insync.replicas=2` requires multiple in-sync replicas.
- What would go wrong without it: broker loss after weak ack could lose acknowledged events.

## 9. System Design Angle

ISR connects consistency/durability to availability.

Stronger:

```text
acks=all + min.insync.replicas=2
```

Safer but may reject writes if too many replicas are unavailable.

Weaker:

```text
acks=1
```

Faster/more available, but less durable.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| safer acknowledged writes | possible produce failures |
| safer leader election | needs healthy replicas |
| durability visibility | monitoring complexity |

## 11. Failure Modes

- Failure: ISR shrinks below minimum.
- Symptom: producers with `acks=all` fail.
- Recovery: restore brokers/followers.
- Prevention: monitor ISR and broker health.

- Failure: unclean leader election enabled.
- Symptom: possible data loss.
- Recovery: investigate and restore from source if possible.
- Prevention: avoid unclean leader election for critical topics.

## 12. Common Mistakes

- Mistake: Setting `acks=all` but `min.insync.replicas=1`.
- Why it is wrong: safety may still be weak.
- Better approach: align replication factor and min ISR.

- Mistake: Ignoring ISR shrink alerts.
- Why it is wrong: durability risk increases.
- Better approach: alert on under-replication.

## 13. Mini Example

```text
replicas: broker 1, broker 2, broker 3
leader: broker 1
ISR: broker 1, broker 2
out of sync: broker 3
```

## 14. Interview Questions

1. What is ISR?
2. Why does ISR matter?
3. How do `acks=all` and `min.insync.replicas` work together?
4. What happens when ISR shrinks?
5. What is under-replication?

## 15. Interview Speak

"ISR means in-sync replicas: replicas that are caught up with the partition leader. Kafka uses ISR for safer acknowledgments and leader election. For critical topics, `acks=all` with `min.insync.replicas` ensures writes are acknowledged only when enough replicas have them, trading availability for durability."

## 16. Quick Recall

- One-line summary: ISR is the trusted caught-up replica set.
- Three keywords: in-sync, acks, durability.
- One trap: `acks=all` without meaningful min ISR.
- One memory trick: Only caught-up note takers can replace the teacher.
