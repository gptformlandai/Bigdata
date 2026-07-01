# Topic 153: Vacuum/Cleanup

## 1. Goal

Understand cleanup operations that remove old unreferenced lakehouse files and metadata safely.

## 2. Baby Intuition

Cleanup is like throwing away old drafts after you are sure nobody needs them.

If you throw them away too early, someone reading an older draft gets stuck.

## 3. What It Is

- Simple definition: Vacuum/cleanup removes old files and metadata that are no longer needed.
- Technical definition: Lakehouse cleanup deletes unreferenced data files, expired snapshots, old transaction logs, manifests, and orphan files after a retention period while preserving active readers and required time travel.
- Category: Lakehouse maintenance and storage management.
- Related terms: VACUUM, expire snapshots, orphan files, retention, time travel, snapshot isolation.

## 4. Why It Exists

Lakehouse tables create old files during:

- updates
- deletes
- compaction
- failed writes
- schema/table rewrites
- snapshot history

Old files are useful for time travel and active readers, but keeping everything forever costs money and increases metadata overhead.

Cleanup balances:

```text
recovery/history needs vs storage/metadata cost
```

## 5. Where It Fits In A Data Platform

```text
Writes/compaction create new table versions
  -> old files remain for safety
  -> cleanup removes files after retention
  -> storage and metadata stay healthy
```

Different systems use names like `VACUUM`, `expire snapshots`, or `clean`.

## 6. How It Works Step By Step

1. Table has current and historical snapshots/versions.
2. Cleanup checks retention policy.
3. Snapshots older than allowed retention may be expired.
4. Files no longer referenced by retained snapshots become deletion candidates.
5. Orphan files from failed writes may also be identified.
6. Cleanup deletes safe candidates.
7. Time travel range shrinks according to retained history.

Important:

```text
Cleanup must respect active readers, audit requirements, and rollback SLA.
```

## 7. How To Use It Practically

Before cleanup, know:

- maximum query duration
- time travel/audit window
- legal retention requirements
- backup/replay strategy
- table criticality
- streaming reader behavior

Examples:

```sql
-- Delta-style concept
VACUUM orders RETAIN 168 HOURS;

-- Iceberg-style concept
CALL system.expire_snapshots('lake.orders');
```

## 8. Real-World Scenario

- Product/system: Orders lakehouse table.
- Problem: Daily MERGE and compaction keep old files for rollback.
- How cleanup helps: after a safe retention window, unreferenced files are deleted to control storage cost.
- What would go wrong without it: storage cost and metadata keep growing forever.

## 9. System Design Angle

Mention cleanup when:

- tables use time travel
- upserts/deletes/compaction run often
- cost control matters
- privacy deletion matters
- old snapshots accumulate

Good design answer:

```text
I would set retention based on max reader duration, rollback needs, audit policy, and cost.
```

## 10. Trade-offs

| Longer Retention | Shorter Retention |
|---|---|
| more time travel | lower storage cost |
| safer rollback | less recovery window |
| protects long readers | can break old readers if too short |
| useful for audit | less old sensitive data retained |

## 11. Failure Modes

- Failure: Cleanup runs too aggressively.
- Symptom: time travel fails or active readers lose files.
- Recovery: restore from backup if possible.
- Prevention: retention guardrails.

- Failure: Cleanup never runs.
- Symptom: high storage cost and metadata growth.
- Recovery: run cleanup in controlled batches.
- Prevention: scheduled maintenance.

- Failure: Orphan detection deletes valid files.
- Symptom: table corruption/query failures.
- Recovery: restore files or rollback.
- Prevention: use table-aware cleanup and safe retention.

## 12. Common Mistakes

- Mistake: Vacuuming immediately after a bad write.
- Why it is wrong: it may remove files needed for rollback/time travel.
- Better approach: investigate first, then clean after recovery window.

- Mistake: Using one retention policy for every table.
- Why it is wrong: audit-critical tables and temporary tables have different needs.
- Better approach: set retention by table class.

## 13. Mini Example

```text
Snapshot 10 references A, B
Snapshot 11 references A, C

After Snapshot 10 expires:
B may be deleted if no retained snapshot needs it.
```

## 14. Interview Questions

1. What does VACUUM do?
2. Why can cleanup break time travel?
3. What are orphan files?
4. How do you choose retention?
5. Why should cleanup be table-aware?

## 15. Interview Speak

"Vacuum or cleanup removes files and metadata no longer referenced by retained table versions. It controls cost and metadata growth, but retention must protect active readers, rollback needs, audits, and time travel requirements."

## 16. Quick Recall

- One-line summary: Cleanup deletes old unreferenced lakehouse files after a safe window.
- Three keywords: retention, orphan files, time travel.
- One trap: Vacuuming too aggressively.
- One memory trick: Throw away drafts only after nobody needs them.
