# Topic 142: Table Formats

## 1. Goal

Understand what a table format is and why it is different from a file format.

## 2. Baby Intuition

Parquet is like a box of pages.

A table format is the library system that knows which boxes belong to the table, what version is current, what the schema is, and which boxes are old.

## 3. What It Is

- Simple definition: A table format defines how a lake table is tracked, changed, and read.
- Technical definition: A table format manages table metadata, snapshots/versions, schema, partitioning, file lists, deletes, and commit rules over underlying data files.
- Category: Lakehouse storage abstraction.
- Related terms: Parquet, ORC, Avro, Iceberg, Delta Lake, Hudi, metadata, catalog.

## 4. Why It Exists

File formats answer:

```text
How is data stored inside one file?
```

Table formats answer:

```text
Which files make up this table right now, and how can that table safely change?
```

Without table formats, data lakes struggle with:

- atomic writes
- concurrent readers/writers
- schema evolution
- updates/deletes
- time travel
- old file cleanup
- metadata scaling

## 5. Where It Fits In A Data Platform

```text
Query engine
  -> catalog
  -> table format metadata
  -> Parquet/ORC/Avro data files
  -> object storage
```

Examples:

| Layer | Examples |
|---|---|
| file format | Parquet, ORC, Avro |
| table format | Iceberg, Delta Lake, Hudi |
| catalog | Hive Metastore, Glue, Unity Catalog, Nessie |
| engine | Spark, Flink, Trino, Presto |

## 6. How It Works Step By Step

1. Data is written into files.
2. Metadata records the files in the table.
3. A commit updates the table state.
4. Readers load the current table state.
5. Query planning uses metadata and statistics to skip unnecessary files.
6. Maintenance jobs rewrite files or remove old metadata safely.

## 7. How To Use It Practically

Choose a table format based on:

- supported query engines
- cloud/platform
- upsert/delete needs
- governance/catalog integration
- streaming support
- maintenance features
- team familiarity

Simple rule:

```text
Parquet stores data efficiently.
Iceberg/Delta/Hudi make many Parquet files behave like a reliable table.
```

## 8. Real-World Scenario

- Product/system: Payments analytics lake.
- Problem: Thousands of Parquet files are written daily and analysts need stable SQL tables.
- How table formats help: They track committed files, schema changes, old versions, and deletes.
- What would go wrong without them: queries might read partial files or miss files after manual folder changes.

## 9. System Design Angle

Table formats matter when:

- multiple engines read/write the same data
- correctness matters
- data is updated/deleted
- audit or rollback is required
- table size is large enough that metadata needs structure

They are less important for:

- tiny one-off exports
- temporary local files
- simple immutable archive blobs

## 10. Trade-offs

| Pros | Cons |
|---|---|
| reliable table state | extra metadata layer |
| ACID-style commits | operational learning curve |
| time travel | old versions use storage |
| schema evolution | engine compatibility matters |
| better pruning | metadata maintenance required |

## 11. Failure Modes

- Failure: Metadata and files disagree.
- Symptom: missing files, query failures, or wrong results.
- Recovery: restore metadata or rebuild table.
- Prevention: use table APIs, not manual file edits.

- Failure: Catalog misconfiguration.
- Symptom: engine sees wrong table version/location.
- Recovery: fix catalog pointer.
- Prevention: controlled deployments and backups.

## 12. Common Mistakes

- Mistake: Saying "we use Parquet, so we have Delta/Iceberg-like behavior."
- Why it is wrong: Parquet has no table transaction log by itself.
- Better approach: distinguish file format from table format.

- Mistake: Mixing manual file operations with table-format operations.
- Why it is wrong: metadata may not know what changed.
- Better approach: use supported INSERT/MERGE/DELETE/OPTIMIZE commands.

## 13. Mini Example

```text
File format question:
  What is inside orders_001.parquet?

Table format question:
  Is orders_001.parquet part of the current orders table version?
```

## 14. Interview Questions

1. What is a table format?
2. How is a table format different from Parquet?
3. Why do Iceberg, Delta, and Hudi exist?
4. What metadata does a table format track?
5. How does a table format help query performance?

## 15. Interview Speak

"A file format like Parquet stores records efficiently inside individual files. A table format like Iceberg, Delta, or Hudi manages many files as one reliable table, including snapshots, schemas, commits, deletes, partitions, and metadata used for query planning."

## 16. Quick Recall

- One-line summary: Table formats turn files into reliable lakehouse tables.
- Three keywords: metadata, snapshots, commits.
- One trap: Confusing file format with table format.
- One memory trick: Parquet is the page; table format is the table of contents.
