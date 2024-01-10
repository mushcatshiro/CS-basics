# Higher-level abstractions and orchestrations

## hello world service orchestrations

any processes, functionality or data that must be discoverable and available
over a network is called a `service`. docker provides `swarm` tooling to work
with services. a `task` is a `swarm` concept that represents a unit of work.
each task is associated to a `service`. with `swarm`, services that are down
are ressurected shortly after they are killed.

![swarm action](./image-20230218101011.PNG)

`swarm` can also replicate $n$ unit of work specified by user by specifying in
replicated mode,

```
docker service scale hello-world=3
```

take note that when scaling down wiht `...scale hello-world=2` the last
last container will be remove first. in global mode, docker runs one replica on
each node in the swarm cluster.

### automated rollout

![service update](./image-20230218102211.PNG)

deployment charateristics should be described including order, batch size and
delays. `service converged` will be printout to indicate rollout success. in
real world people usually use parallelism to balance the time taken to update
service. they introduce delays between update batches to allow new service
instance to become stable before starting. note that docker and swarm are app
agnostic, any app behavior is up to app developer to handle it, docker and
swarm only maintains the desire state of the cluster (?) by validating the
current state.

```bash
>> docker service update --image someimage:sometag somename
```

### service health and rollback

given a 3 node cluster if user updates the service that always fails to start,
user can observed that there are 2 nodes remains on the old version of service
and 1 node alternating between start and failed state. the cluster will be in
stuck in such state and not able to proceed with the deployment. in such
scenario, using the `--rollback` flag on the update command. docker will figure
out that only 1 container need such rollback. it is possible that one
deployment involved hundreds of nodes and it would be challenging to manage it.
docker provides `--update-failure-action` and `--update-max-failure-ratio` flag
to address such problem.

docker only cares about the service state not health. it is up to the user to
define how docker should determine system is healthy. docker will execute that
command periodically to validate.

## declarative service environment

docker compose is a descriptive specification for docker stack which is a
collection of services, volumes, networks and etc. 