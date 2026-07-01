# Topic 225: Data Masking

## 1. Goal

Understand data masking as hiding sensitive values while still allowing some use of the data.

## 2. Baby Intuition

Masking is like covering part of a phone number:

```text
555-123-9876 -> XXX-XXX-9876
```

The user sees enough to recognize the record, but not the full sensitive value.

## 3. What It Is

- Simple definition: Data masking hides sensitive data from users who do not need the full value.
- Technical definition: Data masking transforms or partially hides sensitive fields at rest, in queries, or in non-production copies to reduce exposure while preserving usability.
- Category: Data protection control.
- Related terms: dynamic masking, static masking, redaction, anonymization, tokenization, column-level security.

## 4. Why It Exists

Many users need data context but not raw sensitive values.

Examples:

- support can see last 4 digits
- analysts can see region but not address
- developers can test with masked production-like data
- BI users can see aggregate data but not raw identifiers

Masking reduces unnecessary exposure.

## 5. Where It Fits In A Data Platform

```text
sensitive table/column
  -> masking policy
  -> user query or data copy
  -> masked output for unapproved users
```

Masking can be applied in warehouses, BI tools, APIs, data lake query engines, or ETL outputs.

## 6. How It Works Step By Step

1. Identify sensitive fields.
2. Define who can see full values.
3. Define masking rule.
4. Apply rule dynamically at query time or statically during data copy.
5. Log access to full or masked data.
6. Review masking policy regularly.

## 7. How To Use It Practically

Masking examples:

| Field | Masked Output |
|---|---|
| email | a***@example.com |
| phone | XXX-XXX-1234 |
| SSN | XXX-XX-6789 |
| credit card | **** **** **** 1234 |
| address | city/state only |

Types:

| Type | Meaning |
|---|---|
| dynamic masking | mask when query runs based on user role |
| static masking | create masked copy of dataset |
| redaction | remove or blank value |
| partial masking | show only part of value |

## 8. Real-World Scenario

- Product/system: Customer support dashboard.
- Problem: Support agents need customer lookup but not full SSN.
- How masking helps: agents see last 4 digits only; compliance users can see full value if approved.
- What would go wrong without it: sensitive identifiers are exposed to too many users.

## 9. System Design Angle

Use masking when:

- users need partial context
- raw PII/PHI is unnecessary
- non-prod data needs production-like shape
- BI tools expose sensitive columns
- support workflows need limited identifiers

Be careful:

```text
Masking is not always irreversible anonymization.
```

Masked data can still be sensitive depending on context.

## 10. Trade-offs

| Pros | Cons |
|---|---|
| reduces sensitive exposure | may not fully anonymize |
| preserves some usability | can break exact joins/searches |
| useful for BI/support | policies must be maintained |
| dynamic by role possible | privileged users still need controls |

## 11. Failure Modes

- Failure: Masking only in BI, raw table still broadly accessible.
- Symptom: users bypass BI to see raw data.
- Recovery: restrict base table.
- Prevention: enforce controls at storage/warehouse layer.

- Failure: Masking too weak.
- Symptom: user can infer identity.
- Recovery: stronger masking or aggregation.
- Prevention: privacy review.

- Failure: Masking breaks pipeline logic.
- Symptom: joins/search fail.
- Recovery: use tokenization or surrogate keys.
- Prevention: design safe join keys.

## 12. Common Mistakes

- Mistake: Calling masked data anonymous.
- Why it is wrong: partial values may still identify people.
- Better approach: classify masked data based on re-identification risk.

- Mistake: Masking only final dashboards.
- Why it is wrong: raw data may still be exposed elsewhere.
- Better approach: apply layered access controls.

## 13. Mini Example

```text
Policy:
if user has role pii_reader:
  show email
else:
  show masked_email(email)
```

## 14. Interview Questions

1. What is data masking?
2. Static vs dynamic masking?
3. Masking vs tokenization?
4. Is masked data anonymous?
5. Where should masking be enforced?

## 15. Interview Speak

"Data masking hides or partially transforms sensitive values so users can do their job without seeing raw PII/PHI. I would combine masking with column-level access, least privilege, audit logs, and careful classification because masking is not automatically anonymization."

## 16. Quick Recall

- One-line summary: Masking hides sensitive values from users who do not need them.
- Three keywords: dynamic, static, partial.
- One trap: Thinking masking equals anonymization.
- One memory trick: Show last 4, hide the rest.
