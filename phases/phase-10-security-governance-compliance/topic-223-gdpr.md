# Topic 223: GDPR

## 1. Goal

Understand GDPR from a data engineering and platform design point of view.

## 2. Baby Intuition

GDPR is a rulebook for handling personal data of people in the EU/EEA.

For data engineers, it means personal data needs clear purpose, protection, auditability, retention control, and deletion/rights workflows.

## 3. What It Is

- Simple definition: GDPR is the EU data protection regulation for personal data.
- Technical definition: The General Data Protection Regulation is EU legislation governing processing of personal data, with obligations for organizations and rights for individuals.
- Category: Privacy regulation / compliance.
- Related terms: personal data, data subject, controller, processor, lawful basis, data minimization, consent, deletion, portability.

Official reference:

```text
European Commission GDPR/data protection overview:
https://commission.europa.eu/law/law-topic/data-protection/legal-framework-eu-data-protection_en
```

## 4. Why It Exists

GDPR exists to strengthen privacy and data protection rights in the digital age.

For data platforms, it pushes teams to answer:

- why are we collecting this personal data?
- who can access it?
- how long do we keep it?
- can we delete or export it if required?
- can we prove what happened?
- do vendors/processors have the right controls?

## 5. Where It Fits In A Data Platform

```text
personal data enters platform
  -> classify and document purpose
  -> restrict and protect
  -> process according to policy
  -> support access/export/delete rights
  -> retain audit evidence
```

## 6. How It Works Step By Step

Engineering view:

1. Identify personal data.
2. Classify sensitivity and data subject region.
3. Record purpose and owner.
4. Apply minimization and access controls.
5. Protect data with masking/tokenization/encryption where appropriate.
6. Track lineage and copies.
7. Apply retention/deletion rules.
8. Support rights workflows such as access, correction, deletion, and portability where applicable.
9. Audit access and processing.

## 7. How To Use It Practically

Data platform controls:

- data catalog with personal-data tags
- lawful-purpose metadata
- access approval workflow
- data processing inventory
- retention policy
- right-to-erasure workflow
- subject access/export workflow
- vendor/processor review
- breach/incident workflow

Practical data engineering design:

```text
Avoid spreading raw personal data into many marts.
Use stable surrogate keys and controlled mapping tables where possible.
```

## 8. Real-World Scenario

- Product/system: EU customer analytics.
- Problem: Customer asks for deletion of personal data.
- How GDPR-aware design helps: lineage shows where data exists; deletion workflow removes/anonymizes applicable records; audit logs prove completion.
- What would go wrong without it: teams cannot find all copies of the user's data.

## 9. System Design Angle

Mention GDPR when:

- EU/EEA personal data is processed
- personal data appears in logs/events/lakes/warehouses
- retention and deletion are discussed
- vendors/processors are involved
- cross-border data movement appears

Important caution:

```text
Legal interpretation belongs to privacy/legal teams.
Engineering builds controls that enforce policy.
```

## 10. Trade-offs

| GDPR-Friendly Control | Trade-off |
|---|---|
| data minimization | less exploratory data |
| strict retention | less history |
| deletion workflows | engineering complexity |
| purpose-based access | more governance process |
| pseudonymization | token/key mapping complexity |

## 11. Failure Modes

- Failure: No lineage for personal data.
- Symptom: cannot complete deletion/access request.
- Recovery: trace copies manually and fix catalog.
- Prevention: lineage and classification.

- Failure: Personal data in unmanaged logs.
- Symptom: retention/deletion policy bypassed.
- Recovery: scrub logs and fix logging.
- Prevention: PII-safe logging standards.

- Failure: Retention not enforced.
- Symptom: personal data kept longer than policy.
- Recovery: cleanup/backfill deletion.
- Prevention: automated lifecycle and retention jobs.

## 12. Common Mistakes

- Mistake: Treating GDPR as only a legal document.
- Why it is wrong: compliance requires real technical controls.
- Better approach: implement classification, access, retention, deletion, audit, and incident processes.

- Mistake: Assuming deleting one warehouse row deletes all copies.
- Why it is wrong: data may exist in logs, backups, caches, marts, and ML features.
- Better approach: use lineage-driven deletion workflow.

## 13. Mini Example

```text
Customer deletion request:
1. verify request
2. find customer identifiers
3. locate datasets through lineage/catalog
4. delete/anonymize according to policy
5. recompute affected aggregates if needed
6. record audit evidence
```

## 14. Interview Questions

1. What is GDPR?
2. What is personal data?
3. How does GDPR affect data pipelines?
4. How do you support right to deletion?
5. Why does lineage matter for privacy?

## 15. Interview Speak

"From an engineering perspective, GDPR means personal data must be classified, minimized, protected, governed by purpose and access controls, retained only according to policy, and traceable for rights workflows such as access, correction, portability, and deletion. I would partner with legal/privacy teams for policy interpretation."

## 16. Quick Recall

- One-line summary: GDPR governs personal data handling for EU/EEA data subjects.
- Three keywords: personal data, purpose, rights.
- One trap: No lineage for deletion requests.
- One memory trick: Know why you store it, who can see it, and how to remove it.
