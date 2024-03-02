# Containers

## Elastic Container Service

Launching docker containers is equivalent to launching ECS Tasks on ECS
clusters i.e. `tasks = containers`.

For EC2 launch type, EC2 instances are launched within the ECS clusters. These
EC2 instances are manually provisioned and maintained. ECS agent must be
installed on it unless it is an ECS optimized AMI. With that AWS will take care
of starting and stopping tasks in the EC2 instances. ASG is required to be
defined when setting up ECS cluster. The ASG scaling can be done based on,

- CPU util
- add EC2 over time

or using new feature ECS cluster capacity provider that automatically provision
and scale the infrastructure for ECS tasks through the underlying ASG.

For fargate launch type, no EC2 instances required to be managed. It is
serverless. Task definition are created and AWS will run the ECS tasks based on
CPU/RAM required.

ALB is supported and works for most use cases to expose tasks within the ECS
clusters to users. NLB can be used for high throughput/performance use cases or
pairing it with AWS PrivateLink.

Persistence is achieve by mounting EFS on to ECS tasks. It is compatible with
both launch types. Task running in different AZ will share same data and it is
fully serverless (with fargate).

> note S3 is not a file system.

### IAM Roles

EC2 instance profile (for EC2 launch type) is used by ECS agent to access ECS
service, CloudWatch, ECR, Secrets Manager and etc.

ECS task role (both EC2 and fargate launch type) is created for each ECS task.
This allows different roles to be used for different ECS service and is defined
in the task definition.

### ECS Auto Scaling

Automatically scales the desired number of ECS tasks based on

- ECS service average CPU util
- ECS service average memory util
- ALB request count per target

through AWS Application Auto Scaling service. The scaling policies can be the
following,

- target tracking: based on target value on specific CloudWatch metric
- step scaling: based on CloudWatch alarm
- scheduled scaling: scale based on specific datetime

> note that scaling ECS tasks is not equivalent to scaling EC2 instances for
> EC2 launch type.

## Elastic Container Registry

Stores docker images on AWS, offers private and public repository. It is fully
integrated with ECS and backed by S3. Access is controlled by IAM. It supports
image vulnerability scan, versioning, image tags, image lifecycle out of the
box.

> Public ECR is known as Amazon ECR Public Galery

## Elastic Kubernetes Service

Alternative to ECS which launches a managed kubernetes cluster on AWS. It
manages automatic deployment, scaling and containerized application management.
Similar to ECS, it supports both EC2 and fargate launch type. Kubernetes is
cloud agnostic and is good to migrate from existing system that is on
kubernetes.

For the launch types, EC2 launch type supports

- managed node groups
  - EC2 instances are created automatically and part of ASG managed by EKS
  - supports on demand and spot instances
- self managed node
  - node created manually and registered to EKS cluster and managed by ASG
  - can be prebuild AMI

Data volume that are mounted to EKS must be container storage interface (CSI)
compliant and through specifying `StorageClass` manifest.

- EBS
- EFS
- FSx for lustre
- FSx NetApp ONTAP

## AWS App Runner

Fully managed service to deploy web app and api at scale without knowledge
about infrastructure. By providing containerize image or source code, App
Runner builds and deploys the web app. It handles scaling, HA, load balancing,
encryptions and etc. It has VPC access support and is able to connect to
databases, caches, message queue services and etc.
