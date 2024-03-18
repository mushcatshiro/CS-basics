# Identity Access Management

## Terminology

Principal is a human user or workload that can make request for an action on
AWS. After authentication it can be granted permanent or temporary credential to
make request to AWS. IAM and root users are permanent and roles are temporary
credentials. 

Authorization essentially is a check of the policies. AWS denies by default.
Defaults are override if there is explicit allow (identity or resource based).
Then Organization SCP, IAM permission boundary or session policy overrides the
allow (all must agree to allow). Policies are attached IAM identities or AWS
resources. Policies are usually in JSON format except access control list. There
are 6 types of policies

- identity based policies
- resource based policies: S3 bucket policies and IAM role policies
- permission boundary
- organization service control policy
- access control list
- session policies

> for cross account request, both requester and resource must have appropriate
> identity policy and resource policy that allows the request.

### Identity Based Policies

There are three type of identity based policies, AWS managed, customer managed
and inline policy. AWS managed policy is created and managed by AWS. It has a
ARN. It is a convienient way to assign appropriate permission to users, role and
groups. It can not be modified and when AWS modify it it affects all principals
the policy is attached to.

Customer managed policies have more flexibility in term of modification. When
there is a change in the policy, it does not overwrites the existing one. A new
version is created and AWS stores up to five versions. Revert to earlier version
is possible.

Inline policy is useful if a one to one relationship is required. They are
deleted when the identity is deleted. Two roles can have the same inline policy
but owns a copy of the policy.

> EventBridge is a unique services that requires both resource based policy and
> IAM roles to interact with other AWS services.

## Users in AWS

Users can be IAM or IAM Identity Center users. THe latter have temporary
credentials established everytime they are signed in. Such credentials is
recommended to have an identity provider. Root user is the account used to
create AWS account. A best practice is to only allow temporary credentials for
human users, if needed a long term credentials ensure to update access key when
needed. If the organization has a way of authentication it can be federated to
AWS through IAM or IAM Identity Center.

### User Groups

A collection of IAM users. Used to specify permissions for multiple users.
Identity based policy can be applied to groups. However User Group's `principal`
cannot be identified in a policy e.g. resource based policy as it is not meant
for authentication.

## IAM Roles

IAM identity created with specific permission that allows anyone to assumes it.
Roles are meant to delegate access to users, apps or services that have no
access to AWS resource. Roles can also be users in a different AWS account. When
a role is assumed, it gives up their original permissions.

Policies can be build in IAM Policy Builder in the following policy structure,

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PermissionsBoundarySomeServices",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:*",
                "dynamodb:*",
                "ec2:*",
                "s3:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "PermissionsBoundaryNoConfidentialBucket",
            "Effect": "Deny",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::DOC-EXAMPLE-BUCKET1",
                "arn:aws:s3:::DOC-EXAMPLE-BUCKET1/*"
            ]
        }
    ]
}
```

## Permission Boundaries

Supported for users and roles (not groups) to limit maximum permission an IAM
identity can get.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "cloudwatch:*",
                "ec2:*"
            ],
            "Resource": "*"
        }
    ]
}
// additional permission policy
{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Action": "iam:CreateUser",
    "Resource": "*"
  }
}
```

A user with additional permission policy will not be able to create iam user as
Permission boundaries superceeds the permission policy. It is usually used
together with Organization SCP.

![iam-eval](../static/iam-eval.PNG)

### IAM conditions

```json
// aws:SourceIp -> restrict client from which the api call being made
// aws:RequestedRegion -> region that actually spawns instance
{
  // ...
  "condition": {
    "NotIpAddress": {
      "aws:SourceIp": ["1.1.1.1", "2.2.2.2"]
    }
  }
}
// S3
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::test" // bucket level
    },
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject"],
      "Resource": "arn:aws:s3:::test/*" // object level
    }
  ]
}
```

- `aws:PrincipalOrgId` resource policy to restrict access to member of some org
- `ec2:ResourceTag/Project`
- `aws:PrincipalTag/Department`
- `aws:MultiFactorAuthPresent`
- `aws:RequestedRegion`

## Organization

A global service to managed multiple AWS accounts. The main account is the
management account and others are member account. A single member account can
only be part of one organization. Organization allows billing to be
consolidated. Such single payment gives pricing benefits from aggregated usage.
Shared reserved instance and savings plan discounts are shared. AWS provides an
api to automate account creation.

![org](../static/org.PNG)

Organization Units are commonly organized by business unit, environment
lifecycle or projects-based. Organization provides benefits such as

- multiple account as a separation vs single account multi VPC separation
- use tags for billing purposes
- enable CloudTrail on all accounts and log to central S3
- send CloudWatch to central logging account
- establish cross account role for admin purposes
- Service Control Policies (SCP) for security
  - IAM policy to apply on OU/accounts except mgmt to restrict users and roles
  - by default denies all access, requires explicit allow
  - OU deny but account allow still results in deny
  - allowlist and blocklist strategy
- backup policies - organization wide backup plan for compliance
- tag policies to standardize tags used on all resources

Moving AWS account between two Organization requires old Org. to remove, new Org
to send invite and re-accept.

### Resource Access Manager (RAM)

Securely share resources across AWS accounts within Organization (Organization
Unit) with IAM roles and users.

#### VPC Sharing

Allowing multiple AWS accounts to create appication resource into shared and
centrally managed VPCs. The onwer of VPC shares one or more subnets with other
accounts belong to the same Organization. Only shared resources is visible to
participants.

![ram vpc share](ram-vpc-share.PNG)

## Password Management

User password can be governed by enabling password policy that check for rules
including

- length
- characters requirements
- expiry
- password reuse

A general guideline for IAM are

1. only using root to create (super)users
2. one aws account per user
3. groups for access and permission
4. use password policy and MFA
5. assign appropriate roles for services
6. manage access key properly when using CLI/SDK i.e. not storing key on AWS console

## MFA

Multifactor authentication is possible and recommended in AWS in case of
password lost or hacked to prevent account compromise. Virtual MFA with

- google authenticator
- authy
- U2F security key

or hardware like keyfob MfA device and US goverment AWS govcloud keyfob.

## Security Tools

IAM credential report: account level list of all user and status of various
credentials e.g. password,, MFA status, access keys etc. to help in auditing
and compliance efforts (credentials lifecycle requirements)

IAM access advisor: user level list of service permission granted to user and
last used.

## AWS Cognito

Provide users an identity to interact with web or mobile application, these
users generally are outside of AWS account.

- Cognito User Pool (authentication)
  - sign in functionality for app users
  - integrate with API gateway and ALB (CloudFront requires lambda@edge)
- Cognito Identity Pool (authorization)
  - provide temporary AWS credentials to users to access AWS resource directly
  - works with Cognito User Pool as an identity provider

### Cognito User Pool

Creates a serverless database of users for web and mobile app through simple
username/password login. It supports password reset, email/phone number
verification, MFA and federated identities from FB, Google, SAML etc.

![cup](../static/cup.PNG)

### Cognito Identity Pool

Provide AWS account identity for users ie. temporary AWS credentials. Users can
be from Cognito User Pool, 3rd party logins and etc. Users can then access AWS
services directly or through API gateway. The IAM policies applied to
credentials are defined in Cognito. The IAM policies can also be customized
based on `user_id` for fine grain control. A default IAM role can be defined
such that users (guest or authenticated) that dont have specific roles can
inherit from the default IAM role.

![cip](../static/cip.PNG)

With Cognito Identity Pool, a row level security in DynamoDB can be setup such
that only if the leading key of DynamoDB is same as the cognito `user_id`, the
user can perform certain action.

## AWS IAM Identity Center (was AWS SSO)

Single sign on service for all AWS accounts in AWS organization, business cloud
application (Salesforce, Box, Microsoft 365 etc), SAML2.0-enabled apps, EC2
Windows instances. Identity providers can be build in in IAM identity center or
3rd party e.g. AD, OneLogin, Okta...

![sso](../static/sso.PNG)

How users linked to groups, to permisison sets and to specific accounts.

![usr-to-acc-link](../static/usr-to-acc-link.PNG)

### Active Directory Setup

- AWS managed Microsoft AD
- self managed directory
  - create a two way trust relation using AWS managed Microsoft AD (ootb int.)
  - use AD connector

> no support of msft distributed file system

### Fine grouned permission and assignments

- Multi-account permissions
  - manage access across AWS accounts in Organization
  - permission sets is a collection of one or more IAM policies assigned to
    users and groups to define AWS access
- application assignments
  - sso access to SAML2.0 apps
  - provides urls, metadata and certificates
- attribtue based access control
  - permission based on user's attribute stored in IAM Identity Center ID Store
  - define permission once and modify AWS access through changing attributes

## AWS Directory Services

Microsoft AD is a service found on any Windows server with AD domain service.
It is a database of object including user accounts, computers, printers, file
shares, security groups and etc. Essentially it is a centralized security
management to create accounts and assigning permissions. These objects are
organized in trees and group of trees is a forest.

> one account for the named objects

AWS provides three types of AS services,

- AWS managed Microsoft AD
  - AD can be created in AWS to managed user locally and supports MFA
  - user can use AWS AD or on prem AD to authenticate (trust between on prem and AWS)
  - integration with AWS IAM Identity Center is out of the box (just connect)
- AD connector
  - AWS acts as a proxy to on prem AD and supports MFA
  - on prem AD managed users
- Simple AD
  - fully AWS managed, not joined with on-prem AD

## AWS Control Tower

Set up and govern a secure and compliant multi-account AWS environment using
AWS Organization to create account that is based on best practices. AWS Control
Tower offers guardrails to ensure compliance in two modes

- preventive: with AWS Organization's Sevice Control Policy
- detective: with AWS Config (fix non compliant with SSM or SNS to lambda)

With Control Tower, environment can be setup in few clicks and a monitoring
dashboard is provided.

