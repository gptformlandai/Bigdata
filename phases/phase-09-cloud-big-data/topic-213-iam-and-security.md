# Topic 213: IAM And Security

## 1. Goal

Understand IAM and security as the foundation of cloud data platform access control.

## 2. Baby Intuition

IAM is the cloud's permission system.

It answers: who can do what on which resource?

## 3. What It Is

- Simple definition: IAM controls identities and permissions in cloud systems.
- Technical definition: Identity and Access Management defines users, groups, roles, service accounts, policies, and permissions that control access to cloud resources and actions.
- Category: Cloud security and access control.
- Related terms: role, policy, principal, service account, least privilege, RBAC, resource policy, secrets.

## 4. Why It Exists

Data platforms contain sensitive data:

- customer PII
- financial records
- health data
- credentials
- business metrics
- production systems

IAM exists to prevent unauthorized access and limit damage when something goes wrong.

## 5. Where It Fits In A Data Platform

```text
users/services/jobs
  -> IAM identities and roles
  -> storage, streams, warehouses, compute, keys
```

Every cloud data service depends on correct IAM.

## 6. How It Works Step By Step

1. Define identities: users, groups, roles, service accounts.
2. Define resources: buckets, databases, streams, clusters, keys.
3. Assign permissions through policies/roles.
4. Jobs assume roles or use service accounts.
5. Cloud evaluates request.
6. Access is allowed or denied.
7. Audit logs record important actions.

## 7. How To Use It Practically

Principles:

- least privilege
- separate dev/stage/prod access
- use service accounts/roles for jobs
- avoid hardcoded credentials
- rotate secrets/keys
- audit access
- restrict sensitive data
- use groups instead of individual grants where possible

Example:

```text
Airflow job role:
read raw S3/ADLS/GCS path
write curated path
start Spark job
cannot delete whole bucket
```

## 8. Real-World Scenario

- Product/system: Data lake with PII.
- Problem: Only approved pipelines and analysts should access customer email data.
- How IAM helps: roles restrict bucket/table/key access; audit logs track usage.
- What would go wrong without it: broad permissions expose sensitive data.

## 9. System Design Angle

Mention IAM when:

- cloud data platform is discussed
- services need to access storage/warehouse
- PII/security matters
- cross-account/project/subscription access exists
- data lake zones require different access

Strong phrase:

```text
Default deny, least privilege, audited access.
```

## 10. Trade-offs

| Strict IAM | Loose IAM |
|---|---|
| safer | faster initial development |
| less blast radius | fewer permission tickets |
| better audit/compliance | higher risk |
| harder setup | easier but dangerous |

## 11. Failure Modes

- Failure: Overly broad role.
- Symptom: job/user can access too much data.
- Recovery: reduce permissions.
- Prevention: least privilege and reviews.

- Failure: Missing permission.
- Symptom: pipeline fails access denied.
- Recovery: grant required action only.
- Prevention: pre-prod access tests.

- Failure: Hardcoded secret leaked.
- Symptom: credential compromise.
- Recovery: rotate secret and investigate.
- Prevention: secret managers and no plaintext credentials.

## 12. Common Mistakes

- Mistake: Giving admin permissions to pipeline jobs.
- Why it is wrong: one bug can damage many resources.
- Better approach: service-specific least privilege roles.

- Mistake: Sharing human credentials with jobs.
- Why it is wrong: audit and rotation become unsafe.
- Better approach: service accounts/roles.

## 13. Mini Example

```text
Role: glue-orders-etl-role
Allow:
  read s3://lake/bronze/orders/
  write s3://lake/silver/orders/
Deny:
  delete bucket
  read pii/raw/customers/
```

## 14. Interview Questions

1. What is IAM?
2. What is least privilege?
3. Human user vs service account/role?
4. How do you secure data lake access?
5. Why are audit logs important?

## 15. Interview Speak

"IAM controls who or what can perform actions on cloud resources. For data platforms, I would use least privilege roles/service accounts for jobs, separate access by environment and data zone, avoid hardcoded credentials, audit access, and restrict sensitive datasets with clear ownership."

## 16. Quick Recall

- One-line summary: IAM controls cloud identities and permissions.
- Three keywords: role, policy, least privilege.
- One trap: Admin roles for pipeline jobs.
- One memory trick: Who can do what where?
