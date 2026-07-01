# Topic 177: DAGs

## 1. Goal

Understand DAGs as the structure behind orchestrated workflows.

## 2. Baby Intuition

A DAG is a recipe with ordered steps.

You cannot bake the cake before mixing ingredients. In data pipelines, you cannot transform data before extracting it.

## 3. What It Is

- Simple definition: A DAG is a workflow graph with tasks and one-way dependencies.
- Technical definition: A directed acyclic graph is a set of nodes connected by directed edges where no cycle exists, commonly used to model task dependencies in workflow orchestration.
- Category: Workflow dependency model.
- Related terms: task, dependency, upstream, downstream, topological order, Airflow, Dagster.

## 4. Why It Exists

Data jobs depend on each other:

```text
extract -> validate -> transform -> publish
```

Without a DAG:

- tasks may run too early
- failures may not block downstream tasks
- reruns are hard to reason about
- dependency chains become hidden in scripts

DAGs make workflow order explicit.

## 5. Where It Fits In A Data Platform

```text
Orchestrator
  -> DAG definition
  -> task instances
  -> execution state
```

Airflow DAGs are Python files. Dagster also models assets/jobs with dependency graphs.

## 6. How It Works Step By Step

1. Define tasks as nodes.
2. Define dependencies as arrows.
3. Ensure no cycles exist.
4. Orchestrator finds tasks with all upstream dependencies complete.
5. Ready tasks run.
6. Downstream tasks wait until required upstream tasks succeed.
7. Failed upstream tasks usually block downstream tasks.

Example:

```text
extract_orders
  -> validate_orders
  -> transform_orders
  -> publish_orders
```

## 7. How To Use It Practically

Simple Airflow-style dependency:

```python
extract >> validate >> transform >> publish
```

Parallel branches:

```python
extract >> [clean_orders, clean_customers] >> build_mart
```

Good DAG design:

- one DAG per business workflow
- clear task names
- avoid hidden dependencies
- keep tasks reasonably small
- make tasks idempotent
- avoid cycles

## 8. Real-World Scenario

- Product/system: Daily customer 360 pipeline.
- Problem: Customer, order, and support data must load before building customer profile.
- How DAG helps: parallel source loads can run first, then profile build waits for all required inputs.
- What would go wrong without it: customer profile may build from incomplete inputs.

## 9. System Design Angle

Mention DAGs when:

- task dependency order matters
- parallelism is possible
- failure should block downstream work
- backfills need predictable execution

Key phrase:

```text
The DAG represents dependency order, not necessarily data flow volume.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| explicit dependencies | too many tiny tasks can be noisy |
| parallel execution | complex DAGs are hard to maintain |
| clear failure boundaries | dynamic dependencies can confuse users |
| visual monitoring | cycles are not allowed |

## 11. Failure Modes

- Failure: Missing dependency.
- Symptom: task runs before input is ready.
- Recovery: rerun after fixing DAG.
- Prevention: review dependencies.

- Failure: Overly complex DAG.
- Symptom: hard to debug and operate.
- Recovery: split or simplify.
- Prevention: design by business workflow.

- Failure: Cycle introduced.
- Symptom: DAG invalid.
- Recovery: remove circular dependency.
- Prevention: reason in one-way stages.

## 12. Common Mistakes

- Mistake: Creating one giant DAG for everything.
- Why it is wrong: ownership and failure impact become unclear.
- Better approach: split by domain/workflow boundaries.

- Mistake: Hiding dependencies inside scripts.
- Why it is wrong: orchestrator cannot schedule or monitor them.
- Better approach: express important dependencies in the DAG.

## 13. Mini Example

```text
Good:
extract_customers -> validate_customers -> publish_customers

Bad:
one task called run_everything.sh
```

## 14. Interview Questions

1. What is a DAG?
2. Why must DAGs be acyclic?
3. Upstream vs downstream?
4. How does a DAG enable parallelism?
5. What makes a DAG hard to maintain?

## 15. Interview Speak

"A DAG models workflow dependencies as directed, acyclic task relationships. The orchestrator runs tasks whose upstream dependencies have succeeded, which gives predictable order, parallelism, failure isolation, and clear operational visibility."

## 16. Quick Recall

- One-line summary: A DAG is a no-cycle graph of task dependencies.
- Three keywords: directed, acyclic, dependencies.
- One trap: Hiding real dependencies inside scripts.
- One memory trick: Recipe steps with arrows.
