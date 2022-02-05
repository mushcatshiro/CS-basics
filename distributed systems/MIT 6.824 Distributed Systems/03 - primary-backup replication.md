[TOC]

# Primary-Backup Replication

Failures address by replication are fail-stop faults of a single computer which refers to if anything goes wrong the computer just stops executing. what is not covered by replication are like bugs or design defects of software or hardware etc. other limitations are when the failures are dependent or natural disaster recovery, replication also cant help with it. also do we really need replications? its taking up nx amount of resources and if only its monolith we would not have need to suffer from all the additional work to maintain or achieve CAP.

> note fail stop might be content dependent, a scenario might be considered fail stop for a particular system and software but not for others.

there are two approaches to replicas

1. state transfer - the primary sends a copy of its entire states to the replica
2. replicated state machine - just sends the external events that causes changes in state (GFS paper)

2 is more efficient as the data packet is likely to be smaller, however with more assumptions to the system/machines. there are niche operations that are guaranteed to be different in different machines for example getting local time or getting PID etc. these operations should be handled by the primary and it instructs the secondaries to just execute with the primary's value.

> GFS paper is discussed in a single core machine?

> VMware using state transfer for replicas as it is more robust in the face of multi-core parallelism

a few issue to address for using replicated state machine

- what state should we transfer i.e. what level? inputs? operation? instruction?
- p/b sync interval
- cut-over and anomalies
- bring up a new replica when one of them fails (essentially it will be expensive as state transfer is needed)

## on *replicating state (machine)*

replication scheme as detailed as low level registers and memory between primary and backup is rare however it also allows it to be application agnostic, unlike conventional replicated state machine which heavily relies on application level sync. the vmware FT paper experiment setup is to have two hardware and on each to have a VM spawn with the same os and application. the sync is through LAN with an external disk server. through interrupts, VM sync the state through log entries over the communication channel, thus backup actually executes the same command the primary was requested but the packet is dropped. in the case where the channel is not transmitting packets, the system will assume either machine is down and will operates as if its a single machine system without backup.

### contentious problem

there are still non-deterministic behavior/events,

- inputs - data + interrupt
- weird instructions (uuid, time etc)
- multi-core parallelism is not supported as the instruction will be interleaved in a unpredictable manner

> isn't this conflicts to the statement above?

___

## references

- fault-tolerant VMs [link](http://nil.csail.mit.edu/6.824/2020/papers/vm-ft.pdf)
