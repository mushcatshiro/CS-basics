[TOC]

# networking

virtual private network is global for GCP but regional for AWS. thus if we have 2 VMs created in London and Singapore as long as they stay in the same VPC the can communicate through internal IPs.

## hands-on

### within same project

config: 
- us-central1 us-central1-a E2 e2micro allow http traffic
- us-central1 us-central1-b E2 e2micro allow http traffic
- asia-southeast1 asia-southeast1-b E1 e2micron allow http traffic
- [echo-server](https://github.com/mushcatshiro/echo-server.git)

```bash
# same project:
>> curl -X POST "internal IP":8000/pong -d '{"msg":"test"}' -H "Content-Type: application/json"
# same zone/different zone/different region/external
# >> {"msg":"replying instance-1@"internal IP" with test"}
# note serve at 0.0.0.0
# note for http traffic allowed one should have an web server listening and forward the port correctly

# different project
>> curl -X POST "external IP"/pong -d '{"msg":"test"}' -H "Content-Type: application/json"
# same zone/different region
# >> {"msg":"replying instance-1@"other project's internal IP" with test"}
```

### setting up VPC peering

## cloud NAT

using cloud NAT allows outgoing connections. if external IP does not exists no outgoing connection can be made. by creating a cloud NAT (and router) at the SAME region as the instance that wish to have outgoing connections.

## load balancing

## todo

- [ ] no external IP but wish to access from Internet? (IAP?)
- [ ] both project no external IP?