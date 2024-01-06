# Data Security

data security is needed in both scenario, data in transit and data at rest.
data in transit is where data is transit across internet or private network, is
considered more vulnerable and critical. data at rest eg data stored in hdd,
however is considered less vulnerable and is a more valuable target.

## Proctecting data

data can be exposed to risk in both state thus protection is required for both
state. by using encryption, data at transit utilized encrypted connection and
for data at rest, encryption can be done prior to storage and/or encrypting the
storage itself. besides encryption, network security solution eg. firewalls and
network access control helps to secure the network that is used to transmit
data.

## AWS encrypting data at rest and in transit

AWS key management system integrates with most of the services to allow
lifecycle and permission of a key that is used for data encryption. decryption
of data can be controll at multiple levels, when, by whom, under which
conditions and etc. the access to data and access to key is also separated to
provide another logical layer of separation. in addition default server side
encryption, one can encrypt data within one's application using the client side
encryption. unauthorize use of KMS keys outside the boundary of KMS are
prevented by utilizing hardware security modules.

for data at transit, AWS encourages to leverage a multi-level approach. all network traffic between AWS data centeris encrypted at physical layer. all traffic bewteen VPC and between peered VPC across regions is encrypted at network layer when using EC2 instances. at application layer one can decide to use TLS encryptions.

## in flight/transit (SSL/TLS)

data is encrypted before sending and decrypted after receiving. TLS certificate
helps with the encryption (HTTPS). this ensures that there is no man in the
middle attach.

## server-side encryption/at rest

data is encrypted after received and is decrypted before sending out. data is
stored encrypted with a key (KMS).

## client side encryption

data is encrypted by client and never decrypted by server but is decrypted by
the receiving client.

[reference](https://docs.aws.amazon.com/whitepapers/latest/logical-separation/encrypting-data-at-rest-and--in-transit.html)