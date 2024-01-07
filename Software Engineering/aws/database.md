# database

## Relational Database

### Relational Database Service (RDS)

AWS managed (patch, maintenance, continuous backup, point in time restore).
Supports MySQL/MariaDB, Postgresql, Microsoft SQL, Oracle, Aurora and custom
option. RDS provides a monitoring dashboard, read replica, multi AZ deployment
for disaster recovery. RDS can be scaled both vertically and horizontally.
RDS's is build on top of EBS (gp2 or io). For managed instance, SSH is not
allowed. RDS's maintenance will results in some downtime.

Auto scaling of RDS can be setup such that the storage increase dynamically by
setting a maximum storage threshold e.g. free storage is < 10% of provisioned
storage. Auto scaling is suitable for unpredictable workloads.

Custom RDS option is only for Oracle and MySQL. They are same tto the non
custom option with additional ability to choose OS and SSH to machine.

#### RDS read replica and Multi AZ

Read replica is an async operation that is able to scale read up to 15 instance
across AZ or within same AZ or across region (note cross region is chargeable).
Async nature results in the read replicas are eventual consistent. These
replicas can be promoted into their own. Connection string will be different
for the replicas. Backup are not configure by default.

Multi AZ option is a sync operation meant for disaster recovery by using a
single DNS name for failover (one connection string). Such active backup
increases the availability. Failover happens when there is a network issue,
or AZ loss or instance/storage failure without manual intervention. Note that
there is no read/write capacity improvement, the backup will only come online
when a failover happens.

> multi AZ availability option allows to have 1 or 2 standby DB instance, named
> multi AZ instance deployment and multi AZ cluster deployment. The latter can
> serve read traffic.

A combination of read replica and multi AZ can be used to gether to have a 1 +
1 (backup) + 15 read replica RDS cluster. A multi region deployment read
replica is used as failover **????

It is possible for RDS to be promoted from single AZ to multi AZ with no
downtime by modifying the database option. RDS will take a snapshot of database
and reestore it in a new AZ and run a sync between two instance.

#### RDS Proxy

Fully managed database proxy for RDS to allow pooled connection to database.
Good use case when having thousands of lambda functions. It improves the
database efficiency by reducing stress on database resource and minimized
open connections. RDS proxy is able to auto scale and is high available through
multiple AZ. It improved the failover time ~66%. Supports RDS and Aurora. It
enforces IAM authentication and credentials are stored in AWS secrets manager.
RDS proxy is never publicly acccessible, traffic must be from VPC.

#### Aurora

Database compatible to postgres and mysql that is cloud optimized (generally
better than their RDS counterpart). Auto scales storage in increments of 10 -
128 GB with scaling policy. Can have up to 15 read replicas with ~10ms of
replica lag. The read replica can be promoted as master and read replica can be
in different region. Supports failover and is natively high available at the
cost of +20% cost of RDS. Patching are done automatically with zero downtime.

By default an aurora cluster create 6 copies of data across 3 AZ. 4 out of 6
copies are needed for write and 3 out of 6 for reads. Aurora has self healing
capabilities through peer to peer replication. The data is stored in hundreds
of volumnes.

Aurora provides a write endpoint DNS for master and a reader endpoint DNS with
connection load balancer. Custom endpoints can be created for different use
cases e.g. OLAP etc. When custom endpoints is used, the default reader endpoint
should not be used. With custom enpoints that is meant for OLAP more powerful
machine can be used.

Aurora's replica auto scaling can be done through metric monitoring e.g. cpu
usage and creates more read replica under the same reader endpoint.

Aurora has a serverless option that scales based on actual usage meant for
unpredictable usage. It is a pay per second cost model.

Aurora machine learning integration allows user to make ML based prediction
with sql-like query through integration with SageMaker and Comprehend. Use
cases including fraud detection, recommendations, sentiment analysis and etc.

##### Aurora Global Database

Aurora global database is a service that have 1 primary region for (read/write)
and up to 5 read only region with ~1s replication lag. For each region up to 16
read replica is possible. Promoting another region for disaster recovery has an
RTO of < 1 minute.

> Aurora cross region replication and Aurora global database's difference is
> Aurora global database uses physical level replication while the prior uses
> logical level replication.

##### Aurora Database Clonning

Creates a new one from the existing one for testing/development purposes. Uses
a copy on write protocol which results in no copy until updates are made to the
new database cluster. Storage is only then allocated and data is copied. This
allows clonning to be fast and cost effective.

### Backup For RDS And Aurora

| - | RDS | Aurora |
|-|-|-|
| auto backup (1 - 35 days) | daily backup during backup window, transaction log every 5 minute | cannot be disabled |
| PITR recovery | Y | Y |
| manual snapshot (retain as long as possible) | Y | Y |

A trick to save cost on RDS is to create snapshot and delete database if usage
is 0 for some time. RDS charges as long as instance are up.

Restoring snapshots creates a new database. Backup can be created for on prem
database and restore to cloud through S3. Note that for Aurora cluster, Percona
XtraBackup is needed.

### Security For RDS And Aurora

At rest, data are encrypted using KMS (defined during creation time). If master
is not encrypted, replication will not be encrypted. To encrypt unencrypted
database, snapshot and restore (EBS).

At flight TLS is ready and uses AWS TLS root certificate.

IAM authentication is available and IAM roles can be defined. Security group
can help to filter unwanted connections and audit log can be enabled to send to
CloudWatch.

## ElastiCache

Managed redis and memcached that gives high performance and low latency
(submiliseconds). Helps to reduce load on database and makes application
stateless (potentially balance the EC2 instances). Supports cache invalidation
strategy for data update.

| feature | Redis | Memcached |
|-|-|-|
| multi AZ | Y | N |
| read replica (scale read/HA) | Y | N |
| data durability (AOF)/ persistent | Y | N |
| backup and restore | Y | N |
| supports sets and sorted sets | Y | N |
| multi node partition/sharing | N | Y |
| multi threaded | N | Y |

### ElastiCache Security

| feature | Redis | Memcached |
|-|-|-|
| IAM Authentication | Y | N |
| IAM policy (AWS api level security) | Y | Y |
| user/pw | Y (redis AUTH) | ? |
| security group | Y | Y |
| SSL in flight | Y | Y |
| SASL | N | Y |

### Patterns For ElastiCache

- lazy loading: all read to cache (stale cache and cache invalidation)
- write-through: add/update data in cache when updated to database (no stale)
- session store: store user session (TTL)

Special use case of Redis - gaming dashboard using sorted sets to track real
time top-1. Redis sorted set guarantee uniqueness and ordering.

## nosql vs sql

SQL supports join, sql query statements.

## aurora vs rds

- aurora manages more (spin up and go with preset)
- aurora handles load better
- rds more configs
- rds on ssd

## MISC

| database | port |
|-|-|
| pg | 5432 |
| oracle | 1521 |
| mysql/mariadb | 3306 |
| mssql | 1433 |