# MISC Services

## CloudFormation

> deploying and managing infrastructure at scale

A declarative way that outlines AWS infrastructure for almost any resources.
Once declared AWS will bring the services up in the right order and the exact
configuration specified. This promotes Infrastructure as Code approach,
ensuring infrastructures are not handled manually to prevent resource wastage.
All changes to infrastructure are reviewed through code. CloudFormation will
tag a identifier tag on the stack that allows for cost review. In addition,
special development tag can be automated for deletion beyond office hours to
save some cost (recreate them just before office hour). The entire
infrastructure can be bring up and destroyed on the fly which leads to
productivity improvement. Automated diagram of infrastructure generation is
also provided (CF Stack Designer). There exists CloudFormation templates and
documentation for leveraging. For those resources that are not supported,
"custom resources" can be used instead. Note that the service has to be used in
`us-east-1`.

> declarative programming removes the need of figuring out the correct ordering
> of which services to bring up first

### Service Role

Service role is an IAM role to allow CloudFormation to make changes (C/U/D)
stack resources on the user's behalf. It gives users the ability to work with
the stack resources even if they have no permissions to. This allows a least
privilege principle approach to access control by only giving users to
`iam:PassRole` permissions.

## AWS Simple Email Service

Fully managed service to send email securely and globally at scale. Both
outbound/inbound emails are supported. It gives

- reputation dashboard
- performance insight
- anti-spam feedback
- statistics: email delivery/bounces/feedback loop results/email open etc.
- supports DomainKeys Identified email (DKIM) and Sender Policy Framework (SPF)
- flexible IP: shared, dedicated and customer owned IPs
- send with with AWS console, APIs or SMTP

A few use cases including transactional, marketing and builk email
communications.

## Amazon Pinpoint

A scalable 2-way (inbound/outbond) marketing communication service. Supports
email, SMS, push notification, voice and in-app messaging. It has the ability
to segment and personalize messages with right content to customers. It can
receive replies and scales to billions of messages per day.

Compared to SNS or SES, its a managed service. PinPoint user will only need to
create message templates, specify delivery schedule, create target segment and
full campaigns and the rest will be handled by PinPoint. It is a good use case
for running campaigns through sending bulk transactional marketing SMS.

## Systems Manager (SSM)

### Session Manager

Allows user to start secured shell on EC2 and on prem servers. No SSH access,
bastion hosts or SSH keys needed (thus no need port 22). Supports Linux, macOS
and Windows. It can send session log data to S3 or CloudWatch Logs. This is
achieved by having SSM agent on EC2 instance and appropriate role for the
instance.

### Run Command

Execute a document (script) or a command and can be run across multiple
instances using resource groups. It relies on the SSM Agent to achieve thus
must be registered with Systems Manager service (Fleet management). No SSH
needed and all output can be shown in AWS Console, send to S3 or CloudWatch
Logs. Command status can be send as notifications to SNS. It is fully
integrated with IAM, CloudTrail and EventBridge.

![run cmd](run-cmd.PNG)

### Patch Manager

Automates the process of patching managed instance including OS/app/security
updates. Supports EC2 instances and on prem servers on all major OS platform.
Patches can be on demand or scheduled using Maintenance Windows. It also offers
instances scan and generates a patch compliance report for missing patches.

### Maintenance Windows

Defines a schedule for when to perform actions on instances (refer Patch
Manager) by providing

- schedule
- duration
- set of registered instances
- set of registered tasks

### Automation

Simplifies common tasks e.g. maintenance, deployment and etc of EC2 instances
and other AWS resources. Automation Runbook/SSM documents defines the action to
perform on the resources (pre-defined/custom).

![ssm auto](ssm-auto.PNG)

## AWS Cost Explorer

A service to visualize, intepret and manage AWS costs and usage over time.
Custom reports can be created for analytical purpose of total cost across all
accounts with high granularity (time and resource level). Provides savings plan
to choose from for cost optimization. Usage can be forecast up to 12 months
based on previous data points.

## AWS Batch

Fully managed batch processing at any scale e.g. running 100,000 batch jobs on
AWS efficiently. It launches EC2 instances or Spot Instances dynamically. It
will provision the right amount of compute/memory based on the submitted jobs
which are defined as Docker images and runs on ECS. Jobs can be started
on-demand or scheduled. It can be useful for cost optimization and focus less
on infrastructure.

### Batch vs Lambda

| batch | lambda |
|-|-|
| no time limit | limited time |
| as long as its an Docker image | limited runtime |
| EBS/instance store | limited disk space |
| AWS managed EC2 | serverless |

## AWS AppFlow

Fully managed integration service that enables transferring data securely
between SaaS applications and AWS. Sources can be SalesForce, SAP, Zendesk,
Slack, ServiceNow and destination can be AWS service (S3, Redshift) or
SnowFlake, SalesForce. The triggering can be set on schedule or in response to
event or on demand. Data transformation capabilities e.g. filtering and
validation can be done with AppFlow. Data are transferred over the public
internet or privately over AWS PrivateLink encrypted.

## AWS Amplify

> web and mobile application development tool

Authentication, Storage, API (REST, GraphQL), CI/CD, Pub/Sub, Analytics, AI/ML,
monitoring and etc. Able to connect to source code management online repository
e.g. GH, BB or direct upload.

![amp](amp.PNG)

## AWS Truster Advisor

Provides a high level AWS account assessment without any installation. It
analyzes AWS account and provide recommendations on the following 6 categories,

- cost optimization
- performance
- security (partial)
- fault tolerance
- service limits (partial)
- operational exellence

There is a free tier and a Business/Enterprise support plan for a full range of
checks with api access using AWS support API.

## AWS X-Ray

Service for developer to analyze and debug distributed application through logs
collected from underlying services. It is an end to end view of requests and
shows a map of as request is being handled. It relies on the SDK on the app or
ECS task that communicates traces to X-Ray agent that forwards to AWS X-Ray
service. Alternatively OpenTelemetry can be used. Dashboards that works similar
to Splunk (Splunk QL) is provided. X-Ray group can be created for a subset of
services and publish the notification when threshold is breached.