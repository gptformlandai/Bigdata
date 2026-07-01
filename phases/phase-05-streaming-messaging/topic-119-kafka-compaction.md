# Topic 119: Kafka Compaction

## 1. Goal

Understand log compaction as Kafka's way to keep the latest value for each key.

## 2. Baby Intuition

If a user's address changes five times, sometimes you only need the latest address.

Compaction keeps the newest record per key and removes older versions eventually.

## 3. What It Is

- Simple definition: Compaction keeps latest record for each key in a topic.
- Technical definition: Kafka log compaction is a cleanup policy that retains at least the latest value for each record key, allowing topics to act as changelog streams.
- Category: Kafka storage cleanup/changelog pattern.
- Related terms: key, tombstone, changelog, cleanup.policy=compact, state restore.

## 4. Why It Exists

Some topics represent current state, not just event history.

Examples:

- latest user profile by user id
- latest product price by sku
- latest account status by account id

For these, keeping every old version forever may be unnecessary.

## 5. Where It Fits In A Data Platform

```text
keyed updates -> compacted Kafka topic -> consumers restore latest state
```

Used by:

- Kafka Streams state stores
- CDC changelog topics
- lookup tables
- state restore

## 6. How It Works Step By Step

Records:

```text
user1 -> city=A
user1 -> city=B
user2 -> city=C
user1 -> city=D
```

After compaction eventually:

```text
user2 -> city=C
user1 -> city=D
```

Kafka keeps latest value per key, not necessarily immediately.

## 7. How To Use It Practically

Topic config:

```bash
kafka-configs --bootstrap-server localhost:9092 --alter --entity-type topics --entity-name user_profiles --add-config cleanup.policy=compact
```

Delete key using tombstone:

```text
key=user1, value=null
```

Compaction later removes older values and eventually the tombstone after delete retention.

## 8. Real-World Scenario

- Product/system: Product catalog updates.
- Problem: Consumers need latest product details by product id.
- How compaction helps: Topic can retain latest product record per key.
- What would go wrong without it: consumers restoring state may need to replay huge old history.

## 9. System Design Angle

Use compacted topics for:

- changelog topics
- latest state by key
- lookup topics
- Kafka Streams state restoration

Do not use compaction when:

- every historical event matters
- audit trail must be complete
- records have no meaningful key

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| latest state retained | old event history removed |
| smaller restore volume | requires good keys |
| supports changelog patterns | compaction is eventual |
| tombstone deletes | cleanup semantics to understand |

## 11. Failure Modes

- Failure: missing/null keys.
- Symptom: compaction cannot work as intended.
- Recovery: fix producer.
- Prevention: enforce key schema.

- Failure: expecting immediate cleanup.
- Symptom: old records still visible for a while.
- Recovery: wait/tune compaction.
- Prevention: remember compaction is asynchronous.

## 12. Common Mistakes

- Mistake: Using compaction for audit logs.
- Why it is wrong: old events may be removed.
- Better approach: use delete retention topic or archive to data lake.

- Mistake: Not setting keys.
- Why it is wrong: compaction is key-based.
- Better approach: choose stable business key.

## 13. Mini Example

```text
account-1 -> ACTIVE
account-1 -> SUSPENDED
account-1 -> ACTIVE

After compaction:
account-1 -> ACTIVE
```

## 14. Interview Questions

1. What is Kafka compaction?
2. How is compaction different from retention delete?
3. What is a tombstone?
4. When would you use a compacted topic?
5. Why are keys required?

## 15. Interview Speak

"Kafka compaction keeps at least the latest record per key, making it useful for changelog and latest-state topics. It is key-based and asynchronous. I would use compaction for state restoration or lookup topics, but not for audit logs where every historical event must be preserved."

## 16. Quick Recall

- One-line summary: Compaction keeps latest value per key.
- Three keywords: key, latest, tombstone.
- One trap: Using compaction for full history.
- One memory trick: Keep the newest address per person.
