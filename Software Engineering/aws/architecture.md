# Architecture

AWS EC2 instance are associated with emphemeral IPv4 IP address. To ensure
the IPv4 address always point to EC2 instance, elastic IP can be used (static),
5 per account. Using elastic IP are usually indicator of bad design, instead
use random public IP + DNS or load balancer with no public IP at all.