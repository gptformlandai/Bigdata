# Topic 015: Transactions

## Goal

Understand transactions as a way to group multiple operations into one reliable unit of work.

## Simple Explanation

A transaction says: either all of these changes happen, or none of them happen.

Classic example:

```text
Transfer $100 from account A to account B.
```

You must debit A and credit B. Doing only one is incorrect.

## Core Idea

- Definition: A transaction is a sequence of operations executed as a single logical unit.
- Why it matters: Transactions protect correctness when data changes.
- Related terms: commit, rollback, isolation, lock, write-ahead log, ACID.

## How It Works

Typical flow:

1. Begin transaction.
2. Read or modify data.
3. Validate constraints.
4. Commit if everything succeeds.
5. Roll back if something fails.

Example:

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE account_id = 'A';

UPDATE accounts
SET balance = balance + 100
WHERE account_id = 'B';

COMMIT;
```

If the second update fails:

```sql
ROLLBACK;
```

## How It Is Used

Transactions are used for:

- payments
- orders
- inventory updates
- banking transfers
- user account changes
- metadata updates
- exactly-once-like writes in some pipelines

## Big Data / System Design Angle

Transactions are easy on one database and harder across distributed systems.

Questions to ask:

- Is the transaction inside one database?
- Does it span services?
- Does it span databases?
- Can we accept eventual consistency?
- Do we need saga/outbox patterns?

In data lakes, older systems lacked transaction support. Modern lakehouse formats like Delta Lake, Apache Iceberg, and Apache Hudi add transactional table operations.

## Trade-offs

| Strong Transactions Give | Cost |
|---|---|
| correctness | coordination overhead |
| rollback safety | lower write concurrency in some cases |
| simpler application logic | locks/conflicts/deadlocks |
| consistent state | harder distributed scaling |

## Common Mistakes

- Mistake: Updating related rows without a transaction.
- Better way: Wrap dependent updates in one transaction.

- Mistake: Keeping transactions open too long.
- Better way: Keep transactions short to reduce locks and conflicts.

- Mistake: Expecting simple database transactions across microservices.
- Better way: Use sagas, outbox, idempotency, or workflow orchestration.

## Interview Speak

"A transaction groups operations into one unit so the system does not end in a partial state. I would use it for correctness-critical updates like payments or inventory. In distributed systems, cross-service transactions are expensive, so I would consider sagas, outbox, idempotency, and reconciliation."

## Quick Recall

- One-liner: A transaction turns multiple changes into one reliable unit.
- Keywords: begin, commit, rollback.
- Trap: Assuming transactions are simple across multiple services.
