# Topic 146: Compaction

## 1. Goal

Understand compaction as a maintenance process that rewrites many small files into fewer better-sized files.

## 2. Baby Intuition

Compaction is cleaning up many tiny notes into a few organized notebooks.

The information stays the same, but reading becomes much easier.

## 3. What It Is

- Simple definition: Compaction combines small files into larger files.
- Technical definition: Compaction rewrites table data files to reduce file count, improve file size distribution, and sometimes reorganize records for better scan performance.
- Category: Lakehouse maintenance and performance optimization.
- Related terms: small files, OPTIMIZE, clustering, rewrite data files, file sizing, streaming ingestion.

## 4. Why It Exists

Small files happen because:

- streaming jobs write frequently
- many tasks write many outputs
- partitions are too granular
- CDC/upserts create many file fragments
- micro-batches are small

Too many small files hurt:

- query planning
- object-store listing
- metadata size
- scan efficiency
- engine task scheduling

## 5. Where It Fits In A Data Platform

```text
ingestion writes many files
  -> table grows fragmented
  -> compaction rewrites files
  -> queries scan fewer, larger files
```

Compaction is routine maintenance for Iceberg, Delta, and Hudi tables.

## 6. How It Works Step By Step

1. System finds small files or fragmented file groups.
2. It reads those files.
3. It writes fewer larger replacement files.
4. It commits metadata that removes old files and adds new files.
5. Old files remain physically present until cleanup is safe.
6. Future queries read the compacted files.

Important:

```text
Compaction changes physical layout, not logical table results.
```

## 7. How To Use It Practically

General examples:

```sql
-- Delta-style concept
OPTIMIZE orders;

-- Iceberg-style concept
CALL system.rewrite_data_files('lake.orders');
```

Practical rules:

- compact busy tables regularly
- do not compact every tiny batch immediately
- target file sizes suitable for your engine
- monitor file count and average file size
- avoid creating too few giant files

## 8. Real-World Scenario

- Product/system: Streaming clickstream lakehouse.
- Problem: Micro-batches write thousands of tiny files per day.
- How compaction helps: Rewrite small files into larger files so daily analytics reads faster.
- What would go wrong without it: query planning becomes slow and costs rise.

## 9. System Design Angle

Mention compaction when:

- streaming writes to a lake
- CDC creates many updates
- query latency slowly degrades
- file counts explode
- object-store/list costs rise

Design:

```text
ingestion job writes fresh data
scheduled maintenance compacts older partitions/windows
cleanup removes old unreferenced files after retention
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| faster queries | extra compute cost |
| fewer files | rewrite I/O |
| smaller metadata | must schedule/monitor |
| better scan efficiency | can compete with ingestion resources |

## 11. Failure Modes

- Failure: Compaction job fails halfway.
- Symptom: new files may exist but not be committed.
- Recovery: cleanup orphan files.
- Prevention: atomic table commits and retries.

- Failure: Over-compaction into huge files.
- Symptom: less parallelism.
- Recovery: rewrite into balanced file sizes.
- Prevention: choose sensible target file size.

- Failure: No compaction.
- Symptom: slow queries and massive file count.
- Recovery: run backfill compaction.
- Prevention: schedule maintenance early.

## 12. Common Mistakes

- Mistake: Thinking compaction is optional forever.
- Why it is wrong: lake tables naturally fragment over time.
- Better approach: include compaction in production operations.

- Mistake: Compacting the hottest data constantly.
- Why it is wrong: repeated rewrites waste compute.
- Better approach: compact after data cools or by threshold.

## 13. Mini Example

```text
Before:
  10,000 files x 2 MB

After:
  100 files x 200 MB

Same data, fewer files, faster planning.
```

## 14. Interview Questions

1. What is compaction?
2. Why do lakehouse tables get small files?
3. How does compaction help performance?
4. What are the costs of compaction?
5. When should compaction run?

## 15. Interview Speak

"Compaction is a maintenance job that rewrites many small lakehouse data files into fewer larger files. It reduces metadata overhead, object-store operations, and query planning time, but it costs compute and must be scheduled carefully."

## 16. Quick Recall

- One-line summary: Compaction turns file clutter into efficient layout.
- Three keywords: small files, rewrite, maintenance.
- One trap: Compacting too often or never compacting.
- One memory trick: Tiny notes become notebooks.
