# Topic 145: ACID On Data Lake

## 1. Goal

Understand how lakehouse systems bring ACID-like guarantees to files on object storage.

## 2. Baby Intuition

Plain files are like people placing papers on a table at the same time.

ACID on a data lake adds a rulebook: either a full change becomes official, or it does not count.

## 3. What It Is

- Simple definition: ACID on a data lake means table changes are reliable even though data is stored as files.
- Technical definition: Lakehouse table formats provide atomic commits, consistent metadata, isolated reader snapshots, and durable table history using transaction logs or metadata commits over data files.
- Category: Transactional lakehouse behavior.
- Related terms: atomicity, consistency, isolation, durability, commit, snapshot, transaction log.

## 4. Why It Exists

Object storage is excellent for cheap scalable files, but files alone do not provide table transactions.

Without ACID behavior:

- failed jobs can expose partial outputs
- concurrent writers can overwrite each other
- readers can see inconsistent file lists
- deletes/updates can be unsafe
- recovery is manual

ACID makes lake tables suitable for trusted analytics.

## 5. Where It Fits In A Data Platform

```text
Spark/Flink writes data files
  -> table format commits metadata atomically
  -> readers see old or new table state, not half state
```

It is a core promise of Iceberg, Delta Lake, and Hudi.

## 6. How It Works Step By Step

Lakehouse writes usually follow this pattern:

1. Writer reads current table metadata.
2. Writer creates new data files.
3. Writer creates new metadata/log entries describing file additions/removals.
4. Writer attempts an atomic commit.
5. If commit succeeds, new snapshot/version is official.
6. If commit fails, new files are not part of the table and can be cleaned.
7. Readers use committed metadata only.

ACID mapping:

| Letter | Lakehouse meaning |
|---|---|
| Atomicity | whole commit appears or does not |
| Consistency | metadata and schema rules stay valid |
| Isolation | readers use stable snapshots |
| Durability | committed metadata/files persist in storage |

## 7. How To Use It Practically

Use supported commands:

```sql
INSERT INTO orders SELECT * FROM new_orders;

DELETE FROM orders WHERE status = 'CANCELLED';

MERGE INTO orders USING updates ON orders.id = updates.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

Do not manually move/delete files behind the table format.

## 8. Real-World Scenario

- Product/system: Healthcare claims analytics.
- Problem: Daily claims table must not expose partial loads.
- How ACID helps: a failed load does not become the official table snapshot.
- What would go wrong without it: analysts may report on incomplete claims data.

## 9. System Design Angle

ACID on a data lake matters when:

- downstream reports depend on correctness
- tables receive concurrent writes
- upserts/deletes are required
- pipelines can fail halfway
- audit/rollback is needed

Interview phrase:

```text
Writers commit metadata atomically after writing files; readers only see committed snapshots.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| reliable table updates | commit/metadata overhead |
| safe reader/writer concurrency | conflict retries |
| enables MERGE/DELETE | file rewrites can be expensive |
| supports rollback | old versions need storage |

## 11. Failure Modes

- Failure: Writer crashes after writing files but before commit.
- Symptom: orphan files exist but readers do not see them.
- Recovery: orphan cleanup.
- Prevention: scheduled cleanup and idempotent writes.

- Failure: Concurrent writers update same table.
- Symptom: commit conflict.
- Recovery: retry transaction.
- Prevention: partition-aware writes or serialized jobs.

- Failure: Object store/catalog issue during commit.
- Symptom: uncertain commit state.
- Recovery: inspect metadata/log and retry carefully.
- Prevention: robust commit protocol and monitoring.

## 12. Common Mistakes

- Mistake: Believing object storage automatically gives database transactions.
- Why it is wrong: object storage stores files, not table-level transaction semantics.
- Better approach: use a table format transaction layer.

- Mistake: Mixing direct file writes with table writes.
- Why it is wrong: metadata will not match files.
- Better approach: write through Iceberg/Delta/Hudi APIs.

## 13. Mini Example

```text
Bad old style:
  write output files directly to /orders/
  reader may see half output

Lakehouse style:
  write files to storage
  commit metadata
  reader sees new version only after commit
```

## 14. Interview Questions

1. What does ACID mean in a lakehouse?
2. How can files support atomic table commits?
3. What happens if a writer fails before commit?
4. Why are manual file edits risky?
5. How does isolation work for readers?

## 15. Interview Speak

"ACID on a data lake is implemented by table formats that separate physical file writing from the official table commit. New files are written first, then metadata or a transaction log is atomically updated. Readers only use committed snapshots, so they avoid partial writes."

## 16. Quick Recall

- One-line summary: ACID makes file-backed lake tables reliable.
- Three keywords: commit, snapshot, metadata.
- One trap: Assuming object storage gives ACID by itself.
- One memory trick: Files are drafts until metadata says official.
