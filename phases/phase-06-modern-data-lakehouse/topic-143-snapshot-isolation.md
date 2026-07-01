# Topic 143: Snapshot Isolation

## 1. Goal

Understand how snapshot isolation lets readers see a consistent lakehouse table while writers are changing it.

## 2. Baby Intuition

Imagine reading a book while someone is editing the next edition.

Snapshot isolation means you keep reading your edition calmly. You do not suddenly see half of the next edition mixed into your current pages.

## 3. What It Is

- Simple definition: Snapshot isolation lets each reader see one stable version of a table.
- Technical definition: Snapshot isolation is an isolation model where a transaction reads from a consistent table snapshot, while writers commit new snapshots without changing what active readers see.
- Category: Transaction isolation concept.
- Related terms: ACID, snapshot, commit, version, concurrent reader, concurrent writer.

## 4. Why It Exists

Data lake tables are often read and written at the same time.

Without snapshot isolation:

- a dashboard may read half old data and half new data
- a Spark job may see files added during planning
- failed writes may leak into queries
- concurrent updates may produce confusing results

Snapshot isolation gives a clean rule:

```text
Each query reads one table version.
```

## 5. Where It Fits In A Data Platform

```text
Writer commits Snapshot 101
Reader A starts on Snapshot 101
Writer commits Snapshot 102
Reader A still reads Snapshot 101
Reader B starts later and reads Snapshot 102
```

This matters for Iceberg, Delta Lake, Hudi, and warehouse-style systems.

## 6. How It Works Step By Step

1. A reader asks the catalog for the current table snapshot.
2. The reader plans the query using that snapshot's metadata.
3. A writer creates new data files and new metadata.
4. The writer commits a new snapshot atomically.
5. The reader continues using the original snapshot.
6. New readers can see the newly committed snapshot.

Important state:

```text
reader snapshot id != always latest snapshot id
```

That is intentional.

## 7. How To Use It Practically

You usually do not manually "turn on" snapshot isolation. It is provided by the table format when you use supported commands.

Practical habits:

- write through table APIs
- avoid manual object-store file edits
- monitor commit conflicts
- keep snapshot retention long enough for long-running jobs
- test concurrent batch and streaming writes

## 8. Real-World Scenario

- Product/system: Finance daily reporting table.
- Problem: Analysts run long queries while ETL updates the same table.
- How snapshot isolation helps: analysts get one consistent version instead of a mixed state.
- What would go wrong without it: reports may show impossible totals during table updates.

## 9. System Design Angle

Mention snapshot isolation when interviewers ask about:

- concurrent reads and writes
- atomic table updates
- partial file visibility
- rollback/time travel
- lakehouse correctness

Design answer:

```text
Writers create new files first, then atomically commit metadata.
Readers bind to one snapshot and ignore later commits until they refresh.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| consistent reads | old snapshots must be retained |
| safe concurrent writes/reads | commit conflict handling required |
| avoids partial table state | metadata complexity |
| supports rollback/time travel | cleanup must respect active readers |

## 11. Failure Modes

- Failure: Old snapshot files removed too early.
- Symptom: long-running query fails.
- Recovery: rerun query on available snapshot.
- Prevention: safe retention and cleanup policy.

- Failure: Two writers conflict.
- Symptom: one commit fails.
- Recovery: retry using latest metadata.
- Prevention: write serialization or conflict-aware writers.

- Failure: Manual file overwrite.
- Symptom: snapshot points to corrupted/missing data.
- Recovery: restore files or rollback if possible.
- Prevention: restrict direct storage mutations.

## 12. Common Mistakes

- Mistake: Thinking a query always reads the latest committed data.
- Why it is wrong: it reads the snapshot chosen when the query started.
- Better approach: explain stable reader view vs latest table state.

- Mistake: Cleaning old files without considering active readers.
- Why it is wrong: readers may still depend on old snapshot files.
- Better approach: align cleanup retention with query duration and audit needs.

## 13. Mini Example

```text
10:00 Query starts on Snapshot 5: files A, B
10:01 Writer commits Snapshot 6: files A, B, C
10:02 Query still reads A, B
10:03 New query reads A, B, C
```

## 14. Interview Questions

1. What is snapshot isolation?
2. How does it help data lake writes?
3. Can a reader see half-written files?
4. What happens if cleanup deletes old snapshot files?
5. How do commit conflicts happen?

## 15. Interview Speak

"Snapshot isolation means each reader binds to a stable table version. Writers create new files and atomically commit new metadata, so active readers do not see partial writes or mixed file lists. New readers can see the new snapshot after the commit."

## 16. Quick Recall

- One-line summary: Snapshot isolation gives each query a stable table version.
- Three keywords: stable view, snapshot, atomic commit.
- One trap: Cleaning old files while readers still need them.
- One memory trick: Read your edition, not the editor's draft.
