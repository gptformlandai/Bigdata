# Topic 220: IAM

## 1. Goal

Understand IAM as the broader system for managing identities and access.

## 2. Baby Intuition

IAM is the security office of a data platform.

It manages users, service accounts, roles, policies, permissions, and access reviews.

## 3. What It Is

- Simple definition: IAM manages identities and access permissions.
- Technical definition: Identity and Access Management is the framework of identities, roles, policies, groups, credentials, and governance processes used to control access to systems and data.
- Category: Identity and access management.
- Related terms: authentication, authorization, RBAC, ABAC, service account, policy, least privilege, audit.

## 4. Why It Exists

Data platforms have many actors:

- analysts
- data engineers
- ML jobs
- Airflow tasks
- BI tools
- Spark clusters
- external partners
- admins

IAM makes access manageable and auditable across these actors.

## 5. Where It Fits In A Data Platform

```text
identity provider / cloud IAM / warehouse grants / lake policies
  -> controls access to storage, compute, tables, streams, keys, dashboards
```

IAM spans cloud, warehouse, lakehouse, orchestration, and BI tools.

## 6. How It Works Step By Step

1. Create or federate identities.
2. Group users by team/function.
3. Create roles or policies.
4. Assign permissions to roles/policies.
5. Assign roles to users/groups/services.
6. Enforce access at resources.
7. Log access events.
8. Review and revoke access periodically.

## 7. How To Use It Practically

IAM checklist:

- SSO for humans
- MFA for privileged users
- service accounts for jobs
- least-privilege policies
- separate dev/stage/prod access
- access request workflow
- periodic access review
- audit logs
- secret/key management
- break-glass admin process

## 8. Real-World Scenario

- Product/system: Enterprise data platform.
- Problem: Hundreds of users and jobs need different access to S3/ADLS/GCS, warehouses, and BI dashboards.
- How IAM helps: roles, groups, policies, and service accounts organize access consistently.
- What would go wrong without it: direct grants and shared credentials become unmanageable.

## 9. System Design Angle

Mention IAM when designing:

- cloud data lake
- warehouse security
- pipeline service accounts
- partner access
- PII access
- encryption key access
- audit/compliance system

Strong phrase:

```text
IAM should follow least privilege, separation of duties, and auditable access.
```

## 10. Trade-offs

| Strong IAM Governance | Trade-off |
|---|---|
| safer access | more process |
| audit-ready | more setup |
| easier offboarding | needs automation |
| lower blast radius | access requests may take longer |

## 11. Failure Modes

- Failure: Orphaned service account.
- Symptom: unused identity still has access.
- Recovery: revoke/delete.
- Prevention: identity inventory and reviews.

- Failure: Privilege creep.
- Symptom: users accumulate access over time.
- Recovery: access recertification.
- Prevention: time-bound access.

- Failure: No break-glass process.
- Symptom: emergency access is chaotic.
- Recovery: create emergency role and audit.
- Prevention: tested break-glass workflow.

## 12. Common Mistakes

- Mistake: Managing access only inside one tool.
- Why it is wrong: data access spans cloud storage, warehouse, BI, and pipelines.
- Better approach: design IAM end-to-end.

- Mistake: Never reviewing access after granting it.
- Why it is wrong: people change teams and old access remains.
- Better approach: periodic access reviews and automatic offboarding.

## 13. Mini Example

```text
Human analyst:
SSO group -> warehouse reader role -> SELECT gold metrics

Pipeline job:
service account -> storage read raw/write silver -> no admin permissions
```

## 14. Interview Questions

1. What is IAM?
2. How is IAM different from RBAC?
3. Why use service accounts?
4. What is least privilege?
5. How do access reviews work?

## 15. Interview Speak

"IAM is the end-to-end system for managing identities, roles, policies, credentials, and access reviews. In data platforms, IAM must cover humans and services across cloud storage, compute, warehouses, keys, and BI, with least privilege and auditability."

## 16. Quick Recall

- One-line summary: IAM manages identities and permissions across the platform.
- Three keywords: identity, policy, least privilege.
- One trap: Access granted forever.
- One memory trick: Security office for data access.
