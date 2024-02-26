# Compute Services

## EC2

Virtual machines for rent with full customization on OS, cpu, ram, network
options, firewall rules and security groups.

EC2 allows user to define boostrap script known as "EC2 user data" to run at
instance launch that runs as `root` user.

### EC2 lifecycle

- launch
- stop (hibernate): instance state is kept and no billing
- terminate

When started, the OS boots and runs EC2 user data if any. Subsequently any
user defined application is launched together with cache warm up. In stop 
state, EC2 instance's data on disk is persisted until the next start.
Terminating EC2 will results in destroying the root volume. In order for
speeding up boot hibernation can be utilized. The ram's state is perserved
which results in not required to boot OS. This is done by writing the ram state
into a file in the root EBS volume, as long as it is large enough and is
encrypted. This helps to resume long running processes with/and critical ram
state application through fast booting.

Relaunch a stopped instance will results in change of external IP address.

EC2 instance naming is intepreted as
`{instance class}{generation}.{size within instance class}` e.g. `M2.2xLarge`.

### Instance Classes

- general purposes (`T*`)
  - code repo, web app
- compute optimized (`C*`)
  - batch processing, media transcodeing, HP web/HPC, modeling/ML, gamming
- memory optimized (`R*`)
  - HP database, cache, in memory database, real time processing unstructured data
- storage optimized
  - low latency, high IOPS local storage read/write access
  - OLTP, SQL/noSQL, in memory database, data warehouse app, distributed file system

### Purchasing Options

| name | short description | discount | cost | upfront payment |
|-|-|-|-|-|
| on demand | uninterupted short workload, predicted pricing by second | NA | highest | NA |
| reserved (1/3 years) | reserves instance by attribute (os, type, region etc), convertible option for flexible instances, can be regional or zonal | ~72% or ~66% for convertible | yes |
| savings plan (1/3 years) | commitment for usage e.g. $10/hour not instance type, exceeding is billed as on demand | ~72% savings | | no/partial/all upfront for various discounts |
| spot instance | short workload, emphemeral | ~90% |
| dedicated host | book entire physical server and placement, for compliance or server bound license | | highest, can be on demand or reserved |
| dedicated instance | not sharing hardware with others, may share hardware with other instance of same account, no control over placement |
| capacity reservation | reserve capacity in AZ and get charges regardless | on demand |

#### spot instance/fleet

Define a max spot price, a target capacity (instance, vCPU, ram) and per
instance attributes, get instance when current price is less than defined max
spot price. Instance is terminated or stopped when price is greater than
defined max spot price with 2 minute grace period.

![ec2 spt life](ec2-spt-lc.PNG)

> validate from/until can be infinite

Spot instance can only be terminated in `open`, `active`, `disable` state. User
should first cancel spot request before terminating the instance else new
instance will be created (cancelling spot request does not terminate instance).

Spot fleet: getting set of spot instance + optional on demend instances. It
tries to meet target capacity with price constraints. It launch the most
appropriate defined launch pool (can have multiple). It stop launch if max
cost or capacity is met.

Spot fleet allocation strategy

- lowest price: from all pool
- diversified: distributed from all pools (good for availability)
- capacity optimized: poll with optimal capacity for number of instances
- price capacity optimized: pool with highest capacity and then lowest price

(deprecated) spot block to get reserved 1-6 hours without interruptions.

### Security Group

Controls inbound/outbound traffic in EC2 with only allow rules. Can be
reference by IP (IPv4/v6) or another security group. Think if of as a port
firewall (UFW). Inbound/outbound rules are edited separately. Security group
can be one to many (resource) and limited to same VPC/peered VPC in same
region. Security group are statefull, a traffic once allowed inbound/outbound
is allowed on outbound/inbound.

> when troubleshooting, timeout are usually good indicators of incorrect setup.

### Placement Groups

- cluster: cluster instance into low latency group in single AZ (high network throughput on same rack, high risk of catastrophic failure)
- spread: spread instances across underlying hardware (max 7 per AZ) for HA
  - spread is for smaller number of EC2s
  - HA but not high performant (network cost)
  - one rack per instance
- partition: spread instances across many partitions (racks) within AZ, up to hundreds of EC2 per group and up to 7 partion in AZ
  - partition is more towards distributed systems e.g. kafka etc.
  - allows to launch in to specific partition
  - middle ground between HA, HPC and fault tolerance

## Amazon Machine Image (AMI)

Customized EC2 instance including software, OS, config, monitoring etc. for
fast boot/config time through prepackaging. AMI are bounded by region, and can
be copied across region. AWS marketplace can find AMIs for sale.

To create AMI first start EC2 instance in desired config and install desired
software. Stop the instance and build AMI by choosing `create image`.

## Application Scalability

Allow application to handle greater traffic by adapting through vertical and
horrizontal/elastic scaling. Scaling is related but not exactly high
availability. Vertical scaling examples including better spec, use of caching
and etc non-distributed approach. Horrizontal scaling examples including adding
more machines, running in distributed fashion with auto scaling group and load
balancer.

High availability implies running application in more than 1 data center/AZ.
HA can be active with horizontal scaling or passive with RDS multi AZ. Examples
like auto scaling group/load balancer in multi AZ.

> check [elastic load balancer](./network.md/#elastic-load-balancer-elb)

### Auto Scaling Group (ASG)

Scales in/out depending on traffic by ensuring minimum/maximum instances
running. ASG registers new instance with load balancer. ASG will try to
recreate EC2 instance that marked unhealty and gets termination signal from
ELB.

A launch template is requires for ASG to work with the following informations,

- AMI + instance type
- EC2 user data
- EBS volume
- security groups
- ssh key pairs
- scaling policy
- IAM roles
- network/subnet information
- load balancer information
- min/max capacity and initial capacity

Besides ELB, ASG can scale based on CloudWatch Alarms e.g. average CPU. The
metric is computed for overall ASG instance.

#### Scaling Policies

- dynamic scaling
  - target tracking scaling: ASG average cpu
  - simple/step scaling: CloudWatch alarm trigger and add/remove X units
  - scheduled action: anticipate traffic 11/11 etc
- pretictive scaling
  - continuous forecast and schedule ahead

In the scaling policy there is a scaling cooldown that default to 300s to
prevent scaling after scaling process completed/allow metric stabilization.

> TODO lifecycle hook

## AWS Lambda

A virtual, short executed (up to 15min) function that bills per call duration
and runs on demand. Scaling of the function is fully managed and well
integrated with lots of AWS services, many programming languages. It comes
with CloudWatch monitoring and it is possible to get more resource per
function. When one aspect of the resource increase e.g. RAM, CPU and network
will be improved at the same time.

Lambda supports a wide range of language and if there is no AWS support e.g.
Rust, there is a open sourced custom runtime api option. Also lambda container
image is supported as long as the container image implements the lambda
runtime api. If it is a arbitrary Docker image, ECS/Fargate is preferred to run
it instead.

(S3 event notification) Event triggered job

![s3 evnt noti](s3-evnt-noti.PNG)

Serverless CRON job

![eb lmda](eb-lmda.PNG)

Pricing is based on per calls and per duration.

- first 1Mil request are free
- $0.2 per 1Mil request thereafter

- 400,000GBs free
  - i.e. 400,000s if function requires 1GB RAM
  - or 3,200,000s if function requires 128MB RAM
- $1 per 600,000GBs

### lambda limitation

Lambda is region bounded service with some limitation with its execution and
deployment.

Execution

- memory allocation between 100MB - 10GB in 1MB increments
- maximum execution time of 15min
- 4kb of environment variables
- disk capacity in `/tmp` is 512MB - 10GB (for dependencies and etc)
- concurrency execution: 1000 (can be increased)

Deployment

- lambda function size (compressed .zip): 50MB
- lambda function size (uncompressed): 250MB

Lambda is launched in AWS VPC and cannot access the developers VPC. To get
access to private VPC, first enabled when creating function and specify the
VPC ID, subnet and security group. An ENI is created in subnet for the function
to access to resource within it.

Specifically for RDS, RDS proxy can be used to allow lambda connections and
address connection issue with there is a surge of lambda function. Lambda
function in this case must be launched within the same VPC as RDS proxy as it
is never publicly available. [1]

### Lambda SnapStart

Option to improve Java 11 and above performance by 10x with no extra cost. It
is achieved by using Java AOT.

![lmda ss](lmda-ss.PNG)

## Edge Function

Modern application might executes some logic at edge and this can be done with
Lambda@Edge and CloudFront function.  Executing code at edge ensure that it
runs close to the users and minimize latency. 

A few use case would be,

- modifying the content on the fly
- website security and privacy
- dynamic web app at the edge
- SEO
- across origin/data center routing
- bot mitigation at edge
- real time image transformation
- a/b testing
- user authentication and authorization
- user prioritization
- user tracking and analytics

CloudFront Function

![cf fn](cf-fn.PNG)

| CloudFront Function | Lambda@Edge |
|-|-|
| lightweight JS | written in nodeJS or PY |
| large scale, latency sensitive CDN customization | - |
| sub-ms startup time, millions of request per second | thousands of request per second |
| changes viewer request and response | changes viewer/origin request and response |
| native CF feature (code managed within CF) | - |
| - | author function in one region and CF replicates to all locations |
| max execution time < 1ms | 5-10s |
| max memory 2MB | 128MB - 10GB |
| totalk package size 10kb | 1MB - 50MB |
| no network/file system access | network/file system access |
| no access to request body | access to request body |
| free tier available, 1/6 of lambda@edge | no free tier, charged per request & duration |
| no access to 3rd party library and AWS services | access to 3rd party library and AWS services |
| limited CPU and memory | adjustable CPU and memory |

CloudFront function are usually used for

- cache key normalization (transform request headers/cookies/query strings/URL)
- header manipulation
- URL rewrite or redirects
- Request authentication and authorization (JWT create and validate to allow or deny request)

## Step Functions

Builds a serverless visual workflow to orchestrate lambda functions. It offers
feature like execution sequencing, parallel, conditions, timeouts, error
handling and etc. It ingetrates will with AWS services e.g. EC2, ECS, on-prem
servers, API gateway, SQS and etc. It allows human approval. A few use cases
including

- order fulfillment
- data processing
- web application

## MISC

ports to remember

| name | port number |
|-|-|
| ssh/sftp | 22 |
| ftp | 21 |
| http | 80 |
| https | 443 |
| rdp | 3389 |

[1]: https://aws.amazon.com/blogs/compute/using-amazon-rds-proxy-with-aws-lambda/