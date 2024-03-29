# Middlewares

## Simple Queue System

Fully managed queue where producer connects with SDK or `sendMessage` api and
consumers poll the queue, process and delete the message (up to 10 at a time).
SQS has unlimited throughput and there is no limit of number of messages. Each
message has default of 4 days retention (if not processed/deleted) and maximum
up to 14 days. SQS has low latency < 10ms on each message's publish and
receive. It limits each message to be < 256kb. SQS guarantees at least once
delivery (duplicated message can be received by multiple consumers) and have
best effort message ordering.

Scaling can be done with ASG using CloudWatch on metrics e.g.
`approximate number of messages`. Provides encryption through HTTPS, and KMS
for data at rest. Also client side encryption is optional. Access control is
possible through IAM and SQS access policy for cross account and other AWS
services.

Consumers can choose to have a long polling connection to SQS to wait for a new
message. Such approach reduces latency and reduce poll count. This can be set
at queue level or at api level (consumer). Generally its between 1-20 seconds.

FIFO queue is available that guarantees message ordering but has a limited
throughput of 300 messages/s without batching and 3000 msg/s with batching. It
also guarantees exact once delivery by removing duplicates. SQS FIFO queue has
a message group features such that each consumer can request for a batch of
messages within the same message queue to be processed. FIFO queue **must** end
with suffix `.fifo` and it counts to the 80 character limit of queue name.

> 3000 msg/s is done by batching 10 messages together which is also the max

SQS can be used a buffers to database write when the traffic is high. It helps
decoupling the write operation to database from the application request.

> retries is possible with SQS i.e. when a message is not processed, it will be
> visible once the visibility has timeout to other consumers.

### Message Visibility

SQS at least once delivery is implemented using message visibility timeout.
When a message is polled, it is invisible to other consumers for some time (30s
default). It is possible for consumers to request extension of visibility
timeout through the change message visibility api if additional processing time
is required.

If visibility timeout is set for a large number, the reprocess of message will
be delayed if the consumer is crashed.

### Dead Letter Queue

Queue for messages that failed to be consumed successfully. Useful for
debugging. Configure maximum receives before sending to DLQ to a value between
1 and 1000.

## Simple Notification System

Fully managed pub/sub model where there is one producer and many consumers.
These consumer uses the messages differently (e.g. email, write to database
etc). With SNS, they will receive all the messages (optional filtering). Up to
12.5Mil subscription per topic and 100k topic limit per SNS. Security details
is same as SQS. SNS has a FIFO feature similar to SQS FIFO with same
throughput. Filtering is done through specifying a JSON policy, by default if a
subscription has no filtering policy it receives all messages.

SNS can be published to SQS, lambda, KDF, email/mobile notification, and HTTP
endpoints. Publishing into SNS can be done with topic publish through SDK by
creating a topic, creating a subscription and publish to topic. Alternatively,
mobile apps SDK can do a direct publish by creating a platform application and
endpoint, publish to platform endpoint (works with google GCM, apple APNS and
amazon ADM).

> SNS does not persist message, they are deleted once delivered

### Fanout Pattern with SNS and SQS

A single SNS topic is subscribed by multiple SQS queues such that once message
is pulished to SNS, the queues can process the messages. Appropriate policies
required to be in place. Such setup can be across region. Similarly, this
pattern can be applied to SNS + KDF or SNS FIFO + SQS FIFO (for fanout +
ordering + deduplication).

## Kinesis

AWS Kinesis is a suite of service for collect, process and analyze streaming
data in real time.

### Kinesis Data Stream

![kds](../static/kds.PNG)

> Number of shards is defined and provisioned ahead of time that serves as
> stream capacity.

For each incoming records there is a partition key and data blob up to 1MB at
1MB/s or 1000 message/s per shard. For each outgoing records there is a
partition key, sequence number and data blob. The outgoing records can be
consumed at 2MB/s per shard for all consumers or 2MB/s per shard per consumer
(enchanced/push data) if multiple consumers retrieving data form a stream in
parallel.

> KDS can not output directly to S3

KDS is a real time regional level streaming service with retention of 1-365
days. It has the ability to replay and is immutable (once inserted and cant be
deleted). All data that shares the same partition goes to the same shard
(ordering).

- provisioned capacity mode
  - specify number of shards, scale manually or through api
  - each shards gets 1MB/s in and 2MB/s out
  - pay per shard per hour
- on demand capacity mode
  - no capacity management, scales automatically based on historic throughput peak
  - default provisioned 4MB/s in or 4000 records per second
  - pay per stream per hour and data in/out per GB

Number of consumers for KDS is limited by 20 (enhanced fanout limit) per shard.
Default of shards per AWS account is around 500. When needed unlimited consumer
ordered message middleware, SQS FIFO is the choice to go.

Security is managed through IAM authorization/access control, HTTPS in flight
encryption, KMS at rest encryption, client side encryption is possible, VPC
endpoints available to access within VPC and monitoring through CloudTrail.

KDS are recommended for the following situations

- routing related record to same processors
- ordering records
- ability for multiple application to consume same stream concurrently
- ability to consume records in same order few hours later

### Kinesis Data Firehose

![kdf](../static/kdf.PNG)

Fully managed auto scaling serverless ingestion service. Pay as data going
through firehose pricing model. It is near real time (60s latency minimum for
non full batches or minimum 1MB of data at a time). Good support for many data
formats, conversion/transformation/compression. Custom transformation with
lambda is also possible. When set KDS as the source of KDF, KDS's `PutRecord`
and `PutRecordBatch` operations are diabled and Kinesis Agent cannot write to
KDF.

## Kinesis, SQS and SNS

Ordering in kinesis is preserved at shard level, thus ensuring that all logical
group are send to a single shard will result in ordered data. Ordering for SQS
FIFO is at queue level with one consumer or at message group level.

SQS and SNS has a maximum message size of 256kb while KDS has a maximum size of
1MB.

## Amazon MQ

SNS/SQS are proprietary cloud native protocol from AWS. Open source protocols
e.g. MQTT, AMQP, STOMP, Openwire and WSS can use Amazon MQ instead without
re-engineering the applications. It is a managed message broker for RabbitMQ
and ActiveMQ. The scalability is not as good as SQS/SNS however is still
possible to run in multi-AZ with failover. The failover is done through having
an active and a standby MQ that both mounted to same EFS storage. Offers queue
and topic feature.

## Amazon EventBridge

Serverless event bus service to connect applications and delivers a stream of
real time data to AWS services and more. Routing rules can be setup to
determine where to send data to enable loosely coupled event driven
architecture.

rules:

- can be used to schedule cron jobs (time based)
- react to some event pattern

It is the default event bus (routes events to zero or more destinations). There
exists partner event bus to send events from AWS SaaS partners into AWS and an
option to create custom event bus. Event buses can be accessed by other AWS
accounts using resource-based policies. Events sent to an event bus can be
archive (optional filtering) indefinitely or some period retention. These
archived events can be used for replay.

> a use case for EventBridge resouce based policy is to enable all event in
> an AWS organization to put the events to a single AWS account/region.

Pipes also exists and is intended for point to point integration i.e. receives
events from single source for processing and delivery to single target. Pipes
and buses are used together by creating a pipe with event bus as its target.
(similar to SQS+SNS)

EventBridge can analyze the event in bus and infer schema. Schema Registry
allows to generate code for application and can be versioned for all AWS
services.

Application's availability can be improved with EventBridge Global Endpoints
without additional costs. First assign R53 health check to the endpoint.
When failover initiated, the health check reports unhealthy state. Within
minutes of failover initiation, custom events are routed to an event bus in the
secondary region and processed by that event bus. Once the health check reports
healthy state event are processed in the primary region.

Event can failed to be delivered to target specified (target resource
unavailable, insufficient permission or network condition). EventBridge allows
retries (number of retry and etc in retry policy, default retry for 24 hours
and up to 185 times with exponential backoff/randomized delay) and if it still
fails it drops the event or sends to a dead letter queue (SQS).

intercept all api calls with cloudtrail
