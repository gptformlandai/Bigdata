# Topic 149: Metadata Scaling

## 1. Goal

Understand why lakehouse table metadata must scale and how table formats reduce planning overhead.

## 2. Baby Intuition

Finding one book is easy in a small shelf.

Finding one book in a giant library needs a catalog, sections, labels, and summaries. Metadata is that catalog for huge tables.

## 3. What It Is

- Simple definition: Metadata scaling means keeping table metadata fast and manageable as tables become huge.
- Technical definition: Metadata scaling is the ability of a table format/catalog to efficiently track schemas, snapshots, partitions, manifests, files, statistics, and deletes for very large analytical tables.
- Category: Lakehouse scalability and query planning.
- Related terms: manifest, file statistics, partition pruning, data skipping, catalog, small files, snapshots.

## 4. Why It Exists

Large lakehouse tables can have:

- millions of files
- thousands of partitions
- many snapshots
- frequent commits
- many schema versions
- delete files or log files

Before reading data, engines must plan what to read.

If metadata is too large or poorly organized, queries are slow before scanning even starts.

## 5. Where It Fits In A Data Platform

```text
User query
  -> engine asks catalog/table metadata
  -> metadata pruning decides candidate files
  -> engine scans data files
```

Good metadata means fewer unnecessary files are read.

## 6. How It Works Step By Step

1. Table tracks data files and their stats.
2. Query has filters, such as date or customer region.
3. Planner checks metadata before reading files.
4. Partition metadata skips whole groups.
5. File-level stats skip individual files.
6. Only relevant files are scheduled for scan.

Common metadata:

| Metadata | Why it helps |
|---|---|
| schema | interpret records correctly |
| partitions | skip broad data sections |
| file list | know table contents |
| min/max stats | skip files by filter |
| snapshots | consistent versions |
| delete files/logs | apply row-level changes |

## 7. How To Use It Practically

Keep metadata healthy:

- avoid excessive small files
- avoid high-cardinality partition explosion
- expire old snapshots
- rewrite/compact manifests when needed
- collect/refresh table statistics
- choose partitioning based on query filters
- monitor planning time separately from scan time

## 8. Real-World Scenario

- Product/system: Petabyte-scale clickstream table.
- Problem: The table has millions of files and daily queries filter by date, country, and event type.
- How metadata scaling helps: partition/file stats prune most files before scan.
- What would go wrong without it: every query spends a long time listing and planning files.

## 9. System Design Angle

Mention metadata scaling for:

- very large tables
- slow query planning
- millions of files
- multi-engine lakehouse access
- object-store list bottlenecks
- high partition count

Design:

```text
Use table format metadata instead of raw folder listing.
Compact small files.
Use partitioning/stats/clustering for pruning.
Expire old metadata safely.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| faster query planning | metadata maintenance jobs |
| better file pruning | extra metadata storage |
| avoids raw object listing | catalog reliability matters |
| supports huge tables | complexity increases with features |

## 11. Failure Modes

- Failure: Millions of tiny files.
- Symptom: huge metadata and slow planning.
- Recovery: compaction.
- Prevention: tune writers and target file sizes.

- Failure: Too many old snapshots.
- Symptom: metadata growth.
- Recovery: expire snapshots.
- Prevention: retention policy.

- Failure: Bad partition design.
- Symptom: weak pruning or partition explosion.
- Recovery: partition evolution/rewrite if supported.
- Prevention: design around query patterns.

## 12. Common Mistakes

- Mistake: Only measuring scan time.
- Why it is wrong: planning time can dominate huge lake tables.
- Better approach: measure planning, metadata load, and file scan separately.

- Mistake: Partitioning by user_id.
- Why it is wrong: high cardinality creates too many partitions and files.
- Better approach: partition by common bounded filters like date, region, or bucketed values.

## 13. Mini Example

```text
Query:
WHERE event_date = '2026-07-01'

Bad metadata:
  list millions of files

Good metadata:
  jump to matching partition/manifests
  scan only likely files
```

## 14. Interview Questions

1. What is metadata scaling?
2. Why do millions of small files hurt planning?
3. How do manifests or file stats help?
4. How do old snapshots affect metadata?
5. How do you tune a table with slow planning?

## 15. Interview Speak

"Lakehouse performance depends not only on data scans but also on metadata planning. Table formats scale metadata using catalogs, snapshots, manifests, partition info, and file statistics so engines can prune files before reading them. I would manage this with compaction, snapshot expiration, stats, and good partition design."

## 16. Quick Recall

- One-line summary: Metadata scaling keeps huge lakehouse tables plannable.
- Three keywords: manifests, stats, pruning.
- One trap: Ignoring planning time.
- One memory trick: Giant tables need a giant-card catalog that still opens fast.
