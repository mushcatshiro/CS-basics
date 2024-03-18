# Big Data

## Athena

A serverless query service to analyze data (files) stored in S3 using SQL 
(build on Presto). It supports

- csv
- JSON
- ORC
- Arvo
- Parquet

It is charged based on every TB of data scanned for $5.00. It is commonly used
with QuickSight for reporting dashboards. The combination is commonly used for
BI, analytics/reporting of VPC flow logs, ELB logs, CloudTrails and etc. To
improve performance,

- use columnar data (less scan)
  - parquet or ORC, which can be converted using AWS Glue
- compress data for smaller retrieval
  - bzip2, gzip etc
- partition dataset in S3 using virtual columns (i.e. the s3 "path")
  - s3://bucketname/partition/partition/filename
  - s3://bucketname/year=1991/month=07/some.csv
- use larger files (>128 MB) to minimize overhead
  - more efficient to scan a large file compared to many small files

### Federated Query

Allows user to run SQL queries across data stored in relational,
non-relational, object and custom data sources (AWS/on-prem) using data source
connectors that run with Lambda. Queried results can be stored to S3.

![fed-q](../static/fed-q.PNG)

## RedShift

Based on PostgreSQL but not for OLTP but OLAP i.e. analytics and data
warehouse. 10x performance compared to other data warehouses and scales to PBs
of data. The performance improvement is achieved through columnar storage of
data and parallel query engine. Cost is charged based on instances provisioned.
SQL and BI tools e.g. Tableau and AWS QuickSight compatible.

Comparing to Athena, data first needs to load to RedShift before query can
happen. However RedShift can perform faster queries, join aggregations due to
indexes. Loading data to RedShift can be done through KDF or S3 using COPY
command. Underlying mechanism of KDF would be first copy to S3 then issuing
a COPY command  to RedShift. A third option is to use JDBC driver to bulk
insert data to the cluster.

> take note that S3 copy to RedShift might go through internet (traffic cost),
> unless enhanced VPC routing is configured. also always insert bulk data into
> RedShift for efficiency reasons

RedShift is deployed as a cluster withi leader and compute nodes. Leader node
plans queries and aggregate results while compute node perform queries and
sends results to leader node. Node size has to be provisioned in advance and
reserved instance can be used for cost savings. RedShift has Multi-AZ mode for
disaster recovery. If Multi-AZ is not used, snapshots can be alternative to
disaster recovery. Snapshots are PITR backups for cluster stored in S3 and are
stored incrementally. Each snapshots can be restored into a new cluster. The
default automated backup is every 8 hours or every 5GB. Alternatively a custom
schedule can be set. Retention of automated snapshot can be also set. Manual
snapshots are permanent. RedShift can be configured to automatically copy
snapshots (automated backup or manual backup) of a cluster to another AWS
region.

### RedShift Spectrum

Query data in S3 without loading to RedShift cluster. RedShift cluster issue
a query command to RedShift Spectrum to launch thousands of Spectrum nodes to
query in S3. These resides on dedicated RedShift servers independent of the
RedShift cluster.

## Amazon OpenSearch

Was known as Amazon Elasticsearch previously. In DDB, query only exists by
primary key and indexes but with OpenSearch, all fields can be searched
including partial matches. It is common to use OpenSearch as a complement to
another database. Although the name does not suggest, OpenSearch is capable of
doing analytical search. There are two modes,

- managed cluster
- serverless cluster

It does not support SQL but can be enabled with plugin. Data can be ingested
from KDF, AWS IoT and CloudWatch Logs. Security is achieved through Cognito &
IAM, KMS encryption and TLS. Searched results can be visualized within
OpenSearch Dashboards.

OpenSearch DDB common pattern

![os-pat-1](../static/os-pat-1.PNG)

OpenSearch CloudWatch Logs and KDS common pattern

![os-pat-2](../static/os-pat-2.PNG)

## EMR

Elastic MapReduce, to help create Hadoop clusters to analyze and process vast
amount of data. EMR is made of hundreds of EC2 instances. EMR comes with Apache
Spark, HBase, presto, Flink and etc. These bundled items are challenging to
setup and with EMR, it is all taken care of including provisioning and
configuration. Auto-scaling can be enabled and spot instances can be used for
cost optimization.

> used for batch jobs e.g. data processing, ML, web indexing, big data etc.

Nodes

- master node: manage cluster and health, coordinate - long running
- core node: run task and store data - long running
- task node: run task - usually spot instances

Purchasing options

- on demand
- reserved for cost savings (EMR will automatically use if available)
- spot instances

EMR can be a long running cluster or transient (temporary) cluster.

## Amazon QuickSight

A serverless ML powered BI service to create interactive dashboards. It is
fast, scalable, embeddable with per-session pricing. It integrates well with
RDS, Athena, RedShift, S3 and etc. It also works with 3rd party databases,
on-prem database and files. An in-memory computation using SPICE engine can be
used if data is imported to QuickSight.

For enterprise version, it is possible to setup a column-level security.
QuickSight allows definition of users (standard version) and groups
(enterprise version).

> note groups and users are not IAM equivalent, they exists only within
> QuickSight

When a dashboard is created, it is a read only snapshot of an analysis that is
shared. It preserves the configuration of the analysis (filtering, parameters,
controsl and sort). The analysis or dashboard can be shared with users or
groups. Dashboard must be published before it can be shared. Those who can see
the dashboard can see the underlying data.

## Glue

A fully managed, serverless ETL service to prepare and transform data for
analytics. A few use cases including

- extract data from S3 and RDS, transform and load to RedShift
- extract/import csv in S3, transform it to parquet and load to S3 for Athena
  - S3 event notification to Lambda fn/EventBridge to trigger Glue ETL job

Note requires scripting (py/scala).

### Glue Data Catalog

AWS Glue data crawler crawls from S3, RDS, DDB or any JDBC compatible databse
and stores each database's metadata into AWS Glue data catalog for

- Glue ETL jobs
- Athena
- RedShift Spectrum
- EMR

### Other Glue Features

- Glue Job Bookmarks: prevent re-processing data
- Glue Elastic View:
  - combine and replicate data across multiple data stores using SQL
  - no custom code, Glue monitors changes in source data serverless
  - using virtual table
- Glue DataBrew: clean and normalize data using pre-build transformations
- Glue Studio: GUI for create, run and monitor Glue jobs
- Glue Streaming ETL: built on Apache Spark structured streaming
  - compatible with upstream KDS, Kafka and MSK

## Lake Formation

Data lake is a central place to have all data for analytical purposes and takes
months to setup, but with Lake Formation it only takes days. It helps to
discover, cleanse, transform and ingest data to a data lake. It automates
complex manual steps and de-duplicates using ML transforms. This allows the
combination of structured and unstructured data in data lake. It has out of the
box blueprints for S3, RDS, relational and non-relational databases. It
essentially build on top of Glue and data is stored in S3. At Lake Formation's
downstream, Athena, RedShift, EMR and Apache Spark can be used.

Lake Formation offers fine grained access control for any applications (row and
column level). The crentralized permission to data is what make AWS Lake
Formation usedful instead of IAM control all over the place (RDS, S3, Athena,
QuickSight and etc).

## Kinesis Data Analytics

There are two options - SQL and Apache Flink.

For SQL option, KDS's upstream can only be KDF and KDS with optional reference
data join from S3 with SQL statement. The downstream options are same as its
upstream to pipe to another service/destination. Real time analytics can be
achieved. It is fully managed with no server to provision, scales
automatically and pay as per actual consumption.

For Flink option, Flink (Java, Scala, SQL) is used to process and analyze
streaming data. Streaming Flink application are code needed to be written and
the upstreams must be KDS or MSK. These Flnk application must run on managed
cluster on AWS. Provisioning of compute resource is automated, it allows for
parallel computation and auto scaling. Application backups are implemented as
checkpoints and snapshots.

## Managed Streaming for Apache Kafka (MSK)

It is an alternative to Kinesis. It is a fully managed Apache Kafka on AWS to
stream data. Clusters can be CRUD in real time. MSK creates and manages Kafka
broker nodes and zookeeper nodes. MSK deploys the cluster within VPC in multi
AZ fashion (up to 3 for HA). It offers automatic recovery from common Kafka
failures and the data is stored on EBS volumes permanently.

MSK downstream can eb KFA Flink option, Glue (Spark), lambda, EC2 consumers.

A serverless option is given such that capacity is taken care of. MSK
automatically provision resources and scales the compute and storage nodes.

### MSK vs KDS

| KDS | MSK |
|-|-|
| 1MB msg size limit | 1MB default, configurable |
| data stream with shards | Kafka topics with partition |
| shard spliting and merging for scaling | only adding partition to topic for scaling (no scale down option) |
| TLS in-flight encryption | plain text or TLS |
| KMS at rest encryption | KMS at rest encryption |
| 1-365 days | data can be kept permanently |
