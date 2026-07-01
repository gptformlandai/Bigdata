# Topic 066: MapReduce

## 1. Goal

Understand MapReduce as Hadoop's original batch processing model: map records, shuffle by key, reduce grouped values.

## 2. Baby Intuition

Imagine a class counting words in many books.

Instead of one student reading every book:

1. Give each student some pages.
2. Each student counts words on their pages.
3. Group all counts by word.
4. Add counts for each word.

That is MapReduce.

## 3. What It Is

- Simple definition: MapReduce is a way to process huge data in parallel using map and reduce steps.
- Technical definition: MapReduce is a distributed batch programming model and execution engine that processes input splits with map tasks, groups intermediate data by key through shuffle/sort, and computes final results with reduce tasks.
- Category: Distributed batch processing.
- Related terms: mapper, reducer, shuffle, sort, input split, job, task, combiner.

## 4. Why It Exists

Before MapReduce, processing TB/PB-scale data was hard because developers had to manually handle:

- splitting data
- scheduling work
- moving data
- retrying failed tasks
- combining partial results
- running across many machines

MapReduce gave a simple programming model:

```text
map each record -> group by key -> reduce each group
```

Big Data teams cared because it made huge batch processing possible on commodity clusters.

## 5. Where It Fits In A Data Platform

```text
Sources -> HDFS -> MapReduce Processing -> HDFS Outputs -> Hive/Reports/Exports
```

MapReduce is a processing layer.

It reads from:

- HDFS files
- Hive table files
- logs
- CSV/JSON/SequenceFiles

It writes:

- output directories in HDFS
- aggregated files
- intermediate datasets

## 6. How It Works Step By Step

Example: word count.

Input:

```text
hello data
hello hadoop
```

Map phase:

```text
hello -> 1
data -> 1
hello -> 1
hadoop -> 1
```

Shuffle/sort:

```text
data -> [1]
hadoop -> [1]
hello -> [1, 1]
```

Reduce phase:

```text
data -> 1
hadoop -> 1
hello -> 2
```

Detailed flow:

1. Job is submitted.
2. Input files are split into input splits.
3. Map tasks process splits in parallel.
4. Mappers emit key-value pairs.
5. Framework shuffles and sorts by key.
6. Reducers process grouped values.
7. Output is written to HDFS.
8. Failed tasks are retried.

## 7. How To Use It Practically

Classic Hadoop job style:

```bash
hadoop jar job.jar com.example.WordCount /input /output
```

Output behavior:

- output path must not already exist
- output is usually a directory
- reducers write files like `part-r-00000`

Developer mental model:

```text
Mapper: transform each input record into key-value pairs.
Reducer: aggregate all values for a key.
```

## 8. Real-World Scenario

- Product/system: Daily ad click aggregation.
- Problem: Count clicks per campaign across billions of log records.
- How MapReduce helps: Mappers parse logs and emit `campaign_id -> 1`; reducers sum counts per campaign.
- What would go wrong without it: One machine could not process the logs quickly or reliably.

## 9. System Design Angle

MapReduce is a strong fit when:

- data is huge
- processing is batch
- latency can be minutes or hours
- work can be parallelized
- output is file/table based

Not a strong fit when:

- you need interactive queries
- you need iterative ML
- you need low-latency streaming
- you need many chained transformations quickly

MapReduce is throughput-oriented, not latency-oriented.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| massive batch scale | high job latency |
| automatic task retry | disk-heavy intermediate writes |
| simple programming model | verbose code |
| data locality | less efficient for iterative workloads |

## 11. Failure Modes

- Failure: Mapper fails.
- Symptom: task attempt fails.
- Recovery: Hadoop reruns the map task.
- Prevention: validate input and handle bad records.

- Failure: Reducer skew.
- Symptom: one reducer runs much longer than others.
- Recovery: repartition, salt hot keys, increase reducers.
- Prevention: understand key distribution.

- Failure: Shuffle failure.
- Symptom: reducers cannot fetch mapper output.
- Recovery: retry fetch or rerun map tasks.
- Prevention: stable network, enough disk, proper tuning.

## 12. Common Mistakes

- Mistake: Forgetting shuffle is expensive.
- Why it is wrong: shuffle moves data across network and writes to disk.
- Better approach: reduce shuffle size with combiners, filtering, and good keys.

- Mistake: Using one reducer for huge output.
- Why it is wrong: one reducer becomes bottleneck.
- Better approach: use enough reducers and balanced keys.

- Mistake: Thinking MapReduce is real-time.
- Why it is wrong: it is batch-oriented and disk-heavy.
- Better approach: use Spark/Flink/Kafka for lower-latency needs.

## 13. Mini Example

Python-style tiny logic:

```python
def mapper(line):
    for word in line.split():
        yield word, 1


def reducer(word, counts):
    yield word, sum(counts)
```

The framework handles:

- parallel map execution
- grouping by word
- sending each word group to reducer

## 14. Interview Questions

1. Explain map, shuffle, and reduce.
2. Why is shuffle expensive?
3. What happens if a mapper fails?
4. Why is MapReduce slower than Spark for many workloads?
5. What is data skew in MapReduce?

## 15. Interview Speak

"MapReduce is Hadoop's batch processing model. Mappers process input splits and emit key-value pairs, the framework shuffles and sorts data by key, and reducers aggregate grouped values. It scales well for large batch jobs and handles task retries, but it is disk-heavy and high-latency compared with newer engines like Spark."

## 16. Quick Recall

- One-line summary: MapReduce = map records, shuffle by key, reduce grouped values.
- Three keywords: map, shuffle, reduce.
- One trap: Ignoring shuffle cost.
- One memory trick: Many people count locally, then one group adds totals.
