# Topic 150: Partition Evolution

## 1. Goal

Understand how partition evolution lets a lakehouse table change partition strategy over time.

## 2. Baby Intuition

Imagine a store first organizes receipts by month.

Later, the store becomes huge and also organizes new receipts by day. Partition evolution lets old receipts stay organized by month while new receipts use the better daily layout.

## 3. What It Is

- Simple definition: Partition evolution means changing how new table data is partitioned without rewriting the whole old table immediately.
- Technical definition: Partition evolution allows a table format to support multiple partition specs across table snapshots, so older files can keep their original partition layout while newer files use a changed layout.
- Category: Lakehouse table evolution feature.
- Related terms: partition spec, hidden partitioning, Iceberg, metadata, pruning, rewrite.

## 4. Why It Exists

Partition choices are hard to get perfect on day one.

Workloads change:

- data volume grows
- query patterns change
- old partition columns become less useful
- timestamps need day instead of month
- region or tenant filters become important

Without partition evolution, changing layout may require rewriting huge historical tables.

## 5. Where It Fits In A Data Platform

```text
Old data files -> partition spec v1
New data files -> partition spec v2
Table metadata -> knows both specs
Query engine -> plans correctly across both
```

Iceberg is especially known for strong partition evolution support.

## 6. How It Works Step By Step

1. Table starts with a partition spec.
2. Data files are written with that spec.
3. Team changes the partition spec for future writes.
4. New data uses the new spec.
5. Metadata records which spec applies to each file.
6. Query planner handles old and new specs together.
7. Optional rewrite can migrate old data later.

Example:

```text
Spec v1: month(order_ts)
Spec v2: day(order_ts)
```

## 7. How To Use It Practically

Use partition evolution when:

- historical rewrite would be too expensive
- new query pattern needs better pruning
- table is large and continuously growing
- partition choice must change safely

Before changing:

- inspect query filters
- estimate partition cardinality
- check engine support
- test pruning behavior
- document the change

## 8. Real-World Scenario

- Product/system: Orders table.
- Problem: Table started small and used monthly partitions. Later daily analytics became slow.
- How partition evolution helps: new data can be partitioned by day without rewriting years of history immediately.
- What would go wrong without it: a full historical rewrite may be expensive and risky.

## 9. System Design Angle

Mention partition evolution when:

- table is long-lived
- query patterns are changing
- migration cost matters
- you want future-proof table design

Good design answer:

```text
I would avoid hard-coding folder partitions as a permanent contract.
Using a table format with partition evolution lets us adjust layout as access patterns change.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| avoids full rewrite | mixed layouts add planning complexity |
| adapts to new workloads | engine support must be verified |
| improves future pruning | old data may remain suboptimal |
| safer table evolution | requires metadata correctness |

## 11. Failure Modes

- Failure: New partition spec has too high cardinality.
- Symptom: many tiny files/partitions.
- Recovery: change spec again and compact/rewrite.
- Prevention: cardinality analysis.

- Failure: Engine does not fully support evolution.
- Symptom: wrong or slow queries.
- Recovery: use compatible engine/version.
- Prevention: compatibility testing.

- Failure: Old data remains poorly partitioned.
- Symptom: queries over history still slow.
- Recovery: rewrite historical data gradually.
- Prevention: plan migration windows.

## 12. Common Mistakes

- Mistake: Thinking partition evolution automatically rewrites old data.
- Why it is wrong: it mainly changes future layout.
- Better approach: schedule rewrites if old layout must improve.

- Mistake: Partitioning by a unique ID.
- Why it is wrong: it creates too many tiny partitions.
- Better approach: use bounded, common query filters.

## 13. Mini Example

```text
Before:
orders/month=2026-07/

After evolution:
new files use day(order_ts)

Table metadata knows old files use month and new files use day.
```

## 14. Interview Questions

1. What is partition evolution?
2. Why is it useful for large tables?
3. Does it rewrite old data automatically?
4. How can bad partition evolution hurt performance?
5. Which lakehouse format is known for this feature?

## 15. Interview Speak

"Partition evolution lets a lakehouse table change partition strategy for new writes while preserving old files with their original partition spec. It avoids expensive full rewrites and lets table layout adapt as query patterns change, but old data may still need rewrite if historical queries are slow."

## 16. Quick Recall

- One-line summary: Partition evolution changes future partition layout safely.
- Three keywords: spec, future writes, metadata.
- One trap: Assuming old files are magically repartitioned.
- One memory trick: New receipts can use a new filing system.
