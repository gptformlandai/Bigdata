# Topic 016: ACID

## Goal

Understand the four properties that make transactions reliable: Atomicity, Consistency, Isolation, and Durability.

## Simple Explanation

ACID is the safety promise behind reliable database transactions.

For a bank transfer, ACID helps ensure:

- money is not half moved
- rules are not violated
- concurrent transfers do not corrupt balances
- committed changes survive crashes

## Core Idea

- Definition: ACID is a set of transaction guarantees for correctness and reliability.
- Why it matters: ACID protects critical data from partial writes, invalid states, race conditions, and data loss.
- Related terms: transaction, commit, rollback, isolation level, write-ahead log.

## The Four Properties

| Property | Meaning | Simple Example |
|---|---|---|
| Atomicity | all or nothing | debit and credit both happen, or neither happens |
| Consistency | rules remain valid | balance cannot violate constraints |
| Isolation | concurrent transactions do not interfere incorrectly | two withdrawals do not overwrite each other |
| Durability | committed data survives failure | committed order remains after crash |

## How It Works Internally

Databases use mechanisms such as:

- locks
- MVCC
- write-ahead logs
- constraints
- commit protocols
- recovery logs

You do not need every internal detail yet, but know the purpose: preserve correctness despite failure and concurrency.

## Big Data / System Design Angle

ACID matters most when incorrect data is unacceptable:

- payments
- inventory
- orders
- claims
- account balances
- financial reporting
- metadata commits

In Big Data, ACID appears in:

- relational databases
- warehouses
- transactional metadata stores
- lakehouse table formats

Trade-off:

```text
stronger correctness -> more coordination and operational cost
```

## Example

Without ACID:

```text
1. Create order
2. Charge payment
3. Reduce inventory
4. System crashes after payment but before inventory update
```

Now the system may show paid order but incorrect inventory.

With good transactional design:

- group operations when possible
- use idempotency
- use outbox/events
- reconcile when operations cross services

## Common Mistakes

- Mistake: Saying consistency in ACID is the same as consistency in CAP.
- Better way: ACID consistency means database rules remain valid. CAP consistency means every read sees the latest write in a distributed system.

- Mistake: Using strong ACID everywhere.
- Better way: Use strong ACID where correctness requires it; use eventual consistency where acceptable.

- Mistake: Ignoring isolation anomalies.
- Better way: Choose isolation level based on correctness requirements.

## Interview Speak

"ACID describes transaction guarantees. Atomicity gives all-or-nothing changes, consistency preserves database rules, isolation protects concurrent transactions, and durability ensures committed data survives crashes. I would use ACID strongly for money, inventory, and metadata correctness, but I would be careful with distributed transaction cost."

## Quick Recall

- One-liner: ACID is the reliability contract for transactions.
- Keywords: atomicity, isolation, durability.
- Trap: Confusing ACID consistency with CAP consistency.
