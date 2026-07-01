# Topic 187: CI/CD For Data Pipelines

## 1. Goal

Understand how CI/CD applies to data pipelines.

## 2. Baby Intuition

CI/CD is a safety gate before changes reach production.

Instead of editing a pipeline and hoping it works, you test and deploy it through a controlled process.

## 3. What It Is

- Simple definition: CI/CD automates testing and deployment of pipeline changes.
- Technical definition: CI/CD for data pipelines uses automated checks, builds, tests, approvals, and deployment workflows to safely promote DAGs, SQL models, infrastructure, and configuration across environments.
- Category: DataOps and release engineering.
- Related terms: pull request, build, test, deploy, environment, promotion, rollback.

## 4. Why It Exists

Data pipeline changes can break:

- dashboards
- ML features
- finance reports
- downstream tables
- SLAs

Manual deployment is risky. CI/CD reduces surprise by checking code before production.

## 5. Where It Fits In A Data Platform

```text
developer change
  -> pull request
  -> automated tests/checks
  -> review
  -> deploy to dev/staging/prod
  -> monitor
```

Applies to:

- Airflow DAGs
- dbt models
- Spark jobs
- SQL scripts
- data quality checks
- infrastructure config

## 6. How It Works Step By Step

1. Developer changes code.
2. Opens pull request.
3. CI runs linting and unit tests.
4. CI validates DAG/dbt/project syntax.
5. CI may run sample/integration data tests.
6. Reviewer approves.
7. CD deploys to environment.
8. Production run is monitored.
9. Rollback happens if needed.

## 7. How To Use It Practically

Checks to include:

| Pipeline Type | CI Checks |
|---|---|
| Airflow | DAG import test, lint, dependency checks |
| dbt | compile, test, docs build, slim CI |
| Spark | unit tests, schema tests, small sample run |
| SQL | syntax, formatting, data tests |
| Infra | plan/validate policy |

Deployment environments:

```text
dev -> staging -> production
```

## 8. Real-World Scenario

- Product/system: Revenue dbt project.
- Problem: A new model change could break executive dashboards.
- How CI/CD helps: compile dbt, run tests on changed models, review SQL, deploy after approval.
- What would go wrong without it: bad SQL reaches production and fails during morning refresh.

## 9. System Design Angle

Mention CI/CD when:

- pipelines are mission-critical
- multiple engineers contribute
- schema/model changes happen often
- production reliability matters
- rollback/release control is needed

Key maturity:

```text
Pipeline code should be deployed like software, with data-specific tests added.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| safer deployments | setup effort |
| catches syntax/test failures early | test environments cost money |
| reviewable changes | sample tests may miss production data issues |
| repeatable releases | pipeline promotion process can slow quick fixes |

## 11. Failure Modes

- Failure: CI only checks syntax.
- Symptom: code deploys but data is wrong.
- Recovery: add data tests/integration checks.
- Prevention: layered test strategy.

- Failure: No rollback plan.
- Symptom: bad deployment stays live too long.
- Recovery: revert and redeploy.
- Prevention: versioned releases and rollback process.

- Failure: Environment drift.
- Symptom: works in dev, fails in prod.
- Recovery: align config.
- Prevention: infrastructure as code and environment parity.

## 12. Common Mistakes

- Mistake: Deploying DAGs manually through UI or file copy.
- Why it is wrong: no audit trail or consistent tests.
- Better approach: deploy from version control through CI/CD.

- Mistake: Not testing DAG import.
- Why it is wrong: one Python syntax/import error can break DAG visibility.
- Better approach: run import/parse tests in CI.

## 13. Mini Example

```text
Pull request:
change dbt revenue model

CI:
dbt compile
dbt test changed models
SQL lint

CD:
deploy after approval
```

## 14. Interview Questions

1. What is CI/CD for data pipelines?
2. What tests should run for Airflow DAGs?
3. What tests should run for dbt?
4. How do you deploy safely?
5. How do you roll back bad pipeline changes?

## 15. Interview Speak

"CI/CD for data pipelines means treating pipeline code like production software. I would use pull requests, linting, unit tests, DAG/dbt compile checks, data tests on samples or changed models, controlled deployments, monitoring, and rollback."

## 16. Quick Recall

- One-line summary: CI/CD tests and deploys data pipeline changes safely.
- Three keywords: pull request, tests, deploy.
- One trap: Syntax-only CI for data code.
- One memory trick: Seatbelt before production.
