# Topic 185: Prefect

## 1. Goal

Understand Prefect as a workflow orchestration tool focused on Pythonic flows and operational simplicity.

## 2. Baby Intuition

Prefect lets Python functions become managed workflows.

You write normal Python, then Prefect helps schedule, retry, observe, and run it.

## 3. What It Is

- Simple definition: Prefect orchestrates Python workflows called flows.
- Technical definition: Prefect is a workflow orchestration platform where Python functions are decorated as flows and tasks, then scheduled, deployed, observed, and executed with retries, state tracking, and infrastructure blocks/work pools.
- Category: Workflow orchestration.
- Related terms: flow, task, deployment, work pool, state, retry, block.

## 4. Why It Exists

Teams often want:

- simple Python workflow authoring
- fewer DAG constraints
- flexible local/cloud execution
- easy retries and logging
- modern UI and state tracking
- deployment-friendly orchestration

Prefect exists to make workflow orchestration feel natural to Python developers.

## 5. Where It Fits In A Data Platform

```text
Python data workflow
  -> Prefect flow/task definitions
  -> scheduled or triggered deployments
  -> workers execute work
  -> UI/API tracks state
```

Prefect can orchestrate Python scripts, dbt, Spark submit commands, API pulls, file processing, and warehouse operations.

## 6. How It Works Step By Step

1. Define Python functions as tasks.
2. Define a flow that calls tasks.
3. Configure retries, timeouts, and logging.
4. Create a deployment for schedule/runtime config.
5. Worker picks up scheduled flow run.
6. Tasks execute and report states.
7. UI shows logs, retries, failures, and duration.

## 7. How To Use It Practically

Conceptual code:

```python
@task(retries=3)
def extract_orders():
    ...

@flow
def daily_orders_pipeline():
    orders = extract_orders()
    validate_orders(orders)
    load_orders(orders)
```

Good fit:

- Python-first workflows
- smaller data teams
- flexible deployments
- API and file pipelines
- ML/data science workflows

## 8. Real-World Scenario

- Product/system: SaaS ingestion pipelines.
- Problem: Team pulls data from many APIs with Python and wants retries, schedules, logs, and alerts.
- How Prefect helps: Python flows wrap API tasks and track state without heavy DAG ceremony.
- What would go wrong without it: cron jobs fail silently and reruns are manual.

## 9. System Design Angle

Use Prefect when:

- workflows are Python-first
- developer ergonomics matter
- flexible runtime is useful
- team wants modern orchestration without strict DAG authoring

Be careful with:

- workflow complexity at enterprise scale
- governance standards
- deployment consistency
- separating orchestration from heavy compute

## 10. Trade-offs

| Pros | Cons |
|---|---|
| Pythonic authoring | ecosystem differs from Airflow |
| simple retries/state tracking | team must standardize deployments |
| flexible execution | may need governance patterns |
| good developer experience | not a compute engine |

## 11. Failure Modes

- Failure: Worker not running.
- Symptom: scheduled flows do not execute.
- Recovery: restart worker.
- Prevention: worker health checks.

- Failure: Non-idempotent retries.
- Symptom: duplicate writes.
- Recovery: deduplicate/repair.
- Prevention: idempotent task design.

- Failure: Secrets/config scattered.
- Symptom: deployment failures.
- Recovery: centralize config.
- Prevention: use blocks/secrets standards.

## 12. Common Mistakes

- Mistake: Confusing Pythonic with unstructured.
- Why it is wrong: workflows still need clear ownership, retries, and observability.
- Better approach: standardize flow patterns.

- Mistake: Running huge processing inside orchestration worker.
- Why it is wrong: orchestrator infrastructure may not be sized for heavy compute.
- Better approach: submit work to Spark/warehouse/Kubernetes where appropriate.

## 13. Mini Example

```text
flow daily_api_ingestion:
  extract from API
  validate records
  load to warehouse
  notify on failure
```

## 14. Interview Questions

1. What is Prefect?
2. What is a flow?
3. Prefect vs Airflow?
4. Where do retries fit?
5. When should heavy compute run outside Prefect?

## 15. Interview Speak

"Prefect is a Pythonic workflow orchestrator where functions become flows and tasks with retries, scheduling, state tracking, and deployments. It is useful for Python-heavy data workflows, but like Airflow, it should coordinate heavy compute rather than become the compute engine."

## 16. Quick Recall

- One-line summary: Prefect turns Python workflows into observable scheduled flows.
- Three keywords: flow, task, deployment.
- One trap: Letting flexible Python become messy pipelines.
- One memory trick: Python function plus production wrapper.
