# Alert and Health Monitoring

## CloudWatch

### CloudWatch Metrics

Provides metrics for every services in AWS. These metrics are essentially
variables that any stakeholder of the project cares about, it can be
`CPUutilization` etc. Metrics belongs to namespaces and a dimension is an
attribute of a metric (instance id, environment etc.). A metric can have up to
30 dimensions and have timestamps. CloudWatch dashboards can be created for
monitoring. Also custom metrics can be created.

#### CloudWatch Metric Streams

Stream CloudWatch metrics to a destination of choice in near real time delivery
and low latency with KDF or to 3rd parth service provider e.g. datadog. There
is an option to filter metrics such that only a subset of them is streammed.

> default is every 5 minutes and with detailed monitoring enabled per minute
> metric is gathered.

### CloudWatch Logs

To store logs in AWS. Log groups must be first defined with some arbitrary name
that usually represents the app. Within a log group, multiple log stream that
represents log instances within the application/containers/logs. Expiration
policy (never expire, 1 day to 10 years) can be defined for log purging. These
logs can be send to

- S3
- KDS/KDF
- lambda
- OpenSearch

The logs are encrypted by default, KMS-based encryption with custom keys is
also possible. Sources for CloudWatch Logs including CW Logs SDK, CloudWatch
Logs Agent and CloudWatch Unified Agent (to be deprecated). Elastic Beanstalk's
containers log collection, AWS lambda's function log, VPC logs, CloudTrail
(optional filter) logs, R53 DNS query logs and etc are sent to CloudWatch Logs.
Logs in CW Logs can be queried using CloudWatch Logs Insights for data
analyzation purposes. Visualization and raw data (log lines) are presented
(imagine splunk) using a purpose-built query language.

> note that it is an query engine not a real time engine.

CloudWatch Logs' S3 export can take up to 12 hours to complete with the api
call `CreateExportTask` in a batch manner. For real time purposes use Log
Subscriptions instead. Similarly these real time data can be sent to KDF/KDS or
lambda. A subscription filter can be applied.

Multiple log groups in different AWS accounts can be queried from. Using CW
Logs Subscriptions' cross-account subscription to send log event. A destination
access policy  and a cross account IAM role are created to enable data sending
from the sender AWS account.

Live Tail is a feature that listens to incoming live logs with a filter and
presents on the UI.

#### CloudWatch Logs/Unified Agent

By default no logs from EC2 machine is pushed to CloudWatch. A CloudWatch Agent
can help to push the logs, with appropriate IAM role to push to CW Logs. The
same agent can be setup on on-prem servers.

- (old) CW Logs Agent can only send to CW Logs
- (new) CW Unified Agent collects system level metrics (RAM etc) and send to CW
  - can be easily configured using SSM Parameter Store
  - more fine grained than ootb EC2 metrics

### CloudWatch Alarms

Used to trigger notifications any any metric with various options (%, max, min
and etc) and 3 states (OK, INSUFFICIENT_DATA and ALARM). Period defines the
length of time to evaluate the metric in multiple of 10 or 60 seconds.

CloudWatch Alarm has 3 targets

- to stop/reboot/recover/terminate an EC2 instance
- to trigger auto scaling action
- send notification to SNS

> EC2 instance recovery from status check (instance or system status) can
> ensures same private/public/elastic IP, metadata and placement group on
> different host.

Composite Alarms monitors states of multiple alarms using `AND` and `OR`
conditions. Complex composite alarms is possible to reduce noise.

> testing CW Alarm can be done by manually setting alarm state to Alarm using
> CLI commands

### Amazon EventBridge

rules:

- can be used to schedule cron jobs (time based)
- react to some event pattern

It is the default event bus (routes events to zero or more destinations). There
exists partner event bus to send events from AWS SaaS partners into AWS and an
option to create custom event bus. Event buses can be accessed by other AWS
accounts using resource-based policies. Events can be archive (optional
filtering) sent to an event bus (indefinitely or some period retention). These
archived events can be used for replay.

> a use case for EventBridge resouce based policy is to enable all event in
> an AWS organization to put the events to a single AWS account/region.

EventBridge can analyze the event in bus and infer schema. Schema Registry
allows to generate code for application and can be versioned.

### CloudWatch Insights

#### Container

Collect, aggregate and summarize containers metrics and logs from

- ECS
- EKS
- kubernetes platforms on EC2
- Fargate (ECS/EKS)

CloudWatch Insights for kubernetes (EKS/Kube on EC2) uses a containerized CW
agent to dicover containers.

#### Lambda

System level detailed metrics aggregation and summarize into diagnostic
information e.g. cold starts or shutdowns.

#### Contributor

Create a time series analysis of any AWS generated logs to see the metrics'
top-N contributors which helps system performance impact contributors. E.g.
heaviest network users/host from VPC logs. AWS provides some analysis
templates for reference.

#### Application

Automated dashboard to show potential problem of monitored application to
isolate ongoing issues for

- selected technologies running on EC2
- AWS resources (SNS/RDS and etc)

powered by SageMaker. Findings and alerts are sent to EventBridge and SSM
OpsCenter.

## CloudTrail

A global service enabled by default to provide governance, compliance an audit
for AWS accounts by tracking the history of events and api calls made within
AWS accounts. These calls can be from

- console
- SDK
- CLI
- AWS services

and the logs can be pushed into CloudWatch Logs and S3. A trail can be applied
to all regions (default) or single region. There are 3 main type of CloudTrail
events

- Management events
  - logged by default for operation performed on AWS resources
    - configuring security/rules/setup logging
  - can be separated by read and write events
- Data events
  - high volume, by default is diasbled
    - S3 object level activity (get, put etc)
    - lambda function activity
  - can be separated by r/w
- CloudTrail Insights events
  - mgmt event can also be high volume, use insights to detect unusual activity
    - inaccurate resource provisioning
    - service limit
    - burst of IAM actions
    - gaps in periodic maintenance activity
  - analyze normal mgmt event as baseline and write events for unusual pattern
    - these insights events is sent to CT console/S3/EventBridge

All events by default are stored for 90 days in CloudTrail. For retention
beyond 90 days, log them to S3 (and use Athena)

### EventBridge Integration

![ct-eb-int](ct-eb-int.PNG)

## AWS Config

A per region service that helps with auditing and recording compliances of AWS
resource's configuration over time. E.g.

- unrestricted SSH access to security groups
- S3 bucket created with public access
- ALB config changes

Receive Config notifications if there is any changes through EventBridge or
SNS. Rules that can be configured including AWS managed config rules and custom
config rules that must be defined in AWS lambda. These rules can be evaluated
when there is a change or periodically.

> note that config rules are not for preventing action from happening.

Despite no denying of action happening, remediations can be automated for non
complaint resource using SSM automation documents (AWS managed or custom,
basically lambda fn). Remediations can have retried if the resource is still
non compliant after auto-remediations. Compliance of resource, configuration of
resource and CloudTrail api call of resource over time can be viewed in the UI
(timeline format).

Data can be aggregated across regions and accounts. Configs can be stored into
S3 and subsequently analyzed with Athena. It can get expensive quickly,

- $0.003 per configuration item per region
- $0.001 per config rule evaluation per region
