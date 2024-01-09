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
options is to allow fast snapshot restore which allows full initialization of
snapshot with no latency on first use/creation forcefully.

### EBS Volume Type

| name | short description | IOPS | use case | size |
|-|-|-|-|
| gp2/gp3(ssd) | balance price to performance | see below | | 1 - 16 TB |
| gp2 burst 3000 | size and IOPS linked | max 16,000 IOPS (5334 GB); 3 IOPS per GB |
| gp3 | | 3000 - 16,000 IOPS & 125 - 1000 MB/s throughput (independent setting) |
| io1/io2 (ssd) | high performance SSD, low latency, high throughput | see PIOPS | | 4 - 64 TB |
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

### S3 Security

By default S3 data is encrypted with SSE-S3 (S3 managed keys). Alternatively,
user can use SSE-KMS or SSE-C options for server side encryptions. Client side
encryption is also possible but has to be managed at client side.

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

S3 is encrypted with 

## MISC

throughput vs IOPS