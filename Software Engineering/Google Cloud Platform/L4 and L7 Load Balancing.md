# L4 and L7 Load Balancing

in OSI model L4 and L7 each refers to transport layer and application layer respectively. L4 load balancing is a convinience naming for L3/L4 load balancing, which utilized both IP address from L3 and TCP port number from L4 to enable load balancing. from the network models, message that passed from a node to another is encapsulated through the layers and being handled at the destination layer by layer. thus, at L3/L4 the most valuable information available are IP address and TCP port number. there are only a handful of things that the load balancer at this level can do. contrasting to a l7 http load balancer, it has http header and payload for a smarter routing eg. auth-header for returning 401 status code etc. the merit of L4 balancing is it has lower overhead especially for cheap hardware.

## L4 load balancing

done at packet by packet basis through NAT. it changes the recorded destinatino IP from the load balancer's to the actual backend and vice versa for the reverse (IP and port). often requires a dedicated hardware + proprietary software.

### to validate
another concern at l4 load balancing is where once a TCP connection is made, the source can potentially flood the destination with high qps thus rendering L4 load balancing useless?

## reference

- [Nginx L4 LB](https://www.nginx.com/resources/glossary/layer-4-load-balancing/)