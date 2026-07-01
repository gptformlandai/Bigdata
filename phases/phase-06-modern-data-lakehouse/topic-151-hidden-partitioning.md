# Topic 151: Hidden Partitioning

## 1. Goal

Understand hidden partitioning and why it makes lakehouse queries safer and easier.

## 2. Baby Intuition

Hidden partitioning is like asking a library for books from 2026.

You do not need to know which shelf labels the librarian uses internally. You just ask by normal information, and the librarian finds the right shelves.

## 3. What It Is

- Simple definition: Hidden partitioning means users query normal columns while the table format handles partition pruning internally.
- Technical definition: Hidden partitioning stores partition transforms in table metadata so query engines can derive partition filters from logical predicates without exposing physical partition columns to users.
- Category: Lakehouse table layout feature.
- Related terms: Iceberg, partition transform, partition pruning, days(timestamp), bucket(id), physical layout.

## 4. Why It Exists

Hive-style partitioning often exposed physical partition columns:

```text
dt=2026-07-01/
```

Users had to remember to filter `dt`, even if the real column was `event_ts`.

Problems:

- users forget partition filters
- duplicate columns like `event_ts` and `dt`
- partition layout becomes a user-facing contract
- changing partition strategy is hard

Hidden partitioning solves this by keeping partition logic in metadata.

## 5. Where It Fits In A Data Platform

```text
User query:
WHERE event_ts >= '2026-07-01'

Table metadata:
partition transform = days(event_ts)

Planner:
prune day partitions automatically
```

Apache Iceberg is strongly associated with hidden partitioning.

## 6. How It Works Step By Step

1. Table defines a partition transform.
2. Data files are written according to transformed values.
3. Users query the real data columns.
4. Query planner reads table metadata.
5. Planner converts predicates into partition pruning rules.
6. Engine skips files/partitions that cannot match.

Example transforms:

| Transform | Meaning |
|---|---|
| days(event_ts) | partition by date derived from timestamp |
| months(order_ts) | partition by month |
| bucket(16, user_id) | spread users across 16 buckets |
| truncate(3, country_code) | partition by shortened value |

## 7. How To Use It Practically

Use hidden partitioning to:

- reduce user mistakes
- avoid exposing physical layout
- support partition evolution
- keep queries natural
- improve pruning automatically

Query naturally:

```sql
SELECT *
FROM events
WHERE event_ts >= TIMESTAMP '2026-07-01 00:00:00'
  AND event_ts < TIMESTAMP '2026-07-02 00:00:00';
```

The user does not need to write `event_date = '2026-07-01'` separately.

## 8. Real-World Scenario

- Product/system: Clickstream events table.
- Problem: Analysts filter by timestamp but forget to filter the physical `dt` partition column.
- How hidden partitioning helps: the table format derives day partition pruning from timestamp filters.
- What would go wrong without it: queries accidentally scan too much data.

## 9. System Design Angle

Hidden partitioning is valuable when:

- many users query tables directly
- table layout may evolve
- timestamp transforms are common
- query mistakes are costly
- physical layout should not leak into business SQL

## 10. Trade-offs

| Pros | Cons |
|---|---|
| easier user queries | requires engine support |
| fewer partition mistakes | less obvious physical layout to beginners |
| enables layout evolution | debugging may require metadata inspection |
| avoids duplicate partition columns | planner must understand transforms |

## 11. Failure Modes

- Failure: Engine does not understand hidden partition transforms.
- Symptom: poor pruning or unsupported query.
- Recovery: use compatible engine/version.
- Prevention: compatibility testing.

- Failure: Query predicate cannot be converted.
- Symptom: more files scanned.
- Recovery: rewrite predicate simply.
- Prevention: teach analysts sargable filters.

- Failure: Bad transform choice.
- Symptom: too many files or weak pruning.
- Recovery: evolve partition spec.
- Prevention: analyze query patterns.

## 12. Common Mistakes

- Mistake: Adding duplicate visible date columns only for partitions.
- Why it is wrong: users can filter the wrong one or data can drift.
- Better approach: use table metadata partition transforms where supported.

- Mistake: Assuming hidden partitioning removes need for good filters.
- Why it is wrong: the engine still needs predicates to prune data.
- Better approach: query with clear filters on real columns.

## 13. Mini Example

```text
Physical layout may use days(event_ts).

User writes:
WHERE event_ts BETWEEN '2026-07-01' AND '2026-07-02'

Engine prunes to the matching day internally.
```

## 14. Interview Questions

1. What is hidden partitioning?
2. How is it different from Hive-style partition columns?
3. Why is it useful for timestamp columns?
4. What does the query engine need to support it?
5. How does it help partition evolution?

## 15. Interview Speak

"Hidden partitioning keeps physical partition transforms in table metadata. Users filter normal columns, and the engine derives partition pruning internally. This avoids exposing folder layout as a query contract and makes partition evolution safer."

## 16. Quick Recall

- One-line summary: Hidden partitioning lets users query data columns while metadata handles partitions.
- Three keywords: transform, pruning, metadata.
- One trap: Assuming it works without engine support.
- One memory trick: Ask the librarian, not the shelf label.
