# Architecture

AWS EC2 instance are associated with emphemeral IPv4 IP address. To ensure
the IPv4 address always point to EC2 instance, elastic IP can be used (static),
5 per account. Using elastic IP are usually indicator of bad design, instead
use random public IP + DNS or load balancer with no public IP at all.

## Simple Web App

```mermaid
graph LR
    subgraph WWW
    R53 <---> u[users]
    end
    subgraph AZ
    u ---> e[ELB]
    end
    subgraph "Auto Scaling Group"
    e ---> ec1[ec2-1]
    e ---> ec2[ec2-2]
    end
```

If ELB is used alias record is suitable, if user is directly hitting public
EC2 instance A record will do the job (with R53).

ASG can further improved by having multi AZ deployment -> high availability

Reserve capacity for cost optimization + on demand

### With Database

```mermaid
graph LR
    subgraph WWW
    R53 <---> u[users]
    end
    subgraph AZ
    u ---> e[ELB]
    end
    subgraph "Auto Scaling Group"
    e ---> ec1[ec2-1]
    e ---> ec2[ec2-2]
    end
    subgraph Cache
    ec1 ---> ecc[ElastiCache Cluster]
    ec2 ---> ecc
    end
    subgraph Database
    ec1 ---> RDS[RDS multi AZ + read replica]
    ec2 ---> RDS
    end
```

User information is stored in client browser with ELB sticky session. Note if
EC2 instance is terminated, the user session will be invalid.

Cache with ElastiCache for fast retrieval. For cache miss check RDS and update
to ElastiCache. ElastiCache can set TTL. ElastiCache alternatively can be used
as server side session. This is useful if user cookie is > 4kb.

alternatively,

```mermaid
graph LR
    subgraph WWW
    R53 <---> u[users]
    end
    subgraph AZ
    u ---> e[ELB]
    end
    subgraph "Auto Scaling Group"
    e ---> ec1[ec2-1]
    e ---> ec2[ec2-2]
    end
    subgraph Aurora
    ec1 ---> a[Aurora multi AZ + read replica]
    ec2 ---> a
    end
    subgraph "EBS/EFS"
    ec1 ---> EBS
    ec2 ---> EBS
    end
```

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

```mermaid
graph LR
  client -- upload ---> S3
  S3 -- event ---> aeb[EventBridge]
  aeb -- run task ---> et[ECS task]
  et <-- get from S3 --> S3
  et -- save to ---> DDB
```

or schedule based

```mermaid
graph LR
  aeb[EventBridge] -- scheduled run task ---> et[ECS task]
  et -- save to ---> S3
```

With SQS

```mermaid
graph LR
  msg ---> sqs
  sqs -- poll for message ---> et[ECS task]
```

Combining both SNS and EventBridge

```mermaid
graph LR
  ecs[ECS cluster] -- task exited ---> eb[EventBridge]
  eb ---> SNS
  SNS -- email --> admin
```

## Serverless

### serverless architecture 1

Requirements

- serverless
- expose REST api with HTTPS
- user directly interact with their own folder in S3
- user authenticate with serverless service
- user can read/write but mainly read
- database should scale and have high read throughput

```mermaid
graph LR
  client ---> agw[AWS API gateway]
  agw -- cache ---> agw
  client <-- authenticate/authorize --> ac[AWS Cognito/AWS STS]
  agw <---> ac
  agw ---> lambda
  lambda ---> d[DAX/DDB]
  client -- store/retrieve --> S3
```

### serverless architecture 2

- website that scale globally
- rare write and often read
- some of the site is pure static files and the rest is dynamic REST API
- caching whenever possible
- welcome email for new users
- thumbnail generated for all photo uploaded

```mermaid
graph LR
  client <---> CloudFront
  CloudFront <-- origin access control --> s[S3 with bucket policy only CF dist]
  client ---> agw[API gateway]
  agw ---> lambda
  lambda ---> d[DAX/DDB/DDB global table]
  d ---> ddbs[DDB stream]
  ddbs ---> l[lambda]
  l ---> ses[Simple Email Service]
  client ---> s2[S3 transfer acceleration]
  s2 ---> l2[lambda]
  l2 -- thumbnail --> S3

```

## Microservice

Requirements

- service interact with each other using REST api
- each service's architecture may vary in form and size
- a microservice architecture with leaner development lifecycle

```mermaid
graph LR
  client ---> R53
  client -- https --> ELB
  subgraph "ELB route"
    ELB ---> ECS
    ECS ---> DDB
  end
  client ---> agw[API gateway]
  subgraph "API gateway"
    agw ---> lambda
    lambda ---> elasticache
  end
  client ---> ELB2[ELB]
  subgraph "EC2 route"
    ELB2 ---> ec2[EC2 + ASG]
    ec2 ---> RDS
  end
  ec2 -.-> agw
  lambda -.-> ELB
```

> note the above is a synchronous pattern, async can be applied with SQS,
> Kinesis, lambda triggers (S3) and etc

## Software Update Offloading

EC2 that distributes software update, lots of request when ned update is out.
Prefers minimum changes to application but would like to optimize cost and CPU.

```mermaid
graph LR
  client ---> CloudFront
  CloudFront ---> ELB
  ELB ---> ASG
  ASG ---> EC2
  EC2 ---> EFS
```

Network cost and ASG is minimized and the updates are cached at edge.
