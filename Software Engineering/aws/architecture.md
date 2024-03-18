# Architecture

AWS EC2 instance are associated with emphemeral IPv4 IP address. To ensure
the IPv4 address always point to EC2 instance, elastic IP can be used (static),
5 per account. Using elastic IP are usually indicator of bad design, instead
use random public IP + DNS or load balancer with no public IP at all.

## Simple Web App

![arch 1](../static/arch-1.PNG)

If ELB is used alias record is suitable, if user is directly hitting public
EC2 instance A record will do the job (with R53).

ASG can further improved by having multi AZ deployment -> high availability

Reserve capacity for cost optimization + on demand

### With Database/Cache

![arch 2](../static/arch-2.PNG)

User information is stored in client browser with ELB sticky session. Note if
EC2 instance is terminated, the user session will be invalid.

Cache with ElastiCache for fast retrieval. For cache miss check RDS and update
to ElastiCache. ElastiCache can set TTL. ElastiCache alternatively can be used
as server side session. This is useful if user cookie is > 4kb.

alternatively,

![arch 3](../static/arch-3.PNG)

EFS with multiple ENIs (bound to AZ, one per AZ). Similarly EBS works however
with a catch that its also bounded to AZ and connecting to instance might not
return data from another EBS. EBS is not suitable for distributed system.

### Quick Launch

Snapshot can allow quick restore of RDS and EBS.

## Elastic BeanStalk

Orchestration service by AWS that allow AWS components to be reused e.g. the
architecture above (R53, ELB and ASG). It manages capacity provisioning, load
balancing, scaling, health monitoring, instance configuration etc. Develop will
only need to focus on application code. The orchestration is still
configurable.

It uses managed containers that supports mainstream programming language
environment e.g. java, js, py and docker etc. on known web server e.g. tomcat,
nginx, httpd and etc. Once deployed, develoer can still replace part of system
as they like it. Think it as having infrastructure managed through tested
system configuration template.

There is two deployment mode, single instance for developmet (with elastic IP)
and high availability with load balancer for prod.

BeanStalk is made up of 3 components,

- application: collection of BeanStalk components (envs, versions, configs,...)
- application version
- environment(s)
  - collection of AWS resource (only one application at a time)
  - tiers (web/worker)

BeanStalk deployment is done by CloudFormation.

## ECS

With EventBridge, fully serverless architecture for image processing.

Event based

![ecs 1](../static/ecs-1.PNG)

or schedule based

![ecs 2](../static/ecs-2.PNG)

With SQS

![ecs 3](../static/ecs-3.PNG)

Combining both SNS and EventBridge

![ecs 4](../static/ecs-4.PNG)

## Serverless

### serverless architecture 1

Requirements

- serverless
- expose REST api with HTTPS
- user directly interact with their own folder in S3
- user authenticate with serverless service
- user can read/write but mainly read
- database should scale and have high read throughput

![arch 4](../static/arch-4.PNG)

### serverless architecture 2

- website that scale globally
- rare write and often read
- some of the site is pure static files and the rest is dynamic REST API
- caching whenever possible
- welcome email for new users
- thumbnail generated for all photo uploaded

![arch 5](../static/arch-5.PNG)

## Microservice

Requirements

- service interact with each other using REST api
- each service's architecture may vary in form and size
- a microservice architecture with leaner development lifecycle

![arch 6](../static/arch-6.PNG)

> note the above is a synchronous pattern, async can be applied with SQS,
> Kinesis, lambda triggers (S3) and etc

## Software Update Offloading

EC2 that distributes software update, lots of request when ned update is out.
Prefers minimum changes to application but would like to optimize cost and CPU.

![arch 7](../static/arch-7.PNG)

Network cost and ASG is minimized and the updates are cached at edge.

## Big Data Ingestion Pipeline

requirements

- fully serverless
- real time data collection
- data xfromation
- query the xformed data using SQL
- report created using queries should be in S3
- data to be loaded into warehouse and create dashboards

![arch 8](../static/arch-8.PNG)

## S2S VPN Connection as Backup

![dx s2s](../static/dx-s2s.PNG)

## Shared DX Between Multiple Accounts

![dx mul](../static/dx-mul.PNG)

## Event Processing

![arch evnt 1](../static/arch-evnt-1.PNG)

Note that the dead letter queue and lambda retry mechanism difference.

### Fan Out Pattern

![arch evnt 2](../static/arch-evnt-2.PNG)

### CloudTrail Event

![arch evnt 3](../static/arch-evnt-3.PNG)

### API Gateway and KDS

![arch evnt 4](../static/arch-evnt-4.PNG)

## Caching Strategies

![arch cache](../static/arch-cache.PNG)

> S3 and database has no caching abilities

## IP Blocking Strategies

Depending on the infrastructure, different means might fail.

![ip blck 1](../static/ip-blck-1.PNG)

![ip blck 2](../static/ip-blck-2.PNG)

![ip blck 3](../static/ip-blck-3.PNG)

## High Performance Computing (HPC)

Cloud can support HPC easily as large compute resource can be launched in a
snap. Resources can be added on demand and it follows a pay as you use model.

### Data Management & Transfer

- AWS Direct Connect
  - move GB/s data to cloud over private secure network
- snow family
  - moving PB of data to cloud
- AWS DataSync
  - file system to cloud

### Compute and Networking

EC2 is the main discussion point

- CPU/GPU optimized
- spot instances/spot fleets + auto scaling
- cluster placement group for networking
- EC2 enhanced networking (SR-IOV)
  - higher bandwidth, high packets per second, lower latency
  - (new) Elastic Network Adapter (ENA) up to 100 Gbps
  - (old) Intel 82599 up to 10 Gbps
- Elastic Fabric Adapter (EFA)
  - improved ENA for HPC, low latency and reliable, only linux
  - great for internode communication/tightly coupled workloads
  - leverages Message Passing Interface (MPI) standard through bypassing OS

### Storage

- instance attached storage
  - EBS: up to 256,000 IOPS with `io2`
  - Instance store: up to millions of IOPS
- network storage
  - S3: large blob, not file system
  - EFS: scaled IOPS with size or using provisioned IOPS
  - FSx for Lustre: millions of IOPS backed by S3 

### Automation and Orchestration

- AWS Batch
  - supports multi-node parallel jobs to run single job that spans multiple EC2
  - easy to schedule jobs and launch EC2 instances
- AWS ParallelCluster
  - open source cluster management tool to deploy HPC on AWS
  - configure with text file
  - automate creation of VPC, subnet, cluster type and instance type
  - ability to enable EFA on cluster to improve network performance

## High Availability for EC2

With CloudWatch + Lambda

![ec2 ha 1](../static/ec2-ha-1.PNG)

Without CloudWatch/With ASG + user data to attach EIP (IAM role for attaching)

![ec2 ha 2](../static/ec2-ha-2.PNG)

Using ASG's lifecycle hook

![ec2 ha 3](../static/ec2-ha-3.PNG)

## Well Architected Framework

Six pillar

- operational excellence
  - monitoring systems, continually improving
  - automating changes, responding to events and defining standards to manage operations
- security
  - proctecting information and systems
  - data confidentiality and integrity
  - user permission
  - establish control to detect security events
- reliability
  - workload to perform intended function
  - recovery from failure quickly to meet demand
  - distributed system design, recovery planning
  - adapting to changing requirements
- performance efficiency
  - structered and streamlined allocation of resources
  - right resource type and size for the requirement
  - maintaining efficiency as business evolve
- cost optimization
  - avoiding unnecessary costs
  - understand spending over time and control fund allocation
  - select resource of right type and quantity
  - scale to meet business without overspending
- sustainability
  - minimize environmental impact of running cloud workloads
  - understand and reduce impact, maximize utilization and minimize required resource
