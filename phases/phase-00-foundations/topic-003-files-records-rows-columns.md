# Topic 003: Files, Records, Rows, Columns

## Goal

Understand the basic building blocks used to store and process data.

## Simple Explanation

A file is a container. A record is one item inside the container. In tabular data, each record is usually a row, and each field in the record is a column.

Example:

```text
File: orders.csv
Record/Row: o1,c1,49.99,paid
Column: amount
```

## Core Idea

- Definition: Files hold data; records represent individual facts or events; rows and columns organize records into tables.
- Why it matters: Big Data systems split, scan, compress, partition, and query data based on these units.
- Related terms: field, attribute, tuple, table, dataset, partition, block.

## How They Relate

```text
Dataset
  -> File(s)
      -> Records / Rows
          -> Fields / Columns
```

Example CSV file:

```csv
order_id,customer_id,amount,status
o1,c1,49.99,paid
o2,c2,19.99,failed
o3,c1,99.00,paid
```

- File: `orders.csv`
- Header: `order_id,customer_id,amount,status`
- Record/row: `o1,c1,49.99,paid`
- Column: `amount`
- Field value: `49.99`

## How It Is Used

Data engineers work with these units constantly:

- read files from object storage
- parse records from files or streams
- transform rows using SQL or Spark
- select columns for analytics
- partition files by date, region, or tenant

## Big Data / System Design Angle

At small scale, one file may be enough. At Big Data scale, datasets are usually many files across many machines.

Why this matters:

- Too few huge files can reduce parallelism.
- Too many tiny files can overload metadata systems and query engines.
- Columnar formats let engines scan only needed columns.
- Row-based formats are often simpler for streaming or transactional writes.

## Example

SQL thinks in rows and columns:

```sql
SELECT customer_id, SUM(amount) AS total_spend
FROM orders
WHERE status = 'paid'
GROUP BY customer_id;
```

Spark also processes rows, but distributes them across partitions:

```python
paid_orders = orders_df.where("status = 'paid'")
```

## Common Mistakes

- Mistake: Thinking a dataset is always one file.
- Better way: In Big Data, a dataset is often a directory containing many partitioned files.

- Mistake: Ignoring file size.
- Better way: Use reasonably sized files for distributed processing, commonly hundreds of MB for analytical workloads.

- Mistake: Confusing rows and columns with storage layout.
- Better way: A table can be stored row-wise or column-wise depending on format.

## Interview Speak

"A dataset is usually made of files. Each file contains records, and in tabular systems those records are rows with columns. This matters because distributed engines split work by files and partitions, while query performance depends heavily on file size, layout, and whether the engine can skip unnecessary rows or columns."

## Quick Recall

- One-liner: Files contain records; tables organize records as rows and columns.
- Keywords: file, row, column.
- Trap: Forgetting that Big Data tables are often many files, not one physical table file.
