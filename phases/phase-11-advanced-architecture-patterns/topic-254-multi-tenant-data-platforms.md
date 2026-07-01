# Topic 254: Multi-Tenant Data Platforms

## 1. Goal

Understand how one data platform can serve many customers, teams, or business units safely.

## 2. Baby Intuition

A multi-tenant platform is like an apartment building.

Many tenants share the same building services, but each tenant needs privacy, fair resource usage, and safety from neighbors.

## 3. What It Is

- Simple definition: A multi-tenant data platform serves multiple tenants on shared infrastructure.
- Technical definition: A multi-tenant data platform provides shared ingestion, storage, processing, governance, and serving capabilities while isolating tenant data, access, compute, quotas, cost, and operations.
- Category: Platform architecture pattern.
- Related terms: tenant, isolation, namespace, quota, noisy neighbor, cost attribution, shared service, dedicated tenant.

## 4. Why It Exists

Companies do not want to build a separate data platform for every team or customer.

Shared platforms provide:

- lower cost
- standard tooling
- shared governance
- easier operations
- faster onboarding

But sharing creates risk:

- one tenant can overload others
- data can leak across tenants
- costs become unclear
- custom needs can complicate the platform

## 5. Where It Fits In A Data Platform

```text
many tenants
  -> shared ingestion APIs
  -> tenant-aware storage/catalog
  -> isolated compute or quotas
  -> tenant-scoped governance
  -> dashboards, APIs, exports
```

Tenant can mean:

- external SaaS customer
- internal product team
- business unit
- region
- environment

## 6. How It Works Step By Step

1. Each tenant gets an ID, namespace, and ownership metadata.
2. Ingestion tags data with tenant_id.
3. Storage separates data by tenant or enforces row-level isolation.
4. Catalog registers tenant datasets.
5. Access policies restrict users/services to allowed tenants.
6. Compute uses quotas, pools, or dedicated clusters.
7. Monitoring tracks tenant usage and cost.
8. Operations handle onboarding, offboarding, deletion, and incident response.

## 7. How To Use It Practically

Isolation models:

| Model | Meaning | Best For |
|---|---|---|
| shared everything | same tables/clusters, tenant_id filter | low cost, small tenants |
| shared storage, isolated compute | same lake, separate warehouses/clusters | balanced cost/isolation |
| dedicated tenant | separate storage and compute | high-risk or large customers |

Controls to include:

- tenant-aware auth
- row/column policies
- separate encryption keys when required
- quotas and rate limits
- per-tenant monitoring
- per-tenant cost allocation
- tenant deletion workflow

## 8. Real-World Scenario

- Product/system: SaaS analytics platform.
- Problem: Thousands of customers use the same reporting product.
- How multi-tenancy helps: shared pipelines and warehouse reduce cost while tenant_id, access policies, and quotas isolate data and resources.
- What would go wrong without it: either cost explodes with dedicated stacks or customers risk seeing each other's data.

## 9. System Design Angle

Interviewers look for:

- data isolation
- access control
- compute isolation
- noisy neighbor protection
- per-tenant scaling
- cost attribution
- tenant lifecycle
- compliance and deletion

Strong rule:

```text
Never rely only on application filters for tenant security.
```

Use platform-level enforcement when possible.

## 10. Trade-offs

| Pros | Cons |
|---|---|
| lower shared cost | isolation complexity |
| faster tenant onboarding | noisy neighbor risk |
| standard governance | custom tenant needs are harder |
| centralized operations | data leak impact is severe |

## 11. Failure Modes

- Failure: Tenant isolation bug.
- Symptom: one tenant can access another tenant's data.
- Recovery: revoke access, fix policy, audit exposure.
- Prevention: platform-level policies and automated tests.

- Failure: Noisy neighbor.
- Symptom: one tenant's workload slows others.
- Recovery: throttle or move tenant to isolated compute.
- Prevention: quotas and workload isolation.

- Failure: Tenant deletion incomplete.
- Symptom: deleted customer data remains in derived tables.
- Recovery: run deletion across lineage.
- Prevention: tenant-aware lineage and retention policy.

## 12. Common Mistakes

- Mistake: Using tenant_id only in dashboard filters.
- Why it is wrong: direct queries can bypass the dashboard.
- Better approach: enforce row-level policies in storage/query layer.

- Mistake: No per-tenant cost tracking.
- Why it is wrong: heavy tenants hide in shared bills.
- Better approach: tag resources and meter tenant usage.

## 13. Mini Example

```text
orders table:
tenant_id | order_id | amount
acme      | 1        | 100
beta      | 2        | 80

Policy:
user from acme can only read tenant_id='acme'
```

## 14. Interview Questions

1. What is multi-tenancy?
2. How do you isolate tenant data?
3. What is noisy neighbor risk?
4. Shared vs dedicated tenant architecture?
5. How do you track per-tenant cost?

## 15. Interview Speak

"A multi-tenant data platform shares platform services across tenants while enforcing tenant isolation for data, access, compute, quotas, and cost. I would design tenant-aware ingestion, storage policies, catalog metadata, workload isolation, monitoring, and lifecycle workflows like onboarding and deletion."

## 16. Quick Recall

- One-line summary: Multi-tenant platforms share infrastructure while isolating tenants.
- Three keywords: isolation, quota, tenant_id.
- One trap: dashboard-only tenant filtering.
- One memory trick: Apartment building for data.

