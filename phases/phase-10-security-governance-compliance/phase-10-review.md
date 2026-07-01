# Phase 10 Review: Security, Governance, And Compliance

## 1. Phase Summary

Phase 10 explains how to protect data platforms and govern them responsibly.

The core idea:

```text
verify identity
  -> authorize least-privilege access
  -> classify sensitive data
  -> protect it with masking/tokenization/encryption
  -> audit access
  -> retain/delete by policy
  -> govern ownership, quality, and lineage at scale
```

If you remember only one sentence:

```text
Security and governance must be designed into every data layer, not patched onto dashboards at the end.
```

## 2. Identity And Access Basics

| Concept | Question Answered | Example |
|---|---|---|
| authentication | who are you? | SSO/MFA login |
| authorization | what can you do? | SELECT allowed on gold table |
| RBAC | what does your role allow? | finance_reader role |
| ABAC | what do attributes/context allow? | region and sensitivity tags |
| IAM | how are identities and permissions managed? | users, groups, roles, policies |

Strong memory:

```text
Authentication proves identity.
Authorization checks permission.
```

## 3. RBAC Vs ABAC

| Model | Best For | Watch Out |
|---|---|---|
| RBAC | job/team based access | role explosion or over-broad roles |
| ABAC | context/tag/sensitivity based access | bad metadata creates bad decisions |

Practical enterprise pattern:

```text
RBAC for broad team access
ABAC for sensitive/contextual controls
```

## 4. Sensitive Data

| Term | Meaning | Examples |
|---|---|---|
| PII | identifies or can identify a person | email, phone, SSN, IP, device ID |
| PHI | identifiable health information | diagnosis, claim, lab result linked to person |
| personal data | GDPR-style broad concept of person-related data | identifiers, online IDs, location data |

Core controls:

- classify
- minimize
- restrict
- mask/tokenize
- encrypt
- audit
- retain/delete by policy

## 5. GDPR Engineering View

GDPR means personal data handling needs:

- purpose
- minimization
- access control
- retention
- deletion/erasure workflow where applicable
- export/access workflow where applicable
- lineage
- vendor/processor awareness
- incident process

Engineering does not independently decide legal meaning. Engineering builds controls that privacy/legal policies require.

Official reference:

```text
https://commission.europa.eu/law/law-topic/data-protection/legal-framework-eu-data-protection_en
```

## 6. HIPAA Engineering View

HIPAA-oriented healthcare platforms need:

- PHI/ePHI classification
- minimum necessary access
- safeguards
- audit logs
- encryption/key controls
- vendor/business associate controls
- de-identified or limited analytics datasets where appropriate
- incident response

Official references:

```text
https://www.hhs.gov/hipaa/for-professionals/privacy/index.html
https://www.hhs.gov/hipaa/for-professionals/security/index.html
```

## 7. Protection Mechanisms

| Control | Meaning | Best Use |
|---|---|---|
| masking | hide part/all of value | BI/support views |
| tokenization | replace value with stable token | joins without raw identifier |
| encryption | make data unreadable without key | storage, transport, sensitive fields |
| key management | protect encryption keys | KMS/HSM, rotation, key policies |
| audit logs | record security events | investigations and compliance evidence |

Quick distinction:

```text
Masking hides display.
Tokenization replaces identity.
Encryption locks data.
Key management guards the lock key.
Audit logs prove what happened.
```

## 8. Data Lake Access

Data lake security must cover:

- object storage paths
- table/catalog permissions
- compute job identities
- row/column policies
- encryption keys
- network controls
- audit logs

Common trap:

```text
Securing the warehouse view but leaving raw object storage readable.
```

## 9. Fine-Grained Access

| Control | Protects | Example |
|---|---|---|
| row-level security | rows | manager sees only assigned region |
| column-level security | columns | analyst cannot see SSN/email |
| masking policy | values | show only last 4 digits |

Use platform-level enforcement where possible, not only dashboard filters.

## 10. Retention And Deletion

Data retention answers:

```text
How long should this data live?
```

Right to be forgotten style workflows answer:

```text
How do we find and remove/anonymize a person's data when policy requires it?
```

Deletion workflow needs:

- identity resolution
- lineage
- source and derived table handling
- logs/backups policy
- tombstone/suppression handling
- audit evidence

## 11. Governance At Scale

Governance building blocks:

- data catalog
- ownership
- classification
- lineage
- data quality
- access workflow
- retention policy
- audit logs
- certified data products
- policy automation

Strong line:

```text
Governance must be built into platform workflows, not managed by stale spreadsheets.
```

## 12. Security Design Checklist

For every production dataset:

- owner
- classification
- allowed users/groups
- allowed service accounts
- row/column policies
- masking/tokenization rules
- encryption/key policy
- audit log coverage
- retention policy
- deletion behavior
- lineage
- quality checks
- incident owner

## 13. Common Interview Questions

1. Authentication vs authorization?
2. RBAC vs ABAC?
3. What is IAM?
4. What is least privilege?
5. What is PII?
6. What is PHI?
7. How does GDPR affect data pipelines?
8. How does HIPAA affect healthcare data platforms?
9. Masking vs tokenization vs encryption?
10. What is key management?
11. What should audit logs capture?
12. How do you secure a data lake?
13. Row-level vs column-level security?
14. What is data retention?
15. How do you implement right to be forgotten?
16. What is governance at scale?

## 14. Strong System Design Answer

Question:

> Design a secure enterprise data lakehouse for customer analytics.

Strong answer:

"I would start by classifying data into raw, clean, and curated zones, with PII/PHI tags in the catalog. Humans would authenticate through SSO/MFA and jobs would use service accounts. Authorization would use least-privilege IAM, RBAC for team roles, and ABAC or tag-based policies for sensitive data.

Raw sensitive data would be highly restricted. Curated analytics tables would use tokenized identifiers, masking for sensitive columns, row-level security for region or tenant restrictions, and column-level security for PII. Data would be encrypted at rest and in transit, with KMS key policies limiting decrypt access.

I would enable audit logs for authentication, data access, policy changes, key usage, exports, and deletion jobs. Retention policies would apply by dataset class, and right-to-be-forgotten workflows would use identity mapping, lineage, tombstones/deletes, downstream recomputation, and audit evidence. At scale, governance needs owners, catalog metadata, lineage, quality checks, access reviews, and automated policy enforcement."

## 15. Hands-On Project

Build a mini secure data platform simulation:

1. Create sample customer records with email, region, and revenue.
2. Classify email as PII.
3. Create roles: analyst, pii_reader, admin.
4. Enforce authorization checks.
5. Mask email for normal analysts.
6. Tokenize email for analytics joins.
7. Apply row-level filter by region.
8. Apply retention policy by dataset type.
9. Emit audit log lines for access decisions.

What this teaches:

- authn/authz separation
- RBAC
- masking
- tokenization
- RLS/CLS
- retention
- auditability

## 16. Quick Revision Cards

| Prompt | Answer |
|---|---|
| Authentication | proves identity |
| Authorization | checks permission |
| RBAC | role-based access |
| ABAC | attribute/context-based access |
| IAM | identity and permission management |
| PII | personally identifiable information |
| PHI | identifiable health information |
| Masking | hides values |
| Tokenization | replaces values with tokens |
| Encryption | locks data with keys |
| KMS | manages encryption keys |
| Audit logs | evidence of who did what |
| RLS | restricts rows |
| CLS | restricts columns |
| Retention | how long data lives |
| Right to be forgotten | privacy-driven deletion workflow |
| Governance | owners, catalog, lineage, quality, policy |
