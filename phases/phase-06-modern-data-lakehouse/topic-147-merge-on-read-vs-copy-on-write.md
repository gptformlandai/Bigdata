# Topic 147: Merge-On-Read Vs Copy-On-Write

## 1. Goal

Understand two common strategies for handling updates in lakehouse tables.

## 2. Baby Intuition

Copy-on-write is rewriting the whole corrected page.

Merge-on-read is keeping the original page plus a correction note, then combining them when someone reads.

## 3. What It Is

- Simple definition: Copy-on-write rewrites data files during updates; merge-on-read writes changes separately and merges them during reads.
- Technical definition: Copy-on-write applies updates by creating replacement base files at write time, while merge-on-read stores base files plus delta/log/delete files and resolves the latest view during reads or compaction.
- Category: Lakehouse update storage strategy.
- Related terms: Hudi, upsert, delete file, log file, compaction, read amplification, write amplification.

## 4. Why It Exists

Data lakes store large immutable files. Updating one row inside a file is not like updating one row in a database page.

A system must choose:

```text
Pay more during writes by rewriting files?
or
Pay more during reads by merging changes later?
```

That is the core COW vs MOR trade-off.

## 5. Where It Fits In A Data Platform

```text
CDC/update stream
  -> lakehouse table writer
  -> COW or MOR update strategy
  -> analytics readers
```

Hudi uses these terms directly. Similar ideas appear in Delta and Iceberg through file rewrites, delete files, and compaction patterns.

## 6. How It Works Step By Step

Copy-on-write:

1. Update arrives.
2. System finds affected data file.
3. System rewrites that file with the updated row.
4. New file replaces old file in table metadata.
5. Reads stay simple because base files already contain latest data.

Merge-on-read:

1. Update arrives.
2. System writes update to a log/delta/delete file.
3. Base file may remain unchanged.
4. Reader merges base file plus changes to produce latest view.
5. Later compaction merges changes into new base files.

## 7. How To Use It Practically

Choose copy-on-write when:

- reads are frequent and need predictable speed
- updates are not extremely frequent
- you can afford write amplification
- BI workloads query the table often

Choose merge-on-read when:

- updates are frequent
- low write latency matters
- streaming CDC is heavy
- you can schedule compaction
- readers can tolerate merge cost or read optimized views

## 8. Real-World Scenario

- Product/system: Customer profile table.
- Problem: customer attributes change often from CDC.
- COW fit: daily analytics reads are heavy and updates are moderate.
- MOR fit: updates arrive continuously and write freshness matters more than immediate read speed.
- What would go wrong without choosing intentionally: either writes become too expensive or reads become too slow.

## 9. System Design Angle

Interview keywords:

- CDC
- upserts
- deletes
- write amplification
- read amplification
- compaction
- freshness SLA

Good answer:

```text
For read-heavy reporting I lean COW.
For update-heavy near-real-time ingestion I consider MOR plus compaction.
```

## 10. Trade-offs

| Strategy | Pros | Cons |
|---|---|---|
| Copy-on-write | simpler/faster reads | expensive updates |
| Copy-on-write | fewer merge operations | high write amplification |
| Merge-on-read | faster writes | slower reads before compaction |
| Merge-on-read | good for frequent updates | compaction complexity |

## 11. Failure Modes

- Failure: COW on very frequent updates.
- Symptom: huge rewrite cost.
- Recovery: tune batching or consider MOR.
- Prevention: estimate update rate and file sizes.

- Failure: MOR without compaction.
- Symptom: readers merge too many delta/log files.
- Recovery: run compaction.
- Prevention: compaction schedule and thresholds.

- Failure: Wrong query view.
- Symptom: users read stale/read-optimized view when they need latest.
- Recovery: use correct real-time view.
- Prevention: document table read modes.

## 12. Common Mistakes

- Mistake: Saying COW is always better because reads are faster.
- Why it is wrong: high update rates can make writes too expensive.
- Better approach: balance read SLA, write SLA, and update frequency.

- Mistake: Choosing MOR without owning compaction.
- Why it is wrong: merge debt accumulates.
- Better approach: treat compaction as part of the design.

## 13. Mini Example

```text
Update one row in a 256 MB file:

COW:
  rewrite a new 256 MB file

MOR:
  write a small update log
  merge with base file during read
  compact later
```

## 14. Interview Questions

1. What is copy-on-write?
2. What is merge-on-read?
3. Which is better for read-heavy workloads?
4. Which is better for frequent CDC upserts?
5. Why does MOR need compaction?

## 15. Interview Speak

"Copy-on-write pays the update cost during writes by rewriting affected files, which keeps reads simpler. Merge-on-read writes changes separately and merges them during reads or compaction, improving write freshness but adding read and maintenance cost."

## 16. Quick Recall

- One-line summary: COW pays on write; MOR pays on read until compaction.
- Three keywords: rewrite, merge, compaction.
- One trap: Choosing MOR and forgetting compaction.
- One memory trick: Rewrite page vs correction note.
