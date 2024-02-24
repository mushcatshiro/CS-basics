# Security

Encryption check [in flight](../data%20security.md#in-flight/transit-(SSL/TLS))
, [at rest](../data%20security.md#server-side-encryption/at-rest) and
[client side](../data%20security.md#client-side-encryption)

## AWS Key Management Service

A regional service that provides encryption service to most AWS services and is
managed by AWS. It fully integrates with IAM for authorization and provides an
easy way to control access to data. KMS keys are auditable on CloudTrail. KMS
key encryption is available through API calls (SDK/CLI) which ensure that
secrets in code are not stored in plaintext.

There are two types keys

- symmetric (AES-256)
  - single encryption key for both encrypt and decrypt
  - AWS services integrated with KMS uses this
  - such KMS keys are not possible to get unencrypted KMS keys (only use KMS API to use)???
- asymetric (RSA, ECC key pairs)
  - public for encrypt and private for decrypt
  - user for encrypt/decrypt or verify/sign operations
  - public key are downloadable but no access to private key unencrypted
  - allows users outside of AWS/can not use KMS API to use

AWS KMS offers the following KMS key types

- AWS owned keys (free): SSE-S3/-SQS/-DDB (default key)
- AWS managed key (free): `aws/rds` or `aws/ebs` etc
- customer managed keys in KMS $1/month
- customer managed keys imported (must be symmetric) $1/month

Customer managed key charges API call to KMS. Automatic key rotation are
default to every year for AWS and customer (must be enabled) managed KMS keys.
For imported KMS keys, only manual rotation is possible using alias.

> if other cadence is desired, must be done manually

Restricted to region, when copying snapshots e.g. EBS, the EBS volume is first
snapshoted with same KMS key then re-encrypt with a different key that lives in
the target region. When restoring the snapshot into volume, same KMS key in the
destiny region is used.

![snap kms](snap-kms.PNG)

### KMS Key Policies

When KMS Key Policy is not present, no one can access it. It control access to
KMS keys similar to S3's bucket policy. The default KMS key policy is created
if it is not specified which grants complete access to key to root user and the
entire AWS account. Custom KMS Key Policy is possible by defining users and
roles that can access or administed the KMS key. This is particular useful when
managing cross-account access of KMS keys.

Cross account snapshot copying is similar to EBS cross region copying except
a custom KMS Key Policy is needed to authorize cross-account access to the KMS
key.

> destination account uses KMS key in source account to decrypt

### Multi-Region Keys

It is a set of identical KMS keys in different AWS regions to be used
interchangeably (similar arn `arn:aws:kms:some-region:112233:key/mrk-123`).
They share the same key ID, key material (content) and automatic rotation
option. It allows encryption in one region and decrypt in other regions. No
re-encrypt or making cross-region api calls. KMS multi region are not global,
a primary key is first created and then is replicated to selected regions
within AWS partition. Multi-region key is managed in each region independently
i.e. replication must be done manually and key policy are independent. All AWS
managed keys are single region keys.

It is recommended to not abuse multi-region keys except for a few use cases
including

- global client side encryption
- global DDB/global Aurora

Architecture below show a global DDB that has an client side encryption data,
which protect against even database admins. Client app on different regions can
decrypt the information. Similar technique can be applied on global Aurora to
have column level protection.

![mrk-ddb](mrk-ddb.PNG)

### S3 Replication with Encryption

> check ![S3 Bucket Replication](storage.md#s3-bucket-replication)

Unencrypted objects and SSE-S3 encrypted objects are replicated by default and
SSE-C objects can be replicated. For SSE-KMS objects, option must be enabled
for replication to specify KMS key to encrypt objects within target bucket.
Appropriate KMS Key Policy and IAM role must be in place to successfully
replicate the bucket. KMS throttling errors might be encountered and can be
alleviate by asking for service quota increase.

> IAM role of `kms:Decrypt` for source KMS key and `kms:Encrypt` on target KMS
> key

Multi region key can be used but they are still treated as independent key by
S3 i.e. object still gets encrypted and decrypted.

### AMI sharing with KMS encryption

AMI in source account must first modify the image attribute such that the
target account has `Launch Permission` and KMS keys must have appropriate Key
Policy. In the target account, the role or user should have permission to
`DescribeKey`, `ReEncrypted`, `CreateGrant` and `Decrypt`.

## SSM Parameter Store

A serverless, scalable, durable secured storage for configuration and secrets
with optional seamless encryption using KMS. It also provides version tracking
of the content. Security is managed through IAM and notification is sent
through Amazon EventBridge. It has integration with CloudFormation. SSM
Parameter Store supports folder like store hierarchy.

`/aws/reference/secretsmanager/secret_ID_in_Secrets_Manager`

`/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2` (public) to
know what is the latest supported amis

| - | standard | advanced |
|-|-|-|
| total parameter allowed per AWS account and region | 10,000 | 100,000 |
| maximum size of a parameter value | 4kb | 8kb |
| parameter policies available | No | Yes |
| cost | no additional charge | charges apply |
| storage pricing | free | $0.05 per advanced parameter per month |

Parameter policies for advanced parameters allows to assign TTL to force
update/deletion to sensitive data. On EventBridge end can set an expiration
notification prior to the timestamp.

### Lambda Integration

When creating function, to create a new role with basic Lambda permission and
add permission to access SSM Parameter Store. By adding an inline policy for
systems manager (SSM) to `get_parameters` and `get_parameters_by_path`. It
should look something like `arn:aws:ssm:*:*:parameter/something/*`.

```python
import json
import boto3

ssm = boto3.client("ssm", region_name="region")

def lambda_handler(event, context):
    secret_1 = ssm.get_paramters(Names=["/something/secret_1"])
    return
```

> note for securedstring in SSM Parameters Store, the IAM role should also have
> access to KMS to decrypt the string

## AWS Secrets Manager

New service meant to store secrets that has the capability to force rotation of
secrets periodically. It supports secrets generation on rotation using Lambda.
It has good integration with AWS services including RDS. The secrets are
encrypted using KMS. Similar to multi region keys, secrets are replicated to
multiple AWS regions and kept in sync with the primary secret. It allows to
promote a read replica secret to a standalone secret. It is primarily used for
multi-region apps, disaster recovery strategy and multi-region DBs.

## AWS Certificate Manager

Provides, manage, and deploy TLS certificates for in-flight encryption (HTTPS).
It supports public and private TLS certificates and its free of charge for
public certificates. It integrates with ELBs, CloudFront distributions and APIs
on API Gateway. An application load balancer can get TLS certs from ACM to
enable TLS security. Like any TLS certificate services, auto certifical renewal
is possible.

> EC2 cannot use ACM with public certificates

### Requesting Public Certificates

List domain names to be included in the certificate. It can be FQDN or a
wildcard domain. Then select a validation method, DNS is preferred for
automation purposes by leveragin a CNAME record to DNS config (R53).
Alternatively, email validation is done by sending email to contact address in
the WHOIS database. It takes a few hours to get verified and the certificate
will be enrolled for automatic renewal 60 days before expiry.

### Importing Public Certificates

It is possible to generate certificate outside from ACM however there is no
auto renewal. ACM sends expiration events through EventBridge starting 45 days
prior to expiration (no of days can be configured). Alternatively, one can use
AWS Config's managed rule `acm-certificate-expiration-check` to achieve the
same.

## AWS Web Application Firewall

Protects web application from common L7 web exploits. It is deployed on ALB,
API Gateway, CloudFront, AppSync GraphQL API and Cognito User Pool. Web ACL
rules including

- IP, up to 10,000 address (use multiple rules for more IPs)
- HTTP headers, body, URI string (SQL injection and Cross-Site-Scripting)
- size constraints
- geo-matches (block countries)
- rate-based rules (for DDoS)

Web ACLs are regional except for CloudFront. A rule group is a reusable set of
rules to add to web ACL.

If a static IP is needed while using WAF + load balancer, NLB is not compatible
with WAF as WAF is meant for L7 while NLB is at L4. To resolve this, use a
Global Accelerator to have a fixed IP and that links to an ALB with WAF.

## AWS Shield

Provides DDoS protection with two modes,

- AWS Shield Standard
  - free service for all AWS customer
  - provide protection from SYN/UDP flood, reflection attach and other L3/4 attacks
- AWS Shield Advanded
  - optional DDoS mitigation service ($3000 per month per organization)
  - protect against more sophisticated attach on EC2/ELB/CloudFront/Global Accelerator and R53
  - 24/7 AWS DDoS response team
  - protect against higher fees during usage spike
  - it automatically creates, evaluates and deploys AWS WAF rules to mitigate L7 attacks

## Firewall Manager

Manages all firewall rules in all account of an AWS organization. A security
policy (set of common security rules) including

- WAF rules
- Shield advanced rules (ELBs, Elastic IP, CloudFront)
- security groups for EC2, ALB and ENI in VPC
- AWS Network Firewall (VPC level)
- R53 resolver DNS firewall

These policy are created at regional level. Rules are applied to new resources.

### WAF, Shield and Firewall Manager

They are used together for a comprehensive protection. Web ACLs are defined in
WAF, which gives a granular protection of resources. Use Firewall manager if
the WAF needs to be used across many accounts. Shield Advanced is for those who
are prone to DDoS and requires dedicated support and advanced reporting.

## DDoS Resiliency Best Practices

### Edge Level Mitigation

- CloudFront: delivery at edge, protect from DDoS common attach
- Global Accelerator: edge access, integration with Shield
- R53: DNS at edge, DDoS protection mechanism

### Infrastructure Level Defense

- CloudFront
- Global Accelerator
- R53
- ELB

Protect EC2 against high traffic by preventing the traffic to get through. And
in case the traffic reaches i.e real traffic, Auto Scaling Group helps to
handle surge of traffic together with ELB to balance it.

### Application Layer Defense

- CloudFront
- Global Accelerator
- WAF

CloudFront prevent direct hit to backend through caching. WAF on top of
CloudFront and ALB filters and blocks requests based on signatures. WAF rate
based rules blocks IP of bad actor. WAF also provdies other managed rules e.g.
IP reputation or annonymous IP block. CloudFront can block specific
geographies.

Above 3 together with ELB Shield Advanced integration help to automatically
deploy WAF rules for L7 attacks.

### Attack Surface Reduction

- CloudFront
- Global Accelerator
- API Gateway (+WAF): burst limits, headers filtering, API keys
- ELB

Hides backend.

Security groups and Network ACLs can filter IPs at subnet and ENI level. Also
Elastic IP are protected by AWS Shield Advanced.

## GuardDuty

Thread discovery service to protect AWS account by using ML, anomaly detection
and 3rd party data. No additional software installation is required. It looks
at

- CloudTrail events (management and data events)
- VPC Flow logs
- DNS logs
- other logs (EKS, RDS, ....)

EventBridge rules can be setup to notify on the findings and bridged to SNS or
lambda. It also has a deficated finding for crypto currency attacks.

## Amazon Inspector

Provides automated security assessments for,

- EC2 instances
  - using AWS SSM agent on instances
  - analyze unintended network accessibility and OS known vulnerabilities
- container images when pushed to ECR
- lambda function when they are deployed
  - identify software vulnerabilities in function code and package dependencies

Reports and integrates with AWS Security Hub and also possible to send findings
to Amazon EventBridge. Vulnerability scans only happens when needed i.e. new
changes or there is an update to the CVE database. A risk score is generated
for prioritization.

## Amazon Macie

A fully managed data security and privacy service that uses ML to discover
sensitive data e.g. PII in S3 buckets. Integrates with EventBridge.