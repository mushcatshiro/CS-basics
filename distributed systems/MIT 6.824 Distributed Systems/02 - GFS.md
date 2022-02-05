[TOC]

# GFS

to build a big storage system, which is a key abstraction (a simple storage interface) for real world application. a few theme the GFS paper mentioned including,

- parallel performance
- fault tolerance
- replication
- consistency

to harness the aggregate performance of thousands of machines, ie performance through sharding. however there is more to it, to get better performance through sharding, we need to handle faults through tolerance, and to achieve tolerance we need replication, with replication we need to address consistency and lastly to maintain consistency its required additional costs or it will negatively impact performance. in short, good/strong consistency is where the system behave as if we are communicating to a single server. note GFS is optimized for big sequential access which is opposed to bank transaction where all updates are relatively small and random access.

## architecture and design

master data

- filename -> array of chunk handles
- handle -> list of chunk servers, version number for each chunk, primary chunk, lease expiration
- on disk log and checkpoints (to prevent the need of recovering from begining of time) for recovery.

read operation

1. filename and offset -> master
2. master returns chunk handler and list of servers, client cashes for future use
3. client -> chunk servers

write operation (append)

case 1. no primary on master

1. find up to date replicas
2. picks one to be primary and secondary, increments version number and returns these three information to client
3. master gives a lease to primary
4. client informs all primary and secondary information to append
5. primary and secondaries will stage to temp area, wait for received ACK, then primary picks a suitable offset before actually write happens
6. if all secondaries returns write success to primary, primary will inform client; else stop the current transaction and restarts by communicating with master again

> note, those secondaries that updates successfully will remains updated

> split brain is where we have two primaries due to network partition/error. to address this thus the use of lease, and master will assumes the primary is alive although not ping-able throughout the lease duration.

### introducing strong consistency to GFS

GFS is not real strong consistency.

- primary be able to detect duplicated requests
- secondary have to execute the request from primary, and if it has permanent problems there should be a mechanism to remove it as an secondary
- secondaries should not expose and newly append data until primary is sure that the execution is completed and successful (two phase commit)
- new primary should resync the tail of their operation when the old primary crashes while it has issued some operations
- reads from primary only when there is conflicting/stale information and when the secondaries can't legally respond

### problems with GFS

- feasibility of having the master to store those information in memory
- some application are not suitable for such odd chunk semantics
- master failover is not automatic

___

## reference material

- google file system paper [link](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf)