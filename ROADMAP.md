# Big Data MAANG Roadmap

This roadmap is intentionally broad. We will fill it modularly by phase. Most topics use the compact template in `TOPIC_TEMPLATE.md`; heavier system design topics get deeper trade-off and failure-mode treatment.

## Phase 0: Computer Science And Data Foundations

Status: Complete.

1. What is data?
2. Structured vs semi-structured vs unstructured data
3. Files, records, rows, columns
4. JSON, CSV, XML, Avro, Parquet, ORC
5. Compression: gzip, snappy, zstd
6. Serialization and deserialization
7. Encoding
8. Data schemas
9. Schema evolution
10. Basic Linux for data engineering
11. Networking basics: HTTP, TCP, DNS, ports
12. APIs and REST
13. SQL basics
14. Indexes
15. Transactions
16. ACID
17. CAP theorem
18. Consistency models
19. Latency vs throughput
20. Horizontal vs vertical scaling

## Phase 1: Big Data Basics

Status: Not started.

21. What is Big Data?
22. 3Vs, 5Vs, and practical meaning
23. Data lake
24. Data warehouse
25. Lakehouse
26. OLTP vs OLAP
27. Batch processing
28. Stream processing
29. Real-time vs near-real-time
30. ETL vs ELT
31. Data pipeline
32. Data platform
33. Data mesh
34. Data mart
35. Data catalog
36. Metadata
37. Lineage
38. Data quality
39. Data governance

## Phase 2: Distributed Systems Foundations

Status: Complete.

40. Distributed systems
41. Replication
42. Partitioning/sharding
43. Consistent hashing
44. Leader/follower architecture
45. Quorum
46. Consensus basics
47. Raft and Paxos intuition
48. Fault tolerance
49. Idempotency
50. Retries and exponential backoff
51. Circuit breakers
52. Backpressure
53. Load balancing
54. Caching
55. Bloom filters
56. Clock skew
57. Exactly-once vs at-least-once vs at-most-once
58. Ordering guarantees
59. Eventual consistency
60. Distributed locks

## Phase 3: Hadoop Ecosystem

Status: Complete.

61. Hadoop overview
62. HDFS
63. NameNode and DataNode
64. HDFS block storage
65. Replication factor
66. MapReduce
67. YARN
68. Hive
69. Hive metastore
70. Partitioning in Hive
71. Bucketing in Hive
72. HBase
73. Sqoop
74. Flume
75. Oozie
76. Hadoop limitations
77. Why Spark replaced MapReduce for many workloads

## Phase 4: Spark And Batch Processing

Status: Complete.

78. Apache Spark overview
79. Spark architecture
80. Driver and executors
81. Spark cluster manager
82. RDD
83. DataFrame
84. Dataset
85. Transformations vs actions
86. Lazy evaluation
87. DAG
88. Stages and tasks
89. Narrow vs wide transformations
90. Shuffle
91. Broadcast join
92. Sort-merge join
93. Partitioning in Spark
94. Caching and persistence
95. Spark SQL
96. Catalyst optimizer
97. Tungsten engine
98. Adaptive query execution
99. Data skew
100. Small files problem
101. Spark memory management
102. Spark performance tuning
103. Spark job failure handling
104. PySpark
105. Spark on Kubernetes
106. Spark on EMR/Dataproc/Databricks

## Phase 5: Streaming And Messaging

Status: Complete.

107. Event-driven architecture
108. Message queues vs event streams
109. Apache Kafka overview
110. Kafka broker
111. Kafka topic
112. Kafka partition
113. Kafka offset
114. Kafka consumer group
115. Kafka replication
116. Kafka ISR
117. Kafka producer acknowledgments
118. Kafka retention
119. Kafka compaction
120. Kafka ordering guarantees
121. Kafka exactly-once semantics
122. Kafka Connect
123. Kafka Streams
124. Schema Registry
125. Avro with Kafka
126. Dead letter queues
127. Consumer lag
128. Backpressure in streaming
129. Apache Flink
130. Flink state
131. Flink checkpointing
132. Flink watermarks
133. Event time vs processing time
134. Windowing
135. Late events
136. Spark Structured Streaming
137. Real-time analytics architecture

## Phase 6: Modern Data Lakehouse

138. Data lakehouse architecture
139. Apache Iceberg
140. Delta Lake
141. Apache Hudi
142. Table formats
143. Snapshot isolation
144. Time travel
145. ACID on data lake
146. Compaction
147. Merge-on-read vs copy-on-write
148. Upserts on data lake
149. Metadata scaling
150. Partition evolution
151. Hidden partitioning
152. Z-ordering/clustering
153. Vacuum/cleanup
154. Lakehouse performance tuning

## Phase 7: Warehouses And Query Engines

155. Data warehouse architecture
156. Snowflake
157. BigQuery
158. Redshift
159. Synapse
160. ClickHouse
161. Druid
162. Pinot
163. Presto/Trino
164. Athena
165. Columnar storage
166. MPP architecture
167. Query planning
168. Cost-based optimizer
169. Materialized views
170. OLAP cubes
171. Star schema
172. Snowflake schema
173. Fact and dimension tables
174. Slowly changing dimensions
175. Data modeling for analytics

## Phase 8: Orchestration And DataOps

176. Apache Airflow
177. DAGs
178. Airflow scheduler
179. Airflow executor
180. Sensors
181. Backfills
182. Retries
183. SLAs
184. Dagster
185. Prefect
186. dbt
187. CI/CD for data pipelines
188. Data pipeline testing
189. Data contracts
190. Data observability
191. Great Expectations
192. Monte Carlo/Datafold-style observability concepts
193. Pipeline monitoring
194. Alerting
195. Incident response for data pipelines

## Phase 9: Cloud Big Data

196. AWS S3
197. AWS EMR
198. AWS Glue
199. AWS Athena
200. AWS Kinesis
201. AWS Redshift
202. AWS Lambda for data
203. GCP Cloud Storage
204. GCP Dataproc
205. GCP Dataflow
206. GCP Pub/Sub
207. BigQuery
208. Azure Data Lake Storage
209. Azure Synapse
210. Azure Event Hubs
211. Azure Databricks
212. Cloud cost optimization
213. IAM and security
214. Encryption at rest and in transit
215. VPC/networking basics for data platforms

## Phase 10: Security, Governance, And Compliance

216. Authentication
217. Authorization
218. RBAC
219. ABAC
220. IAM
221. PII
222. PHI
223. GDPR
224. HIPAA
225. Data masking
226. Tokenization
227. Encryption
228. Key management
229. Audit logs
230. Access control in data lakes
231. Row-level security
232. Column-level security
233. Data retention
234. Right to be forgotten
235. Governance at scale

## Phase 11: Advanced Architecture Patterns

236. Lambda architecture
237. Kappa architecture
238. Medallion architecture
239. Bronze, silver, gold layers
240. CDC
241. Debezium
242. Outbox pattern
243. Saga pattern
244. Event sourcing
245. CQRS
246. Feature stores
247. Real-time feature pipelines
248. Search analytics pipelines
249. Recommendation data pipelines
250. Fraud detection pipelines
251. Metrics platform
252. Logging platform
253. Time-series analytics
254. Multi-tenant data platforms
255. Data platform reliability

## Phase 12: MAANG-Level System Design

256. Design YouTube analytics pipeline
257. Design Netflix viewing analytics
258. Design Uber real-time location pipeline
259. Design LinkedIn feed analytics
260. Design Amazon clickstream pipeline
261. Design fraud detection system
262. Design real-time ad analytics
263. Design log aggregation system
264. Design metrics monitoring system
265. Design recommendation feature pipeline
266. Design data lake for an enterprise
267. Design data warehouse for finance reporting
268. Design CDC pipeline from MySQL to lakehouse
269. Design real-time dashboard system
270. Design batch + streaming hybrid architecture

For every system design topic, include:

- Requirements
- Functional requirements
- Non-functional requirements
- Capacity estimation
- APIs/events
- Data model
- High-level architecture
- Deep dive components
- Data flow
- Scaling strategy
- Partitioning strategy
- Storage choices
- Processing choices
- Consistency guarantees
- Failure handling
- Monitoring
- Cost optimization
- Security
- Trade-offs
- Interview-ready final answer

## Phase 13: Interview Mastery

271. Big Data resume project ideas
272. Common Big Data interview questions
273. Spark interview questions
274. Kafka interview questions
275. Airflow interview questions
276. SQL interview questions
277. Data modeling interview questions
278. System design interview framework
279. Debugging production pipeline questions
280. Performance tuning questions
281. Cost optimization questions
282. Behavioral stories for data engineers
283. How to explain trade-offs clearly
284. How to answer when you do not know
285. Final MAANG Big Data revision guide
