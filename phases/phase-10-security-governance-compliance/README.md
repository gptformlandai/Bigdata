# Phase 10: Security, Governance, And Compliance

Phase 10 teaches how to protect data platforms and operate them responsibly.

The mental model is:

```text
identify the user/service
  -> decide what they can access
  -> protect sensitive data
  -> log what happened
  -> retain/delete data according to policy
  -> govern access and usage at scale
```

Security is not a feature added at the end. In Big Data systems, it affects storage, pipelines, warehouses, lakehouses, streaming, BI, ML, and incident response.

## Topics

| # | Topic | Status |
|---:|---|---|
| 216 | Authentication | Complete |
| 217 | Authorization | Complete |
| 218 | RBAC | Complete |
| 219 | ABAC | Complete |
| 220 | IAM | Complete |
| 221 | PII | Complete |
| 222 | PHI | Complete |
| 223 | GDPR | Complete |
| 224 | HIPAA | Complete |
| 225 | Data masking | Complete |
| 226 | Tokenization | Complete |
| 227 | Encryption | Complete |
| 228 | Key management | Complete |
| 229 | Audit logs | Complete |
| 230 | Access control in data lakes | Complete |
| 231 | Row-level security | Complete |
| 232 | Column-level security | Complete |
| 233 | Data retention | Complete |
| 234 | Right to be forgotten | Complete |
| 235 | Governance at scale | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- authentication vs authorization
- RBAC vs ABAC
- IAM roles, policies, users, groups, and service accounts
- PII and PHI handling in data systems
- GDPR and HIPAA from an engineering point of view
- masking, tokenization, encryption, and key management
- audit logs and access control for lakes, warehouses, and BI
- row-level and column-level security
- retention, deletion, and right-to-be-forgotten workflows
- how governance scales across many teams and datasets

## Suggested Study Flow

1. Read Topics 216-220 for identity and access basics.
2. Read Topics 221-224 for sensitive data and compliance context.
3. Read Topics 225-229 for protection and audit mechanisms.
4. Read Topics 230-232 for fine-grained data access controls.
5. Read Topics 233-235 for retention, deletion, and governance at scale.
6. Finish with `phase-10-review.md`.
