 # Virtual Private Cloud

an on demand configurable pool of shared resource allocated within a public cloud. provides a certain level of isolation between different entities using the resources. the isolation between entities is achieved normally through allocatin of a private IP subnet and a virtual communication construct per entity. VPC is accompanied with VPN function (per user) that secures (auth and encryption) the remote access of the entity to its VPC resources. virtual private properties is achieved through such isolation, as if they are not on the same public cloud infrastructure hence the name VPC.

NAT gateway or network address translation service allows instances in a 
private subnet to connect to services out of VPC but external cannot initiate
a connection in.