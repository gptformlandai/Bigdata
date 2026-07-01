# Topic 217: Authorization

## 1. Goal

Understand authorization as deciding what an authenticated identity is allowed to do.

## 2. Baby Intuition

Authentication asks:

```text
Who are you?
```

Authorization asks:

```text
What are you allowed to do?
```

Having an office badge does not mean you can enter every room.

## 3. What It Is

- Simple definition: Authorization decides permissions.
- Technical definition: Authorization evaluates policies, roles, attributes, ownership, or rules to determine whether an authenticated principal can perform an action on a resource.
- Category: Access control.
- Related terms: permission, policy, role, RBAC, ABAC, ACL, row-level security, column-level security.

## 4. Why It Exists

Different identities need different access:

- finance analysts can see revenue
- marketing analysts can see campaign aggregates
- engineers can operate pipelines
- service jobs can write curated tables
- only approved roles can see raw PII

Without authorization, every authenticated user could access everything.

## 5. Where It Fits In A Data Platform

```text
authenticated identity
  -> authorization policy check
  -> allow or deny action
```

Examples:

- Can this user read table `customers`?
- Can this job write to `silver/orders`?
- Can this analyst see column `ssn`?
- Can this manager see rows for all regions?

## 6. How It Works Step By Step

1. Request arrives with authenticated identity.
2. System identifies resource and action.
3. Authorization engine loads policies.
4. Policies evaluate identity, role, attributes, tags, or context.
5. System allows or denies the request.
6. Access decision is logged.

Access request:

```text
principal=analyst_a
action=SELECT
resource=gold.revenue
context=production
```

## 7. How To Use It Practically

Common authorization layers:

| Layer | Example |
|---|---|
| storage | bucket/path read/write |
| table | SELECT on warehouse table |
| column | mask or block email column |
| row | only show region=US rows |
| job | allow service account to start ETL |
| admin | manage grants/policies |

Good practices:

- least privilege
- deny by default
- role/group-based access
- periodic access reviews
- separate read and write permissions
- log access decisions

## 8. Real-World Scenario

- Product/system: Enterprise warehouse.
- Problem: Finance can see payroll data, but product analysts should not.
- How authorization helps: table/column policies restrict payroll tables to approved finance roles.
- What would go wrong without it: sensitive data leaks internally.

## 9. System Design Angle

Mention authorization when:

- users consume BI/warehouse/lake data
- sensitive datasets exist
- service accounts access storage
- data sharing is discussed
- compliance/audit is important

Clarify:

- who needs access
- what actions are allowed
- what data is sensitive
- how access is approved
- how access is audited/revoked

## 10. Trade-offs

| Strict Authorization | Trade-off |
|---|---|
| lower data exposure | more access requests |
| better compliance | more policy management |
| smaller blast radius | can slow exploration |
| clearer accountability | requires ownership metadata |

## 11. Failure Modes

- Failure: Over-permissive role.
- Symptom: user sees data beyond need.
- Recovery: reduce grants.
- Prevention: least privilege and reviews.

- Failure: Missing access.
- Symptom: pipeline/user blocked.
- Recovery: grant required minimal permission.
- Prevention: access testing in lower environments.

- Failure: Permission drift.
- Symptom: old users retain access.
- Recovery: revoke stale grants.
- Prevention: periodic access reviews.

## 12. Common Mistakes

- Mistake: Granting access directly to every user.
- Why it is wrong: hard to manage at scale.
- Better approach: use groups/roles and automate approvals.

- Mistake: Granting write access when read is enough.
- Why it is wrong: increases damage from mistakes.
- Better approach: separate read, write, admin permissions.

## 13. Mini Example

```text
User: product_analyst
Allowed:
  SELECT gold.product_metrics
Denied:
  SELECT raw.customer_pii
  DELETE gold.product_metrics
```

## 14. Interview Questions

1. What is authorization?
2. Authentication vs authorization?
3. What is least privilege?
4. How do you authorize table/column access?
5. How do you review permissions?

## 15. Interview Speak

"Authorization decides what an authenticated identity can do. In data systems, I would enforce least privilege across storage, tables, columns, rows, jobs, and admin actions, using roles or policies, periodic reviews, and audit logs."

## 16. Quick Recall

- One-line summary: Authorization decides what you can access or change.
- Three keywords: permission, policy, least privilege.
- One trap: Authenticated does not mean authorized.
- One memory trick: Badge does not open every door.
