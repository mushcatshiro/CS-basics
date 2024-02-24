# Storage

## Elastic Block Storage (EBS)

Network drive that can be attached to instance and persist after instance
termination. EBS are bound to AZ, to move across AZ user first create a
snapshot and restore to another AZ. Slight latency is expected as network can
be unstable/unreliable, however is compensated with ease of attach-detach.
Although EBS default behavior persist after termination, delete on termination
tag can be added to enable (root EBS is always destroyed). EBS can be expanded
over time.

EBS snapshot has an archive option to make them ~75% cheaper and takes 24-72
hours to restore. Deleted snapshots are available in recycle bin. It is
possible to setup retention rules betwen 1 - 365 days for recovery. Another
option is to allow fast snapshot restore which allows full initialization of
snapshot with no latency on first use/creation forcefully.

### EBS Volume Type

| name | short description | IOPS | use case | size |
|-|-|-|-|-|
| gp2/gp3(ssd) | balance price to performance | see below | - | 1 - 16 TB |
| gp2 burst 3000 | size and IOPS linked | max 16,000 IOPS (5334 GB); 3 IOPS per GB |
| gp3 | size and IOPS are independent setting | 3000 - 16,000 IOPS; 125 - 1000 MB/s throughput |
| io1/io2 (ssd) | high performance SSD, low latency, high throughput | see PIOPS | - | 4 - 64 TB |
| PIOPS io2 | better durability than io1 | max 64,000 IOPS for EC2 Nitro and 32,000 for the rest; independent of size |
| PIOPS io2 block express | submilisecond latency | max 256,000 with IOPS:GB 1000:1 | support multi-attach EBS |
| st1 (hdd) | low cost, frequent access, high throughput | max 500 MB/s & 500 IOPS | data warehouse, logging | 125 GB - 16 TB |
| sc1 (hdd) | lowest cost, infrequent access | max 250 MB/s & 250 IOPS | archive | 125 GB - 16 TB |

> note io2 is superior in all terms to io1 at same price

### EBS multi attach

Available for io1/io2 such that same EBS can be attached to multiple EC2 (up
to 16) in same AZ. each instance has full read and write access. This allows
for higher applicaiton availablity (clustered linux app or mandaroty concurrent
write).

> note that cluster aware files system should be used (not XFS, EXT4)

### EBS encryption

Data at rest is encrypted in volume and at transit (to EC2) is also encrypted.
All EBS snapshots are encrypted and volume/image created from snapshots are
encrypted. The encryption has minimal impact to latency using KMS AES-256 keys.
Snapshots are always encrypted regardless if it is encrypted or not (2 layers
of encryption) and is a good way of creating encrypted volume.

## Elastic File System (EFS)

Attach to multiple EC2 in same region (cross AZ, creates ENI per AZ). EFS is
high available, scalable, and is ~3x of gp2 with a pay per use model (no
capacity planning). A few use cases including content management, web serving,
data sharing and wordpress. EFS uses NFS 4.1 protocol and security group for
access control. EFS is only compatible with linux AMI as it is based on POSIX
filesytem. EFS files are encrypted with KMS.

EFS can scale to thousands of NFS clients, with ~10 GB/s throughput and grows
into PB size storage. Performance option is available at creation time to have
maximum I/O with high latency, high throughput and highly parallel (compared to
default latency sensitive mode).

Throughput option is available with bursting capabilities, provisioned
throughput i.e. fixed value regardless of storage size and elastic mode which
scales throughput up and down based on workloads.

### EFS storage class

EFS has a lifecycle management policy to move files after some time.

- standard: frequently accessed files
- infrequent accessed: costly to retrieve, low cost to store (move with EFS-IA policy)

For EFS availability and durability,

- standard multi AZ option
- one zone with default backup and EFS one zone IA policy (~90% discount)

## EBS vs EFS

| EBS | EFS |
|-|-|
| 1:1 ec2 except io1/2 multi attach | 1: many |
| locked at az | locked at region |
| migrate with snapshot | 
| backup consumes EBS I/O, affects performance |
| root EBS is erased (can be disabled) |
| | only unix system |
| | more expensive |

## Instance Store

Temporary physically attached block level storage to host computer. It has the
best IO performance (> 256,000 IOPS, up to millions IOPS) however is 
emphemeral. It is usually used in buffer, cache, temporary/scratch file
scenario. Note that there is a risk for data loss should there be a hardware
failure.

## Simple Storage Service (S3)

S3 is an infinitely scaling storage for backup/archive and object level
storage. It can be used as

- disaster recovery
- hybrid cloud storage
- application/static site/media hosting
- big data storage and analytics
- software delivery (patches)

> S3 is generally good for bigger objects and less great for many smaller
> objects

S3 although is presented like a directory/file system, however is more like a
key value store from the underlying infrastructure perspective. All buckets
must have a globally unique name - across all region all accounts. Buckets
are bounded at region level despite looking like a global service. Objects in
S3 has a size limit of 5TB and its recommended when uploading a file larger
than 5GB to use multi-part upload. Each object has,

- metadata (list of kv pair for system and user metadata)
- tags (kv pair, up to 10, usually for security and lifecycle management)
- version ID (if enabled)
  - versioning is enabled at bucket level
  - mainly used to prevent unintended delete and version control (roll back)
  - files prior to versioning enabled will have version null
  - suspeding versioning will not delete pervious version

### S3 Bucket Replication

S3 bucket replication allows for both cross- and same- region replication
through setting replication rule. Versioning must be enabled in both source
and destination region. The buckets can be in different AWS accounts and the
replication is done asynchronously. IAM permission must be set correctly to
start replication.

Some use case for the two replication mode,

- CRR: compliance, low latency access, replication cross account
- SRR: log aggregation, live replication between test and prod environment

When deleting an object with no version specified, a delete marker is attached.
However when deleting an object with version specified, that particular version
object is deleted. Delete marker is not replicated by default and deletion are
not replicated to avoid malicious delete. If a delete request has version
specified, S3 does not replicate delete from source bucket.

S3 replication will not be chained i.e. object created in first bucket will
only be replicated to second bucket and not the third bucket despite second
bucket is set to replicate objects to the third bucket.

> note that only new object after replication enabled is replicated. for object
> that exists or failed during replication in bucket requires manual batch

S3 has a requester pay option such that the object's requestor (AWS
authenticated) pays for the network transfer.

S3 events can be used for automation (simple filtering is allowed). Events
created can be linked to other services and expect delays (seconds - minutes).
Appropriate IAM permission must be granted on downstream services including
lambda, SNS and SQS. S3 events can be limited (downstream service and
filtering), thus using EventBridge might be an alternative.

> S3 events can only have one event rule per perfix, use SNS to circumvent it

S3 batch operation allows bulk operation to be performed on existing S3 objects
with single request,

- modify object metadata/properties/ACL/tags
- copy between buckets
- encrypt unencrypted objects
- restore objects from S3 Glacier
- invoke lambda funtion to perform custom action on each object

A batch operation consist of a list of objects, action and optional parameters.
S3 batch operation is highly managed, it retries, tracks progress, sends
completion notification, generates report and etc. Batch operation can be used
together with S3 inventory to get object list and S3 select to filter objects.

### S3 Performance

> bucket/folder/subfolder/file name, prefix is anything between bucket and file
> name

- scales to high request rate with latency ~200ms
- at least 3,500 put/delete/copy/post per second per perfix
- at least 5,500 get/head request per second per perfix
- no limit to number of prefix in bucket

A few tips on S3 performance optimization including

- multipart upload: parallel upload to speed up
  - recommend for files > 100MB
  - must use for file > 5GB
- S3 transfer acceleration
  - improve speed by xfering to AWS edge location and forward data to S3 bucket in target region
- byte range fetch: speed up download or retrieve only specific data
  - parallel get for specific byte range
  - resilient to failures

S3 Select/Glacier Select is means to retrieve object with SQL queries. Server
side filtering is done to improve network cost. The selection can be done on
rows and columns.

### Storage Classes

S3 storage can move between classes manuall or through lifecycle config. All
S3 storage classes has 11 9s durability across multiple AZ. The difference
between classes is the availability.

| class | availability | use case |
|-|-|-|
| general purpose | 99.99% | frequently accessed data, low latency high throughput able to sustain 2 facility failure |
| infrequenct access | 99.9% | less frequent access and rapid access when needed, lower cost, usually for disaster recovery |
| S3 inteligent tiering | - | move between tier based on usage, charged monthly for monitoring and auto tiering, no retrieval charge |
| one zone IA | 99.5% | hugh durability in one AZ, data is lost if AZ destroyed, secondary backup for on prem data |
| glacier instant retrieval | - | milisecond retrieval, minimum 90 days storage, data accessed per quarter |
| glacier flexible retrieval | - | expedited 1-5mins; standard 3-5hours, bulk 5-12hours, min storage 90 days, data access yearly |
| glacier deep archieve | - | standard 12 hours; bulk 48 hours; min 180 days storage, long term storage |

Lifecycle rules can be setup to move object between storage tiers. There are
two types of actions,

- transition action: move object from class A to class B after X days (entire objec)
- expiration action: delete object after X days 
  - only current version
  - to delete old version of files if versioning enabled
  - delete incomplete multipart upload

Rules can be created for certain prefix of S3 bucket name or tags

Storage class analysis can be done in S3 analytics to decide when to transition
object to right storage class. Only for standard and standard IA. It is updated
daily and need to wait 24-48 hours for first analysis.

### S3 Security

By default S3 data is encrypted with SSE-S3 (S3 managed keys). Alternatively,
user can use SSE-KMS or SSE-C (customer provided key) options for server side
encryptions. Client side encryption is also possible but has to be managed at
client side.

- SSE-S3
  - AWS256 encrypted
  - request must have header "x-amz-server-side-encryption": "AES256"
- SSE-KMS
  - under controlled key (stored in AWS)
  - integration with CloudTrail for key usage
  - header "x-amz-server-side-encryption": "aws:kms"
  - accessing object requires key
  - limited by KMS generate key/decrypt and counts towards KMS quota
- SSE-C
  - key is stored at client end and is sent together to AWS for encryption
  - AWS do not store the key thus every request requires key provided
  - HTTPS is required
- DSSE-KMS
  - double encryption option with KMS

> for SSE-KMS and SSE-C it is possible to add additional bucket policy to
> enforce encryption.

For in flight security, S3 has an option to enforce encryption by including
bucket policy "secured transport". Note the policy is evaluated before
encryption. S3 CORS can be enabled for some defined host in case cross origin
request is expected to hit on S3 buckets.

User based control is done through IAM and roles. resource based policy can be
setup such that it applies bucket wide (known as S3 bucket policy), object ACL
for fine grain control and bucket ACL (less commonly used). When multiple rules
exists, it will first ensure that IAM permission or resource based policy
allows, while also ensuring there is no explicit deny.

With the policies above, it is possible to grant public access, or force object
to be encrypted at upload, or grant access to another account (cross account).

> naming convention including only lowercase, no underscore, 3-63 characters
> long, not an IP, start with alphanum, must not start with xn- prefix and
> -s3alias suffix.

 S3 has an option to enable MFA delete for permanently deleting an object
 version or suspending versioning on a bucket. List deleted version/enable
 versioning does not require MFA. Versioning must first be enabled before MFA
 delete is enabled and enablement requires bucket owner (root account).

 S3 access logs can be enabled for audit purposes. All incoming request will be
 logged into another S3 bucket in the same region. Infinite loop is be created
 if the monitored bucket is set as the logging bucket.

 S3 can generate pre-signed urls such that the IAM permission is shared to
 another user with the url (with exipry). A few use cases including

 - sharing/upload some files without changing bucket to public
 - ever changing user list
 - premium media download

 S3 access point can help to simplify security management for S3 buckets. It
 masks off the buckets and only user through any access point to access a
 subset of buckets. Each access point has a DNS name (internet or VPC origin).
 Access point is controlled by access point policy.

 For VPC origin access point, a VPC endpoint must be created to access with
 VPC endpoint policy allow access to target bucket and access point.

### S3 Locks

Glacier has an glacier vault lock option adopts a Write Once Read Many model by
creating a vault lock policy. The vault lock prevents object from future edits
and it is helpful for compliance and data retention.

A similar option is available for non glacier S3 known as S3 object lock which
blocks object deletion for specified amount of time and requires versioning.
There are two modes,

- retention mode compliance
  - object version can not be overwritten or deleted including root user
  - object retention mode and retention period can not be changed 
- retention mode governance
  - most users can not overwrite or delete object version or alter lock settings

Retention period must be set for both modes and can be extended. There is also
legal hold option that protect object (version) indefinitely and is independent
from retention period. IAM permission is required to place and remove legal
hold.

### S3 Object Lambda

Using lambda to modify object just before caller retrieve the object. Access
point and S3 object lambda access point is required. The retrieval path would
be S3, S3 access point, lambda function, lambda function access point and
client.

Use cases

- masking personal identifiable information
- converting file formats
- resizing images on the fly

## AWS Snow Family

Is a suite of services that allows data processing at edge or moving PB of data
to and from AWS through highly secure and portable device. It mainly addresses
situation where connectivity or bandwidth is limited and optimize the cost
of transfer. Generally it is used when the data transfer takes more than one
week.

- snowcone/snowball: migrate/process data at edge (EC2/lambda)
- snow mobile: migrate data

The usage process for data migration would be the following,

- snow family device request from AWS
- install snowball client/AWS OpsHub on server
- connect snowball to server and copy files using client
- ship back the device
- data loaded to S3 bucket
- snowball is completely wiped

Edge computing with snow family devices are for use cases when there is limited
internet or power supply and

- data preprocessing
- ML at edge
- media stream transcoding

and etc. are needed. The data can be send back to AWS (optional). The lambda
function is using AWS IoT Greengrass service. Long term deployment options for
1 and 3 years are at discounted pricing.

### Snowball Edge

Moving TB/PB data in or out of AWS. Its a pay per data transfer job service.
The device provides block storage and S3 compatible object storage.

- storage optimized: 80TB HDD
  - Up to 40vCPU, 80GB RAM
- compute optimized: 42TB HDD/28 TB NVMe
  - 104 vCPU, 416GB RAM, optional GPU
  - storage clustering up to 16 nodes

There is no direct pipeline for snowball to glacier however it can be done by
using lifecycle policy on the S3 bucket.

### Snowcone (SSD)

Small, portable, durable and secure computing device. Use when snowball does
not fit due to space constraint. Power supplied must be prepared. Data can be
transfered through physical transfer or through AWS DataSync.

- snowcone: 8TB HDD
- snowcone SSD: 14TB SSD

Snowcone devices has 2 CPUs, 4GB RAM, wired and wireless access and using USB-C
or optional battery for power supply.

### Snowmobile

Exabyte-level of data transfer (1000PB), 100PB per truck. It is highly secured,
temperature controlled, GPS, 24/7 video surveillance etc.

### AWS OpsHub

AWS OpsHub is an alternative for using snow family devices through CLI that can
be installed on local machine.

## AWS FSx

[choosing fsx](https://aws.amazon.com/fsx/when-to-choose-fsx/)

FSx is a service to launch fully managed 3rd party filessystem on AWS. FSx only
supports lustre, Netapp ONTAP, Windows File Server and OpenZFS.

FSx for Windows supports,

- SMB protocol and Windows NTFS
- msft Active Directory, ACL, user quotas
- can be mounted to Linux EC2 instance
- supports msft distributed file system namespace for groupping files across multiple FS (on prem and on AWS)
- scales to tens of GB/s, millions of IOPS, hundreds PB of data
- storage option
  - SSD
  - HDD
- can be accessed from on prem infrastructure through VPN or Direct Connect
- can be configured as Multi-AZ for high availability
- daily backup to S3

FSx for Lustre

- parallel distributed file system for large-scale computing (ML/HPC)
  - video processing, financial modeling, Electronic Design Automation
- scales to hundreds of GB/s, millions of IOPS, sub-ms latencies
- storage option
  - SSD: low-latency, IOPS intensive, small and random file operation
  - HDD: throughput intensive, large and sequential file operation
- seamless integration with S3
  - can read fromm and write to S3 as file system through FSx
- can be accessed from on prem infra
- deployment option
  - scratch file system
    - temporary file storage
    - data is not replicated (does not persiste if file server fails)
    - high burst (6x faster)
    - short term processing/cost optimization
  - persistent file system
    - long term storage
    - data is replicated within same AZ
    - replace failed files within minutes
    - long term processing/sensitive data

![fsx-lustre](fsx-lustre.PNG)

> only difference is if its persistent, it has replication in same AZ

NetApp ONTAP

- file system compatible with NFS, SMB, iSCSI protocol
- move work load on ONTAP or NAS to AWS
- works with linux/win/MacOS/VMware cloud on AWS/Amazon workspace & AppStream 2.0/EC2, ECS and EKS
- storage shrink and grows automatically
- snapshot, replication, low-cost, compression and data deduplication
- PITR instantaneous cloning (helpful for testing new workloads)

OpenZFS

- only compatible with NFS (v3, v4, v4.1, v4.2)
- move workload on ZFS to AWS
- same compatibility list as NetApp ONTAP
- up to 1Mil IOPS with < 0.5ms latency
- snapshot, replication, low-cost
- PITR instantaneous cloning

## AWS Storage Gateway

A bridge between on prem data and cloud data for disaster recovery, backup &
restore, tiered storage, on prem cache and low latency file access. There is an
option to get hardware appliance for the gateways from AWS.

S3 file GW caches the most trecently used data at the file GW. Bucket access
uses IAM roles for each file GW. SMB protocol has integration with Active
Directory for user authentication.

![file-gw](file-gw.PNG)

FSx file GW allows native access to AWS FSx for windows file server and caches
frequently accessed data. It has native windows compatibility (SMB, NTFS, AD).
AWS FSx works without the gateway however does not caches data. Its useful for
group file share and home directories.

Volume GW is a block storage using iSCSI protocol backed by S3 and is further
backed by EBS snapshots for quick restore.

- cached volume: low latency access to most recent data
- stored volume: dataset on prem and scheduled backups to S3

Tape GW for physical tape backup process to be backup on cloud using Virtual
Tap Library backed by AWS S3 and Glacier. Backup data is using existing tape
based process and iSCSI interface.

## AWS Transfer Family

Fully managed service for file transfer in and out of S3 and EFS using FTP
protocol (including FTP, SFTP, FTPS). The infrastructure is managed by AWS, and
its scalable, reliable and HA across multi-AZ. Pay per provisioned endpoint per
hour and data transfer in GB. It is possible to store and manage user's
credentials within the service and it integrates with existing authentication
systems (msft AD, LDAP, Amazon Cognito, custom). Uses cases including sharing
files, public datasets, CRM and ERP.

![xfer-fam](xfer-fam.PNG)

## AWS DataSync

Scheduled data moving/replication task between

- on prem - AWS (require agent)
- AWS - AWS

to destination including S3 (any tier including glacier), EFS, FSx on hourly,
daily or weekly basis. The file permission metadata are preserved (NFS POSIX,
SMB etc). One agent can use 10GB/s and a bandwidth limit can be set to ensure
there is bandwidth for other operations.

> when there is insufficient network capacity for DataSync, snowcone can be
> used.

## MISC

throughput vs IOPS
