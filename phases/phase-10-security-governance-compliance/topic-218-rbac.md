# Topic 218: RBAC

## 1. Goal

Understand role-based access control as a common way to manage permissions.

## 2. Baby Intuition

RBAC is like job titles with permissions.

A cashier, manager, and auditor have different access because their roles are different.

## 3. What It Is

- Simple definition: RBAC grants permissions through roles.
- Technical definition: Role-based access control assigns permissions to roles and assigns users or service identities to those roles.
- Category: Access control model.
- Related terms: role, group, permission, grant, least privilege, IAM.

## 4. Why It Exists

Managing permissions user-by-user does not scale.

RBAC simplifies access:

```text
permissions -> role -> users/groups
```

Instead of granting table access to 500 analysts one by one, grant it to an `analytics_reader` role.

## 5. Where It Fits In A Data Platform

```text
user/service
  -> assigned role
  -> role has permissions
  -> data access allowed/denied
```

Examples:

- `data_engineer`
- `finance_analyst`
- `pii_approved_reader`
- `etl_writer`
- `warehouse_admin`

## 6. How It Works Step By Step

1. Define job/access roles.
2. Attach permissions to roles.
3. Assign users/groups/services to roles.
4. User requests a resource.
5. System checks user's roles.
6. If a role has required permission, access is allowed.
7. Access is logged.

## 7. How To Use It Practically

Example roles:

| Role | Permissions |
|---|---|
| raw_reader | read raw non-sensitive data |
| pii_reader | read approved PII tables/columns |
| etl_writer | write curated tables |
| dashboard_reader | read gold marts |
| admin | manage grants and policies |

Good practices:

- assign roles to groups, not individuals
- keep roles small and meaningful
- avoid giant admin-like roles
- review role membership
- separate read/write/admin

## 8. Real-World Scenario

- Product/system: Data warehouse access.
- Problem: Finance users need revenue tables, product users need product metrics, and only compliance-approved users need PII.
- How RBAC helps: users join appropriate groups mapped to roles.
- What would go wrong without it: grants become one-off and impossible to audit.

## 9. System Design Angle

Use RBAC when:

- access aligns with job function
- many users need similar permissions
- role review is required
- warehouse/lake permissions need scale

Watch for:

- role explosion
- roles too broad
- stale memberships
- exceptions outside standard roles

## 10. Trade-offs

| Pros | Cons |
|---|---|
| simple mental model | can be too coarse |
| easy to audit roles | role explosion possible |
| scales better than user grants | exceptions can get messy |
| works well with teams | context-aware rules may need ABAC |

## 11. Failure Modes

- Failure: Role too broad.
- Symptom: users get unnecessary access.
- Recovery: split role.
- Prevention: least-privilege role design.

- Failure: Role explosion.
- Symptom: hundreds of confusing roles.
- Recovery: consolidate and standardize.
- Prevention: naming and role design review.

- Failure: Stale group membership.
- Symptom: former team member retains access.
- Recovery: remove user.
- Prevention: automated offboarding and access reviews.

## 12. Common Mistakes

- Mistake: One role called `data_admin` for everyone.
- Why it is wrong: it destroys least privilege.
- Better approach: separate reader, writer, steward, and admin roles.

- Mistake: Creating roles for every tiny exception.
- Why it is wrong: role management becomes impossible.
- Better approach: use standard roles plus approval workflow or ABAC for context.

## 13. Mini Example

```text
Role: finance_reader
Permissions:
  SELECT gold.revenue
  SELECT gold.invoice_summary

Members:
  finance_analysts_group
```

## 14. Interview Questions

1. What is RBAC?
2. Why use roles instead of direct user grants?
3. What is role explosion?
4. RBAC vs ABAC?
5. How do you review RBAC access?

## 15. Interview Speak

"RBAC manages access by assigning permissions to roles and users/groups to those roles. It scales better than direct grants and is easy to audit, but roles must be designed carefully to avoid over-broad access or role explosion."

## 16. Quick Recall

- One-line summary: RBAC gives permissions through roles.
- Three keywords: role, group, permission.
- One trap: Giant roles with too much access.
- One memory trick: Job title controls doors.
