# Topic 222: PHI

## 1. Goal

Understand protected health information and why healthcare data needs stronger controls.

## 2. Baby Intuition

PHI is health-related personal data.

If a medical record, diagnosis, claim, prescription, or appointment can be linked to a person, it is highly sensitive.

## 3. What It Is

- Simple definition: PHI is identifiable health information.
- Technical definition: PHI is individually identifiable health information handled by covered entities or business associates in healthcare contexts, especially under HIPAA in the United States.
- Category: Sensitive regulated data.
- Related terms: HIPAA, ePHI, covered entity, business associate, de-identification, minimum necessary, audit.

## 4. Why It Exists

Health data is deeply sensitive.

Exposure can harm people through:

- privacy invasion
- discrimination
- financial/insurance harm
- embarrassment
- identity theft

PHI handling requires strict privacy, security, access, audit, and retention controls.

## 5. Where It Fits In A Data Platform

```text
healthcare source systems
  -> PHI classification
  -> restricted raw zones
  -> de-identified/limited analytics datasets
  -> audited access and compliance controls
```

## 6. How It Works Step By Step

1. Identify whether data is health-related and individually identifiable.
2. Classify PHI/ePHI.
3. Limit access to approved users/jobs.
4. Apply minimum necessary principle.
5. Mask, tokenize, or de-identify where possible.
6. Encrypt and manage keys.
7. Log and audit access.
8. Retain/delete according to policy and legal requirements.

## 7. How To Use It Practically

PHI examples:

| Data | Example |
|---|---|
| identity | patient name, member ID |
| clinical | diagnosis, lab result, medication |
| claims | procedure code, claim amount |
| care events | appointment, admission, discharge |
| identifiers | address, phone, email linked to health record |

Practical controls:

- strict role-based access
- column masking
- row-level restrictions by business need
- de-identification for analytics
- audit logs
- encryption
- business associate/vendor controls

## 8. Real-World Scenario

- Product/system: Healthcare claims lake.
- Problem: Data scientists need cost trends but not patient-identifying details.
- How PHI handling helps: de-identified or tokenized datasets support analytics while raw PHI stays restricted.
- What would go wrong without it: broad access to claims could expose member health details.

## 9. System Design Angle

Mention PHI when:

- healthcare, insurance, claims, clinical, or patient data appears
- HIPAA or ePHI is discussed
- vendors/partners process health data
- de-identification is required
- audit and access controls are strict

Design:

```text
separate raw PHI, use minimum necessary access, create safer analytics datasets
```

## 10. Trade-offs

| Control | Trade-off |
|---|---|
| de-identification | less granular analysis |
| strict access | slower onboarding |
| audit logging | log storage/review effort |
| tokenization | token mapping complexity |
| data minimization | fewer exploratory options |

## 11. Failure Modes

- Failure: PHI lands in general analytics table.
- Symptom: too many users can access sensitive health data.
- Recovery: restrict/delete/remediate and investigate.
- Prevention: classification and pipeline gates.

- Failure: Re-identification risk ignored.
- Symptom: "de-identified" data can be linked back to people.
- Recovery: privacy review.
- Prevention: careful de-identification and risk assessment.

- Failure: Access not audited.
- Symptom: cannot investigate misuse.
- Recovery: enable audit logs.
- Prevention: audit-by-default for PHI.

## 12. Common Mistakes

- Mistake: Treating PHI like ordinary PII.
- Why it is wrong: health context and regulation make it more sensitive.
- Better approach: apply stricter healthcare controls.

- Mistake: Assuming removing name is enough.
- Why it is wrong: combinations of dates, location, and health data can re-identify.
- Better approach: formal de-identification/tokenization strategy.

## 13. Mini Example

```text
Raw PHI:
member_id, diagnosis_code, provider_id, service_date, claim_amount

Analytics-safe:
member_token, diagnosis_group, region, service_month, claim_amount
```

## 14. Interview Questions

1. What is PHI?
2. PHI vs PII?
3. What is ePHI?
4. How do you protect PHI in a data lake?
5. Why is de-identification hard?

## 15. Interview Speak

"PHI is identifiable health information and needs strict controls. I would separate raw PHI, enforce minimum necessary access, use masking/tokenization/de-identification for analytics, encrypt data, log access, and ensure compliance controls around users, jobs, vendors, and retention."

## 16. Quick Recall

- One-line summary: PHI is identifiable health data.
- Three keywords: health, identity, minimum necessary.
- One trap: Removing names but leaving re-identification risk.
- One memory trick: Health plus identity equals extra care.
