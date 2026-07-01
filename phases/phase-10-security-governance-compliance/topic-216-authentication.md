# Topic 216: Authentication

## 1. Goal

Understand authentication as proving identity before access is allowed.

## 2. Baby Intuition

Authentication asks:

```text
Who are you?
```

It is like showing your ID badge before entering an office.

## 3. What It Is

- Simple definition: Authentication verifies identity.
- Technical definition: Authentication is the process of validating that a user, service, application, or workload is who it claims to be.
- Category: Identity security.
- Related terms: password, MFA, SSO, OAuth, OIDC, SAML, service account, token, certificate.

## 4. Why It Exists

Data systems contain sensitive and valuable data.

Before allowing access, the platform must know:

- which human is connecting
- which service/job is running
- whether the credential is valid
- whether the request is coming from a trusted identity provider

Without authentication, anyone could claim to be anyone.

## 5. Where It Fits In A Data Platform

```text
user/service tries to access data platform
  -> authentication verifies identity
  -> authorization checks allowed actions
  -> access granted or denied
```

Authentication comes before authorization.

## 6. How It Works Step By Step

1. User or service presents a credential.
2. Identity system validates the credential.
3. Identity system may require MFA or certificate proof.
4. A session, token, or principal identity is created.
5. Downstream systems use that identity for authorization checks.
6. Logs record the identity and access event.

Common credentials:

| Credential | Example |
|---|---|
| password | user login |
| MFA | password plus one-time code/device |
| token | OAuth/OIDC access token |
| certificate | mutual TLS/service identity |
| key | API key or service credential |

## 7. How To Use It Practically

Good practices:

- use SSO for human users
- require MFA for sensitive access
- use service accounts or workload identities for jobs
- avoid shared user accounts
- rotate credentials
- avoid hardcoded secrets
- log authentication events

For pipelines:

```text
Airflow/Spark/dbt job should authenticate as a service identity,
not as a human engineer's personal account.
```

## 8. Real-World Scenario

- Product/system: Cloud data lake.
- Problem: Spark jobs and analysts access sensitive tables.
- How authentication helps: humans authenticate via SSO/MFA; jobs authenticate with service accounts.
- What would go wrong without it: audit logs cannot reliably say who accessed data.

## 9. System Design Angle

Mention authentication when:

- users access dashboards/warehouses
- services access storage
- APIs expose data
- auditability matters
- zero-trust/security architecture is discussed

Clarify:

- human vs service identity
- MFA requirement
- token lifetime
- credential rotation
- identity provider integration

## 10. Trade-offs

| Stronger Authentication | Trade-off |
|---|---|
| MFA | small user friction |
| short token lifetime | more refresh complexity |
| certificates/workload identity | setup complexity |
| no shared accounts | more identity management |

## 11. Failure Modes

- Failure: Shared account.
- Symptom: cannot tell who did what.
- Recovery: migrate to named identities.
- Prevention: ban shared logins.

- Failure: Hardcoded credential leaks.
- Symptom: unauthorized access risk.
- Recovery: revoke/rotate credential.
- Prevention: secret manager and scanning.

- Failure: No MFA for admin users.
- Symptom: stolen password gives broad access.
- Recovery: enable MFA.
- Prevention: enforce MFA policy.

## 12. Common Mistakes

- Mistake: Confusing authentication with authorization.
- Why it is wrong: proving identity does not mean access should be allowed.
- Better approach: authenticate first, authorize second.

- Mistake: Using human credentials in production jobs.
- Why it is wrong: job breaks when user leaves/rotates password and audit is unclear.
- Better approach: use service identities.

## 13. Mini Example

```text
Analyst logs into warehouse:
1. SSO verifies analyst identity.
2. MFA confirms login.
3. Warehouse receives analyst principal.
4. Authorization decides which tables are visible.
```

## 14. Interview Questions

1. What is authentication?
2. Authentication vs authorization?
3. Why use MFA?
4. Why avoid shared accounts?
5. How should pipelines authenticate?

## 15. Interview Speak

"Authentication verifies identity. In a data platform, humans should authenticate through SSO/MFA, while pipelines should use service accounts or workload identities. Authentication tells us who is calling; authorization decides what that identity can do."

## 16. Quick Recall

- One-line summary: Authentication proves who you are.
- Three keywords: identity, credential, MFA.
- One trap: Shared production accounts.
- One memory trick: Show ID before entering.
