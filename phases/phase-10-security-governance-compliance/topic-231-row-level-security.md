# Topic 231: Row-Level Security

## 1. Goal

Understand row-level security as filtering rows based on user or context.

## 2. Baby Intuition

Row-level security means two users query the same table but see different rows.

Example: a regional manager sees only their region.

## 3. What It Is

- Simple definition: Row-level security restricts which rows a user can see.
- Technical definition: Row-level security applies policy-based filters to table rows at query time based on user identity, role, attributes, or context.
- Category: Fine-grained data access control.
- Related terms: RLS, policy, filter, tenant isolation, region restriction, ABAC.

## 4. Why It Exists

Sometimes users need the same table structure but different data slices:

- region managers see their region
- tenants see only their own tenant data
- analysts see permitted countries
- healthcare users see assigned facilities

Creating separate physical tables for every user/team does not scale.

## 5. Where It Fits In A Data Platform

```text
shared table
  -> row-level policy
  -> query returns only allowed rows
```

Common in warehouses, BI tools, data marts, and multi-tenant analytics.

## 6. How It Works Step By Step

1. User submits query.
2. System identifies user/role/attributes.
3. RLS policy determines allowed row filter.
4. System rewrites or applies filter to query.
5. User receives only matching rows.
6. Access is logged.

## 7. How To Use It Practically

Example policy idea:

```text
sales_manager can see rows where sales.region in user's assigned_regions
```

Common RLS use cases:

| Use Case | Policy |
|---|---|
| tenant isolation | tenant_id = current_user_tenant |
| regional access | region in user_regions |
| facility access | facility_id in allowed_facilities |
| data residency | country in allowed_countries |

## 8. Real-World Scenario

- Product/system: SaaS customer analytics.
- Problem: Each customer tenant should see only its own rows in shared analytics tables.
- How RLS helps: tenant_id filter is automatically applied for each tenant.
- What would go wrong without it: one tenant could see another tenant's data.

## 9. System Design Angle

Use RLS when:

- same table serves many users/tenants
- access differs by row attributes
- BI dashboards need user-specific filtering
- copying tables per user would be unmanageable

Be careful with:

- performance
- policy correctness
- bypass paths
- admin/service accounts
- aggregation leakage

## 10. Trade-offs

| Pros | Cons |
|---|---|
| fine-grained access | policy complexity |
| avoids table duplication | query performance overhead |
| good for tenant/region filters | bypass risk if raw table accessible |
| centralized policy | testing needed |

## 11. Failure Modes

- Failure: Missing tenant filter.
- Symptom: cross-tenant data leak.
- Recovery: incident response and policy fix.
- Prevention: default deny and automated tests.

- Failure: RLS only in BI tool.
- Symptom: users query warehouse directly and bypass filter.
- Recovery: enforce at warehouse/table layer.
- Prevention: defense in depth.

- Failure: Aggregation leakage.
- Symptom: user infers restricted rows from totals.
- Recovery: minimum thresholds/suppression.
- Prevention: privacy-aware aggregate design.

## 12. Common Mistakes

- Mistake: Relying only on application filters.
- Why it is wrong: direct queries or bugs can bypass them.
- Better approach: enforce RLS in the data platform where possible.

- Mistake: Not testing policies.
- Why it is wrong: one bad condition can expose data.
- Better approach: test allowed and denied cases.

## 13. Mini Example

```text
Table: sales
Rows:
region=US, revenue=100
region=EU, revenue=80

User assigned region=US
Query result:
only US row
```

## 14. Interview Questions

1. What is row-level security?
2. Where is RLS useful?
3. How can RLS be bypassed?
4. RLS vs column-level security?
5. What is tenant isolation?

## 15. Interview Speak

"Row-level security applies policy filters so users see only allowed rows from a shared table. I would use it for tenant, region, facility, or data residency restrictions, enforce it at the data platform layer, and test policies to avoid leakage."

## 16. Quick Recall

- One-line summary: RLS filters rows by user/context.
- Three keywords: row filter, tenant, region.
- One trap: Enforcing only in BI/application layer.
- One memory trick: Same table, different rows.
