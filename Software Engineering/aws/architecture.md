# Architecture

AWS EC2 instance are associated with emphemeral IPv4 IP address. To ensure
the IPv4 address always point to EC2 instance, elastic IP can be used (static),
5 per account. Using elastic IP are usually indicator of bad design, instead
use random public IP + DNS or load balancer with no public IP at all.

## Simple Web App

![arch 1](arch-1.PNG)

If ELB is used alias record is suitable, if user is directly hitting public
EC2 instance A record will do the job (with R53).

ASG can further improved by having multi AZ deployment -> high availability

Reserve capacity for cost optimization + on demand

### With Database

![arch 2](arch-2.PNG)

User information is stored in client browser with ELB sticky session. Note if
EC2 instance is terminated, the user session will be invalid.

Cache with ElastiCache for fast retrieval. For cache miss check RDS and update
to ElastiCache. ElastiCache can set TTL. ElastiCache alternatively can be used
as server side session. This is useful if user cookie is > 4kb.

alternatively,

![arch 3](arch-3.PNG)

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
- applicaiton version
- environment(s)
  - collection of AWS resource (only one application at a time)
  - tiers (web/worker)

BeanStalk deployment is done by CloudFormation.

## ECS

With EventBridge, fully serverless architecture for image processing.

Event based

![ecs 1](ecs-1.PNG)

or schedule based

![ecs 2](ecs-2.PNG)

With SQS

![ecs 3](ecs-3.PNG)

Combining both SNS and EventBridge

![ecs 4](ecs-4.PNG)

## Serverless

### serverless architecture 1

Requirements

- serverless
- expose REST api with HTTPS
- user directly interact with their own folder in S3
- user authenticate with serverless service
- user can read/write but mainly read
- database should scale and have high read throughput

![arch 4](arch-4.PNG)

### serverless architecture 2

- website that scale globally
- rare write and often read
- some of the site is pure static files and the rest is dynamic REST API
- caching whenever possible
- welcome email for new users
- thumbnail generated for all photo uploaded

![arch 5](arch-5.PNG)

## Microservice

Requirements

- service interact with each other using REST api
- each service's architecture may vary in form and size
- a microservice architecture with leaner development lifecycle

![arch 6](arch-6.PNG)

> note the above is a synchronous pattern, async can be applied with SQS,
> Kinesis, lambda triggers (S3) and etc

## Software Update Offloading

EC2 that distributes software update, lots of request when ned update is out.
Prefers minimum changes to application but would like to optimize cost and CPU.

![arch 7](arch-7.PNG)

Network cost and ASG is minimized and the updates are cached at edge.

## Big Data Ingestion Pipeline

requirements

- fully serverless
- real time data collection
- data xfromation
- query the xformed data using SQL
- report created using queries should be in S3
- data to be loaded into warehouse and create dashboards

![arch 8](arch-8.PNG)

## S2S VPN Connection as Backup

![dx s2s](dx-s2s.PNG)

## Shared DX Between Multiple Accounts

![dx mul](dx-mul.PNG)
