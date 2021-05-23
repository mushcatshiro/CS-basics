[TOC]

# limiting risk with resource controls

keywords: resource limit, memory sharing, permission, privileges, access

containers provide isolated process but not full system virtualization. four isolation feature set will be discussed to help enhancing system security.

## resource allowances

resource overconsumption of processes will leads to performance issues and / or causes to process stop running. resource allowance is part of building a strong isolated system such that a single program will not overconsume resources planned for other programs. by default docker containers may use UNLIMITED CPU, memory, and device I/O.

### memory limits

useful to ensure that one container can't allocate the entire system's memory by using the `-m` flag which follows by a number and units (b, k, m, or g). setting memory limits doesn't guarantee the specified memory to be available but rather a protection from overconsumption. to gauge a appropriate memory limit we can run the container on real workloads and use `docker stats`. however we could set a larger memory size than our machine's ram (extends memory into disk), thus its something for the developer to consider. if the software fails due to memory exhaustion, docker doesn't defects or attempts to resolve this issue, the easiest thing we can do is to restart the container.

### cpu limits

when cpu resource (processing time) runs out, performance is impacted instead of failure. process will pause and wait for the CPU which could be worse than failing one for latency-sensitive data-processing program. CPU resources can be restricted by specifying relative weight of a container to other containers or specifying the total amount of CPU used by a container.

for the first method, by using the flag `--cpu-shares` and follow by an **integer**, the percentages for the sum of the computing cycles of all processors available to the container. these cpu shares are different from the memory limits where they are enforced only when there is a contention for CPU, but if all processes are on idling, one process could burst beyond limits. 

for the second method, use the `cpus` option which allocates a quota of CPU resources or number of CPU cores the container may use by configuring the linux completely fair scheduler (CFS). these CPU quota is allocated, enforced and refreshed at every 100ms interval by default. if the CPU quota is exceeded its CPU usage will be throttled until the next measurement period begins.

