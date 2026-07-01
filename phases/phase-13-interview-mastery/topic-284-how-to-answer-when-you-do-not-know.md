# Topic 284: How To Answer When You Do Not Know

## 1. Goal

Learn how to handle unknown interview questions without panicking or pretending.

## 2. Baby Intuition

Not knowing something is normal.

The interview is not only testing memory. It is testing how you reason when memory is incomplete.

## 3. The Safe Response Pattern

Use:

```text
I have not used that deeply, but here is how I understand it.
I would reason from the problem it solves.
I would compare it to something I do know.
I would validate by checking docs/metrics/tests in a real system.
```

## 4. What Not To Do

Avoid:

- pretending you know
- inventing fake details
- rambling
- going silent
- over-apologizing
- saying "I have no idea" and stopping

## 5. Bridge From Known Concepts

Examples:

Question:

```text
Have you used Apache Hudi?
```

Answer:

```text
I have studied lakehouse table formats more generally. Hudi focuses strongly on upserts and incremental processing on data lakes. I would compare it with Iceberg and Delta around metadata, merge-on-read/copy-on-write behavior, compaction, and query engine support.
```

## 6. Reason Out Loud

If asked a new system design:

```text
I have not designed this exact system before, but I would start by clarifying the users, data sources, scale, freshness, correctness, and serving requirements. Then I would choose ingestion, storage, processing, and serving based on those constraints.
```

## 7. Admit Boundaries Clearly

Good:

```text
I have not configured that in production, but I understand the concept and can explain the trade-offs.
```

Bad:

```text
Yes, I know it completely.
```

when you do not.

## 8. Recovery Phrases

Use:

- "Let me reason through it."
- "I know the adjacent concept..."
- "The main problem this tool solves is..."
- "I would validate this assumption by..."
- "My confidence is higher on the architecture than the exact config."

## 9. When You Make A Mistake

If interviewer corrects you:

```text
That makes sense. I was thinking about it as <old assumption>, but with your correction, the better design would be <updated answer>.
```

This shows adaptability.

## 10. Common Unknowns

Prepare for:

- tool you have not used
- cloud service-specific detail
- exact config parameter
- edge case in distributed systems
- company-specific architecture
- deep internals

You can still answer by reasoning from fundamentals.

## 11. Interview Speak

"I have not used that exact tool in production, so I do not want to invent details. Conceptually, I understand it as solving <problem>. I would compare it with <known tool>, and in a real implementation I would verify the exact behavior with documentation, a small test, and production metrics."

## 12. Quick Recall

- One-line summary: Unknown answers should be honest, reasoned, and grounded in fundamentals.
- Three keywords: honest, adjacent, validate.
- One trap: pretending.
- Memory trick: do not fake; reason.

