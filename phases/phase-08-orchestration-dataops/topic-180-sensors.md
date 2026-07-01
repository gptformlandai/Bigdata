# Topic 180: Sensors

## 1. Goal

Understand sensors as tasks that wait for something before downstream tasks run.

## 2. Baby Intuition

A sensor is like waiting at the door for a package.

The next step should not start until the package arrives.

## 3. What It Is

- Simple definition: A sensor waits for an external condition to become true.
- Technical definition: In orchestration systems like Airflow, a sensor is a task that repeatedly checks for a condition such as a file, partition, API response, external task, or dataset availability.
- Category: Workflow waiting/coordination primitive.
- Related terms: poke, reschedule, deferrable sensor, ExternalTaskSensor, file sensor, dataset dependency.

## 4. Why It Exists

Data pipelines often depend on external events:

- file arrives in S3
- upstream DAG finishes
- table partition is created
- API export is ready
- partner feed lands

Starting too early causes failures or incomplete data. Sensors wait safely.

## 5. Where It Fits In A Data Platform

```text
wait_for_file sensor
  -> load_file
  -> validate_data
  -> transform_data
```

Sensors are usually upstream of tasks that need external inputs.

## 6. How It Works Step By Step

1. Sensor task starts.
2. It checks a condition.
3. If condition is false, it waits.
4. It checks again after an interval.
5. If condition becomes true, sensor succeeds.
6. Downstream tasks can run.
7. If timeout is reached, sensor fails.

## 7. How To Use It Practically

Common sensors:

| Sensor | Waits For |
|---|---|
| File/S3 sensor | file/object arrival |
| ExternalTaskSensor | another DAG/task success |
| SQL sensor | query condition |
| HTTP/API sensor | external API condition |
| Dataset/event sensor | dataset update |

Practical advice:

- set timeout
- set poke interval
- prefer reschedule/deferrable sensors where available
- avoid thousands of busy sensors
- alert on stuck waits

## 8. Real-World Scenario

- Product/system: Partner data feed.
- Problem: Vendor uploads a daily file at unpredictable time.
- How sensor helps: pipeline waits for file before loading and validating it.
- What would go wrong without it: load task runs early and fails or loads partial data.

## 9. System Design Angle

Mention sensors when:

- dependency is external
- file arrival is uncertain
- pipeline should wait, not fail immediately
- upstream workflow is outside current DAG

Trade-off:

```text
Sensors improve coordination but can consume scheduler/worker resources if misused.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| clean external waiting | can waste worker slots |
| avoids premature runs | stuck sensors delay pipelines |
| simple dependency expression | many sensors can overload system |
| useful for files/partitions | timeout policy needed |

## 11. Failure Modes

- Failure: File never arrives.
- Symptom: sensor times out or waits forever.
- Recovery: alert vendor/team.
- Prevention: timeout and SLA.

- Failure: Sensor consumes worker slot all day.
- Symptom: other tasks starve.
- Recovery: use reschedule/deferrable mode.
- Prevention: efficient sensor configuration.

- Failure: Sensor checks wrong path/partition.
- Symptom: false timeout.
- Recovery: fix path/date logic.
- Prevention: test date templating.

## 12. Common Mistakes

- Mistake: No timeout.
- Why it is wrong: task can wait forever.
- Better approach: set timeout and alert.

- Mistake: Using sensors for high-frequency event streaming.
- Why it is wrong: orchestration sensors are not stream processors.
- Better approach: use event-driven/streaming systems for real-time triggers.

## 13. Mini Example

```text
wait_for_s3_file
  -> load_orders
  -> validate_orders
```

## 14. Interview Questions

1. What is a sensor?
2. What does a file sensor do?
3. Why do sensors need timeouts?
4. What is the downside of many sensors?
5. Sensor vs streaming system?

## 15. Interview Speak

"A sensor waits for an external condition before allowing downstream tasks to run. I use sensors for file, partition, external task, or API readiness, but I configure timeouts and efficient modes so sensors do not waste worker capacity or wait forever."

## 16. Quick Recall

- One-line summary: A sensor waits before the pipeline continues.
- Three keywords: wait, timeout, external condition.
- One trap: Sensors without timeout.
- One memory trick: Doorbell for data arrival.
