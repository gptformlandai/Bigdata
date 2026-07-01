# Topic 144: Time Travel

## 1. Goal

Understand time travel in lakehouse tables and why it is useful for debugging, recovery, and audits.

## 2. Baby Intuition

Time travel is like version history in a document.

If today's table is wrong, you can look at yesterday's version and compare what changed.

## 3. What It Is

- Simple definition: Time travel lets you query an older version of a table.
- Technical definition: Time travel uses retained table snapshots, transaction logs, or commit timelines to reconstruct table state as of a version, timestamp, or commit.
- Category: Lakehouse table feature.
- Related terms: snapshot, version, timestamp, rollback, audit, retention, VACUUM.

## 4. Why It Exists

Data changes. Sometimes changes are wrong.

Time travel helps with:

- debugging bad pipelines
- recovering from accidental deletes
- comparing before/after states
- audit investigations
- reproducible ML training
- historical reports

Without time travel, recovery usually means restoring backups or replaying raw data.

## 5. Where It Fits In A Data Platform

```text
Current table -> query latest snapshot
Older table   -> query previous snapshot/version/timestamp
```

It is commonly supported by Delta Lake, Iceberg, and Hudi in different forms.

## 6. How It Works Step By Step

1. Every successful write creates a version/snapshot/commit.
2. Table metadata remembers which files were active in each version.
3. A time travel query asks for an older version or timestamp.
4. The engine loads metadata for that older state.
5. The engine reads files referenced by that older state.
6. Cleanup later removes old versions/files after retention expires.

Important:

```text
Time travel works only while old metadata and data files still exist.
```

## 7. How To Use It Practically

Examples:

```sql
-- Conceptual examples. Syntax differs by engine/table format.
SELECT * FROM orders VERSION AS OF 25;

SELECT * FROM orders TIMESTAMP AS OF '2026-06-30 10:00:00';
```

Use time travel for:

- checking what changed
- rebuilding downstream tables
- restoring data after bad jobs
- validating audit questions
- training ML models on reproducible data

## 8. Real-World Scenario

- Product/system: Revenue reporting table.
- Problem: A bad deployment overwrote yesterday's revenue categories.
- How time travel helps: Query the previous table version, compare differences, and restore/reprocess.
- What would go wrong without it: teams must rebuild from raw data or backups under pressure.

## 9. System Design Angle

Time travel is valuable when:

- data correctness is high stakes
- auditability matters
- pipelines are complex
- ML reproducibility is required
- rollback must be fast

Design consideration:

```text
Retention controls how far back time travel works.
Longer retention = more recovery window + more storage cost.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| easy debugging | uses extra storage |
| rollback support | cleanup must be careful |
| audit/history | old versions may expose sensitive data |
| reproducible ML | retention costs grow |

## 11. Failure Modes

- Failure: VACUUM/cleanup removed old files.
- Symptom: old version cannot be queried.
- Recovery: use backups/raw replay if available.
- Prevention: set retention to match audit/recovery needs.

- Failure: Bad data existed before time travel window.
- Symptom: cannot inspect old table version.
- Recovery: restore from backup.
- Prevention: keep raw immutable source and backups.

- Failure: PII deletion conflict.
- Symptom: old versions still contain deleted personal data.
- Recovery: privacy-aware deletion and cleanup.
- Prevention: governance policy for retention and deletion.

## 12. Common Mistakes

- Mistake: Assuming time travel is a backup.
- Why it is wrong: cleanup can remove old versions, and object storage loss still matters.
- Better approach: use time travel plus backups/raw replay for critical data.

- Mistake: Keeping infinite history without governance.
- Why it is wrong: cost and privacy risk grow.
- Better approach: set retention per table criticality.

## 13. Mini Example

```text
Version 40: correct revenue
Version 41: bad pipeline writes wrong categories
Version 42: fix pipeline

Time travel lets you inspect Version 40 and compare with Version 41.
```

## 14. Interview Questions

1. What is time travel?
2. How does time travel work in a lakehouse table?
3. Is time travel the same as backup?
4. How does VACUUM affect time travel?
5. Where is time travel useful in ML?

## 15. Interview Speak

"Time travel lets us query a lakehouse table as of a previous version or timestamp using retained metadata and data files. It is useful for debugging, rollback, audits, and reproducible ML, but retention and cleanup policies determine how far back it works."

## 16. Quick Recall

- One-line summary: Time travel queries old table versions.
- Three keywords: version, snapshot, retention.
- One trap: Treating time travel as a full backup.
- One memory trick: Table version history.
