# Topic 219: ABAC

## 1. Goal

Understand attribute-based access control as a flexible policy model.

## 2. Baby Intuition

ABAC decides access using labels and context.

It is like saying: "Allow access if the user is in Finance, the dataset is tagged Finance, the region matches, and the request is from a trusted network."

## 3. What It Is

- Simple definition: ABAC grants access based on attributes.
- Technical definition: Attribute-based access control evaluates policies using attributes of the subject, resource, action, and environment to allow or deny access.
- Category: Access control model.
- Related terms: attribute, tag, policy, subject, resource, environment, context, data classification.

## 4. Why It Exists

RBAC can become too rigid when access depends on context:

- user region must match data region
- dataset sensitivity tag controls access
- environment is dev vs prod
- data owner approval is required
- request comes from corporate network
- purpose is allowed

ABAC handles these dynamic conditions better.

## 5. Where It Fits In A Data Platform

```text
request:
  subject attributes: department=finance, clearance=pii
  resource attributes: domain=finance, sensitivity=pii
  action: read
  environment: production, trusted_network=true

policy evaluates attributes -> allow/deny
```

## 6. How It Works Step By Step

1. Assign attributes/tags to users, services, datasets, and environments.
2. Write policies based on attributes.
3. Request arrives.
4. Policy engine reads attributes.
5. Policy evaluates action/resource/context.
6. Access is allowed or denied.
7. Decision is logged.

## 7. How To Use It Practically

Useful attributes:

| Attribute Type | Example |
|---|---|
| user | department, region, clearance |
| service | app, environment, owner |
| data | sensitivity, domain, country |
| action | read, write, delete |
| context | time, network, device, environment |

Example policy:

```text
Allow read if:
user.department == data.domain
and user.clearance includes data.sensitivity
and environment == production
```

## 8. Real-World Scenario

- Product/system: Global customer analytics platform.
- Problem: EU analysts can see EU customer data but not US customer PII unless approved.
- How ABAC helps: policies use user region, data region, and sensitivity tags.
- What would go wrong with only RBAC: many region-specific roles can explode.

## 9. System Design Angle

Use ABAC when:

- data has rich classification tags
- access depends on region, sensitivity, purpose, or environment
- RBAC roles are exploding
- policy needs dynamic context

Be careful with:

- attribute correctness
- policy complexity
- debugging decisions
- tag governance

## 10. Trade-offs

| Pros | Cons |
|---|---|
| flexible and context-aware | policies can be complex |
| reduces role explosion | needs reliable tags/attributes |
| good for sensitive data | harder to debug than simple RBAC |
| supports dynamic rules | governance of metadata is critical |

## 11. Failure Modes

- Failure: Wrong data classification tag.
- Symptom: access too open or too restricted.
- Recovery: fix tag and audit access.
- Prevention: metadata quality controls.

- Failure: Policy too complex.
- Symptom: users cannot predict access.
- Recovery: simplify and document.
- Prevention: policy design review.

- Failure: Missing attribute.
- Symptom: default deny or unsafe fallback.
- Recovery: populate attribute.
- Prevention: required metadata checks.

## 12. Common Mistakes

- Mistake: Using ABAC without trusted metadata.
- Why it is wrong: policy decisions depend on attributes.
- Better approach: govern tags and attributes like production data.

- Mistake: Replacing every RBAC role with ABAC immediately.
- Why it is wrong: simple role access is often enough.
- Better approach: combine RBAC for broad access and ABAC for sensitive/contextual rules.

## 13. Mini Example

```text
User:
department=finance
region=EU
clearance=pii

Dataset:
domain=finance
region=EU
sensitivity=pii

Decision:
allow read
```

## 14. Interview Questions

1. What is ABAC?
2. RBAC vs ABAC?
3. What attributes can be used?
4. Why does metadata quality matter?
5. When is ABAC useful?

## 15. Interview Speak

"ABAC evaluates access using attributes of the user, resource, action, and context. It is useful when access depends on data sensitivity, region, purpose, or environment, but it requires reliable metadata and careful policy design."

## 16. Quick Recall

- One-line summary: ABAC grants access using attributes and context.
- Three keywords: attributes, tags, policy.
- One trap: Bad tags create bad access decisions.
- One memory trick: Labels decide doors.
