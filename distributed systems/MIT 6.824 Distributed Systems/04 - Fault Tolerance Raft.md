[TOC]

# Fault Tolerance with Raft

to get state replication machine correct. after going through VMware-FT, GFS and mapreduce, it is not difficult to realize that they share one common thing - single entity that decides the most critical operation. It is simple however it also a single point of failure, which is something undesired in production. to address this, we can have multiple primaries, with a new challenge, split brains.

## Split Brains

say we have two client and two server (p/b), if

- we are required to talk to both servers before we are able to proceed, or
- we just need to talk to either one of the server to proceed

we are essentially risking to either being not fault tolerant or being incorrect, and being incorrect is called split brain.

> we can build system that can deal with flaky network, where client 1 can only talk to server 1 and client 2 only to server 2, also known as the partition.

### Majority Vote (qourum system)

is how we deal with split brain, the main concept of raft. With an odd number of servers, to make progress of any kind, majority votes are required. note the majority here refers the majority of **all servers** not just the live servers. if we have $2f + 1$ servers we can withstand $f$ server failures. for every network partitions, we can only have one majority. another subtlety is that we need at least one overlapping server in the majority, which is also a property that allows raft to avoid split brain.

## Raft

raft is supposed to be a library complimentary to some other application code to maintain replication. a simple example of how would things work is as follows,

- client issues a PUT (or any) request to a KV store
- KV store (application layer) communicates to raft layer
- raft talks between other raft servers to ensure all or the majority of the replicas get the new operation into their log
- upon confirmation the raft leader will inform the KV store replication is done
- KV store proceed to execute the PUT (or any) request

depending on the design the leader could issue an execute command through heartbeat ping or as an additional message. it is not so critical for the replicas to execute these operation as essentially no one is waiting for it until there is a failure. however log is critical, 

- to ensure the operation execution order
- these yet to be committed operation in logs might need to be discarded
- allow the leader to resend the operations to replicas that having failures
- allowing a crashed server to rejoin the raft cluster easily by recreating state

> in a production software we probably would need a throttling mechanism ie by informing the leader if a replica is lagging in terms of executed commands to prevent running out of memory storing these logs?

### On leader election

we could build a system without having leader, so why having one? we could build a more efficient system if the system don't fail with **one round trip** of messages, and for interpretability. in each term we can only have at **most one leader**, or no leader. each raft instance have a election timer, if until the term ends and there is no message from the current leader, the server will assume the current leader is dead and starts an election. starting election is basically increment the term number, nominate and vote for itself, and ask for $n/2$ request votes. if the leader does fail we will have election, but it is not always the case. the new leader is required to send out a heartbeat with an append entry. this heartbeat will also acts as a suppressor of the election timer and ask the fleet to update their election timer to a new value. setting the minimum election timer is a bit of art but generally it must be at least $n$ times of heartbeat interval. as for maximum election timer is gives the idea of how long does the system can recover from losing a leader (failure).

> note between leader failure and next leader elected, all client requests are rejected.

also the interval between different timer should be at least long enough for a candidate to collect the majority of the votes.

**On a new leader sorting out the failure**

how would the logs behave? note by looking at the log we will not be able to tell how far the leader has got before crashing. leader will check all followers previous index and term, if its matched then to sync and if not match the next index to check will be $index - 1$ until its matched and to drop everything after the matched index and accept the leaders log record. backtrack and backup.

> why?

### why not longest log as leader?

it is not suitable in raft design but it is perfectly fine with other system design.

| Server/Term |      |      |      |
| ----------- | ---- | ---- | ---- |
| S1          | 5    | 6    | 7    |
| S2          | 5    | 8    |      |
| S3          | 5    | 8    |      |

term 8 would have been committed, overwriting with 6 and 7 is not reasonable.

### fast backup

case 1.

| Server/Term |      |      |      |      |
| ----------- | ---- | ---- | ---- | ---- |
| S1          | 4    | 5    | 5    |      |
| S2          | 4    | 6    | 6    | 6    |

case 2.

| Server/Term |      |      |      |      |
| ----------- | ---- | ---- | ---- | ---- |
| S1          | 4    | 4    | 4    |      |
| S2          | 4    | 6    | 6    | 6    |

case 3.

| Server/Term |      |      |      |      |
| ----------- | ---- | ---- | ---- | ---- |
| S1          | 4    |      |      |      |
| S2          | 4    | 6    | 6    | 6    |

append entry reply with,

- xterm, term of conflicting entry
- xindex, index of first entry with xterm
- xlen, length of log

### persistent

- log, only record of application state
- current term, to prevent same term number for split groups which executes different commands
- voted for, to prevent voting for multiple leader in the same term

note writing to persistent is slow ~10ms (time for head to spin or pointer to point in mechanical drive) which is far slower than any other operations, so we should be smart enough to choose when we should write to disk. **synchronous disk updates** are extremely expensive.

### log compacting and snapsnots

in most application, the application state is much smaller than the log, therefore a snapshot up to a certain point in log. upon snapshotting we can throw away the log before that chosen checkpoint.

## Correctness

Linearizability, execution history is linearizable if there exists a total order of operation in history it matches the real time order for a non concurrent request and reach read sees most recent write in order.

___

## reference and reading material

- raft paper [link](https://raft.github.io/raft.pdf)
- paxos
- VSR (view stamp replication)