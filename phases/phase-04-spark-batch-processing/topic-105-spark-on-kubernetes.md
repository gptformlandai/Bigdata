# Topic 105: Spark On Kubernetes

## 1. Goal

Understand how Spark runs on Kubernetes and why many modern platforms use it.

## 2. Baby Intuition

Kubernetes is like a container building manager.

Spark says:

```text
I need one driver container and many executor containers.
```

Kubernetes places them on machines and keeps track of them.

## 3. What It Is

- Simple definition: Spark on Kubernetes runs Spark driver and executors as Kubernetes pods.
- Technical definition: Spark can use Kubernetes as a cluster manager, launching a driver pod and executor pods that run Spark workloads in containers.
- Category: Spark deployment model.
- Related terms: pod, container, driver pod, executor pod, namespace, service account, image.

## 4. Why It Exists

Companies use Kubernetes to standardize deployment.

Spark on Kubernetes helps:

- run Spark in containers
- isolate jobs by namespace/resources
- use Kubernetes scheduling
- integrate with cloud-native infrastructure
- package dependencies into images

## 5. Where It Fits In A Data Platform

```text
spark-submit -> Kubernetes API -> driver pod -> executor pods -> storage
```

Storage may be:

- S3
- GCS
- ADLS
- HDFS
- lakehouse table storage

## 6. How It Works Step By Step

1. User submits Spark application with Kubernetes master URL.
2. Spark creates driver pod.
3. Driver requests executor pods.
4. Kubernetes scheduler places pods on worker nodes.
5. Executors connect back to driver.
6. Tasks run inside executor pods.
7. Pods terminate when application finishes.

## 7. How To Use It Practically

Submit shape:

```bash
spark-submit \
  --master k8s://https://kubernetes-api:6443 \
  --deploy-mode cluster \
  --name spark-job \
  --conf spark.executor.instances=5 \
  --conf spark.kubernetes.container.image=my-spark-image:latest \
  local:///opt/spark/jobs/job.py
```

Common Kubernetes concerns:

- container image
- service account permissions
- namespace
- CPU/memory requests and limits
- logs
- storage credentials
- network access

## 8. Real-World Scenario

- Product/system: Cloud-native data platform.
- Problem: Team wants Spark jobs deployed like other containerized workloads.
- How Kubernetes helps: Schedules driver/executor pods and standardizes images.
- What would go wrong without good setup: dependency, permission, or resource issues can make jobs fail before processing starts.

## 9. System Design Angle

Spark on Kubernetes is useful when:

- organization already uses Kubernetes
- containerized dependency management is important
- workload isolation matters
- cloud-native scaling is desired

Watch for:

- pod startup overhead
- image size
- executor pod failures
- shuffle storage behavior
- permissions/secrets
- observability

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| containerized Spark jobs | Kubernetes complexity |
| dependency isolation | image management |
| cloud-native scheduling | pod startup overhead |
| namespace/resource controls | networking/security setup |

## 11. Failure Modes

- Failure: Image missing dependency.
- Symptom: driver/executor import error.
- Recovery: rebuild image.
- Prevention: test images before production.

- Failure: Pods cannot access storage.
- Symptom: read/write permission errors.
- Recovery: fix IAM/secrets/service account.
- Prevention: standardize storage access.

- Failure: Executors killed by resource limit.
- Symptom: pod OOMKilled.
- Recovery: tune memory/overhead/limits.
- Prevention: align Spark configs and K8s limits.

## 12. Common Mistakes

- Mistake: Setting Spark memory but not Kubernetes memory limits correctly.
- Why it is wrong: pod can be killed even if Spark config seems fine.
- Better approach: align executor memory, overhead, and pod limits.

- Mistake: Building huge images.
- Why it is wrong: slow startup and deployment friction.
- Better approach: keep images lean and versioned.

## 13. Mini Example

```text
Spark app on Kubernetes:
driver pod
  -> executor pod 1
  -> executor pod 2
  -> executor pod 3
```

Each pod is a containerized Spark process.

## 14. Interview Questions

1. How does Spark run on Kubernetes?
2. What is a driver pod?
3. What is an executor pod?
4. What issues are common on Kubernetes?
5. How do memory limits affect Spark pods?

## 15. Interview Speak

"Spark on Kubernetes uses Kubernetes as the cluster manager. Spark launches a driver pod, and the driver requests executor pods. Kubernetes schedules these pods on worker nodes. This gives containerized deployment and resource isolation, but requires careful image, permissions, memory, networking, and logging setup."

## 16. Quick Recall

- One-line summary: Spark on Kubernetes runs driver/executors as pods.
- Three keywords: pod, image, namespace.
- One trap: Misaligned Spark memory and pod limits.
- One memory trick: Kubernetes gives Spark containers a place to run.
