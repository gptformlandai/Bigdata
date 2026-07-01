# Topic 232: Column-Level Security

## 1. Goal

Understand column-level security as controlling access to sensitive columns.

## 2. Baby Intuition

Column-level security means a user can see the table but not every column.

Example: they can see `customer_id` and `region`, but not `email` or `ssn`.

## 3. What It Is

- Simple definition: Column-level security restricts access to specific columns.
- Technical definition: Column-level security enforces policies that allow, deny, mask, or transform sensitive columns based on user identity, role, attributes, or context.
- Category: Fine-grained data access control.
- Related terms: CLS, masking, data classification, sensitive column, PII, PHI, RBAC, ABAC.

## 4. Why It Exists

Tables often mix safe and sensitive columns:

```text
customer_id, signup_date, region, email, phone, ssn
```

Many analytics users need non-sensitive columns but not raw identifiers.

Column-level security avoids copying many table variants.

## 5. Where It Fits In A Data Platform

```text
shared table
  -> column policy
  -> full, masked, or denied column access
```

Used in warehouses, lakehouse catalogs, BI semantic layers, and data APIs.

## 6. How It Works Step By Step

1. Sensitive columns are classified/tagged.
2. Policies are attached to columns or tags.
3. User submits query.
4. System checks user permissions.
5. Sensitive columns are allowed, denied, or masked.
6. Access is logged.

## 7. How To Use It Practically

Policy examples:

| Column | General Analyst | PII Reader |
|---|---|---|
| customer_id | allowed | allowed |
| region | allowed | allowed |
| email | masked | allowed |
| phone | masked | allowed |
| ssn | denied | allowed only if approved |

Good practices:

- tag sensitive columns
- enforce policy close to data
- use masking where partial value is useful
- deny highly sensitive columns by default
- audit full-value access

## 8. Real-World Scenario

- Product/system: Customer warehouse table.
- Problem: Marketing analysts need segments and regions but not email/phone.
- How CLS helps: analysts query the same customer table but sensitive columns are masked or denied.
- What would go wrong without it: teams create uncontrolled copies without sensitive columns.

## 9. System Design Angle

Use column-level security when:

- tables contain mixed sensitivity
- users need only some fields
- PII/PHI columns exist
- masking policies are required
- shared tables serve many teams

Combine with:

- row-level security
- masking
- audit logs
- data classification

## 10. Trade-offs

| Pros | Cons |
|---|---|
| protects sensitive fields | policy maintenance |
| avoids table duplication | query/tool compatibility matters |
| supports masked access | users may need alternative join keys |
| centralizes control | raw storage bypass risk |

## 11. Failure Modes

- Failure: Column not classified.
- Symptom: sensitive column exposed.
- Recovery: tag and restrict.
- Prevention: automated classification scans.

- Failure: Raw table accessible outside policy layer.
- Symptom: users bypass CLS.
- Recovery: restrict raw access.
- Prevention: enforce at storage/catalog/warehouse layer.

- Failure: Masking breaks joins.
- Symptom: users cannot join by masked identifier.
- Recovery: provide token/surrogate key.
- Prevention: design safe analytical keys.

## 12. Common Mistakes

- Mistake: Creating many manually stripped table copies.
- Why it is wrong: copies drift and are hard to govern.
- Better approach: central table plus column policies or curated marts.

- Mistake: Only hiding columns in dashboards.
- Why it is wrong: direct SQL may expose them.
- Better approach: enforce at data platform layer.

## 13. Mini Example

```text
SELECT customer_id, email
FROM customers;

general analyst:
customer_id=123, email=a***@example.com

pii_reader:
customer_id=123, email=alice@example.com
```

## 14. Interview Questions

1. What is column-level security?
2. How is it different from row-level security?
3. How does masking fit?
4. Why classify columns?
5. How can CLS be bypassed?

## 15. Interview Speak

"Column-level security controls access to sensitive fields within a table. I would tag PII/PHI columns, deny or mask them by default, grant full access only to approved roles, audit access, and ensure users cannot bypass controls through raw storage."

## 16. Quick Recall

- One-line summary: CLS protects sensitive columns.
- Three keywords: column, masking, classification.
- One trap: Dashboard-only hiding.
- One memory trick: Same table, fewer columns.
