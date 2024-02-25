# Disaster Recovery

Any event that has a negative impact on the company's business continuity or
finances is a disaster. Disaster recovery is about preparing for and recovering
from a disaster.

- on prem to on prem
- on prem to cloud (hybrid recovery)
- cloud region A to cloud region B

Two key metric to look at are

- Recovery Point Objective (RPO)
  - how often backup is run? to which checkpoint can be recovered?
  - how much of data loss business can accept? 1 hour? 1 minute?
- Recovery Time Objective (RTO)
  - how fast can system recover from disaster? (total down time)

## Disaster Recovery Strategies

| strategy | (relative) RTO | (relative) RPO | (relative) price |
|-|-|-|-|
| backup and restore | 8 | 8 | 1 |
| pilot light | 4 | 4 | 2 |
| warm standby | 2 | 2 | 4 |
| hot site/multi site approach | 1 | 1 | 8 |

### Backup and Restore

- not managing infrastructure before disaster and creates as disaster happens
- high RPO implies more data loss
- only data storage cost

![bu res](bu-res.PNG)

### Pilot Light

A small verion of app, usually the critical core, is always running on cloud.
Similar to backup and restore, but slightly faster as the critical core is
already up. Some additional cost for running the critical core (e.g. RDS below)
and when disaster happen R53 will failover + bring up EC2.

![p l](p-l.PNG)

### Warm Standby

Having a full system up and running at minimum size. Similar to Pilot Light
upon disaster system is scaled up to production load.

![w s](w-s.PNG)

### Hot Site/Multi Site Approach

Very low RTO and very expensive by having full production scale on AWS and on
prem.

![m s](m-s.PNG)

### AWS Multi Region

![aws a r](aws-a-r.PNG)

## Disaster Recovery High Level Overview

- backup
  - EBS snapshots, RDS automated backups/snapshots
  - regular S3 ingestion + lifecycle policy, cross region replication
  - snow family/storage gateway for on prem
- HA
  - R53 to migrate DNS region to region
  - RDS multi-AZ/Elasticache multi-AZ/EFS/S3
  - S2S VPN + DX
- replication
  - RDS (cross region) replication, AWS Aurora (global) database
  - database replication from on prem to RDS
  - storage gateway
- automation
  - CloudFormation/Elastic Beanstalk to recreate entire environment
  - recover/reboot EC2 with CloudWatch Alarm
  - lambda function for customized automation
- chaos testing

## On Prem Strategy With AWS

- download AMI as VM/.iso format that is compatible with VMWare etc
- VM import/export
  - migrate existing VM to EC2 (DR strategy for on prem VM)
  - export VM back to on prem
- AWS Application Discovery Service
  - gather information about on prem server to plan migration
  - server utilization and dependencies mappings
  - track with AWS Migration Hub
- ![AWS DMS](database.md#database-migration-service)
- AWS Server Migration Service
  - incremental replication of on prem live server to AWS

### AWS Application Discovery Service

- agentless discovery (AWS agentless discovery connector)
  - VM inventory, config, performance history (CPU, RAM, disk usage etc)
- agent based discovery (AWS application discovery agent)
  - sys config, sys performance, running process, details of network connection

### AWS Application Migration Service (MGN)

Lift and shift (rehost) solution to simplify migration to AWS from physical,
virtual or other cloud. Supports wide range of OS, platform and databases.
Minimal downtime with reduced cost. Once the system is completed replicated
while running in low cost instance, a cutover can be performed to scale it back
to production.

## AWS Backup

A fully managed service to automate backup to S3 across supported AWS services.
No custom scripts or manual process required. Cross region and cross account
backups are possible.

> once created AWS resources must be assigned to the plan to kickstart backup

- supports PITR is the service is compatible
- on demand backup and scheduled backup
- tag based backup policies
- create backup policies knowns as backup plans
  - backup frequency
  - backup window
  - transition to cold storage
  - retention period

AWS Backup has a Vault Lock feature to enforce WORM state for the backups. It
is an additional layer against malicious delete operation or updates that
modify the retention period. Root user will not be able to delete when enabled.

## Transferring Large Amount of Data To AWS

200TB with 100Mbps internet connection

- over internet/S2S VPN
  - immediate setup
  - 200(TB) * 1000(GB) * 1000(MB) * 8(Mb)/100 Mbps = 185 days
- over DX 1Gbps
  - over a month to setup
  - 18.5 days
- over snowball
  - ~ a week for end to end transfer, get 2 - 3 for parallelism
  - combine with DMS
- on going replication and leverage on S2S VPN/DX/DataSync

## VMware Cloud on AWS

Customers using VMware Cloud managing on prem data center can extend data
center's capacity to AWS while keeping VMware Cloud software. This allows

- migrating VMware vSphere-based workloads to AWS
- run production workloads across VMware vShpere private/public/hybrid cloud
  - together with access to AWS service
- as a disaster recovery strategy