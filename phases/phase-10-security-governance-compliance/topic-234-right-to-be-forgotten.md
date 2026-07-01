# Topic 234: Right To Be Forgotten

## 1. Goal

Understand right-to-be-forgotten style deletion workflows from a data engineering point of view.

## 2. Baby Intuition

A person may request that their personal data be deleted.

For engineers, the hard part is finding every place their data went and deleting or anonymizing it safely.

## 3. What It Is

- Simple definition: Right to be forgotten is a privacy-related deletion request concept.
- Technical definition: In privacy contexts such as GDPR, erasure rights can require organizations to delete personal data under applicable conditions, with exceptions depending on law and policy.
- Category: Privacy rights workflow.
- Related terms: erasure, deletion request, lineage, retention, anonymization, legal hold, GDPR.

## 4. Why It Exists

People should not always have their personal data kept forever.

For data platforms, deletion is hard because data may exist in:

- raw lake files
- warehouse tables
- derived marts
- logs
- caches
- search indexes
- ML features
- backups
- third-party exports

## 5. Where It Fits In A Data Platform

```text
verified deletion request
  -> identify subject keys
  -> find datasets through lineage/catalog
  -> delete/anonymize according to policy
  -> validate and audit completion
```

## 6. How It Works Step By Step

1. Privacy/legal team validates request and applicability.
2. Resolve user identity to internal identifiers.
3. Use catalog/lineage to find affected datasets.
4. Delete, anonymize, or tombstone records according to policy.
5. Rebuild affected derived tables/aggregates where needed.
6. Handle backups and logs according to retention/legal policy.
7. Record audit evidence.
8. Prevent re-ingestion from old sources where required.

## 7. How To Use It Practically

Engineering requirements:

- stable subject identifier mapping
- data catalog and lineage
- deletion APIs/jobs
- tombstone propagation
- partition-aware deletion/compaction
- backup/restore policy
- audit log of deletion actions
- clear exception/legal hold handling

Common deletion styles:

| Style | Meaning |
|---|---|
| hard delete | physically remove record |
| soft delete/tombstone | mark as deleted and suppress |
| anonymization | remove link to person |
| aggregate rebuild | recompute outputs without person-level record |

## 8. Real-World Scenario

- Product/system: Customer analytics lakehouse.
- Problem: Customer requests deletion.
- How workflow helps: lookup customer IDs/tokens, delete from subject-level tables, propagate tombstones, rebuild marts, and record evidence.
- What would go wrong without lineage: some copies remain in downstream tables.

## 9. System Design Angle

Mention right to be forgotten when:

- GDPR/privacy rights are discussed
- personal data spreads across pipelines
- lakehouse upserts/deletes are needed
- retention/deletion requirements exist

Important caution:

```text
Whether deletion is legally required depends on policy/legal review.
Engineering builds the capability.
```

## 10. Trade-offs

| Approach | Benefit | Cost |
|---|---|---|
| hard delete | removes record | expensive in immutable files |
| tombstone | easy propagation | data may remain until cleanup |
| anonymization | preserves aggregate utility | must prevent re-identification |
| lineage automation | complete workflow | metadata investment |

## 11. Failure Modes

- Failure: Missing subject identifier mapping.
- Symptom: cannot find all records for person.
- Recovery: manual investigation.
- Prevention: identity resolution design.

- Failure: Derived table not updated.
- Symptom: deleted person still appears downstream.
- Recovery: backfill/recompute.
- Prevention: lineage-aware deletion.

- Failure: Re-ingestion from raw source.
- Symptom: deleted data returns.
- Recovery: add tombstone/suppression.
- Prevention: deletion registry.

## 12. Common Mistakes

- Mistake: Deleting only the main user table.
- Why it is wrong: data usually exists in events, logs, marts, and features.
- Better approach: trace through lineage and identifiers.

- Mistake: Ignoring immutable file formats.
- Why it is wrong: deleting rows may require rewriting files/compaction.
- Better approach: use lakehouse delete support and cleanup.

## 13. Mini Example

```text
Deletion request for user_id=42:
1. map to customer_token and email hash
2. delete from customer profile
3. tombstone events by user_id/customer_token
4. rebuild user-level aggregates
5. remove from search/features
6. record audit evidence
```

## 14. Interview Questions

1. What is right to be forgotten?
2. Why is deletion hard in data lakes?
3. How does lineage help?
4. What are tombstones?
5. How do backups affect deletion?

## 15. Interview Speak

"Right-to-be-forgotten workflows require identity resolution, lineage, deletion or anonymization jobs, propagation to derived datasets, backup/retention handling, and audit evidence. The legal applicability comes from privacy/legal teams, but engineering must make deletion operationally possible."

## 16. Quick Recall

- One-line summary: Right to be forgotten means privacy-driven deletion workflows.
- Three keywords: lineage, deletion, audit.
- One trap: Deleting only one table.
- One memory trick: Find every copy before saying forgotten.
