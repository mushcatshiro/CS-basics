[toc]

# working with storage and volumes

keywords: mount points, data sharing, filesystems, storage plugins

questions to think about

- what happen to the postgres image data when we stop the container?
- where is the data stored when the db container is running?
- how to retain data while upgrading the db?
- where should be write the log files to ensure log files outlives the container?
- how to access these log files for both human and log digest tools?

## file trees and mount points

UNIX organize its filesystem into a tree, any storage are attached to specific location in the tree (or mounting points) with access properties. to be precise a mounting point defines the location in the FS tree, determine access properties and source of data. similarly, every container has a MNT namespace and a unique file tree root, thus technically we can mount non related storage to the container. all three mount points can be created using `--mount` flag on `docker run` and `docker create` subcommands.

### bind mounts

these are mount points used to remount parts of a filesystem tree onto other locations. in containers setting, bind mounts attaches a user-specified location on the host filesystem to a specific point in the container filesystem. often the use case is where the host provides a file or director that is needed by a program running in a container or the containerized program produces data that is being processed by entities running outside of the containers. (think some sort of access isolation)

> docker run -d --name service_name \
>
> ​	--mount type=bind, readonly=true, src=\${ conf_src }, dst=\${conf_dst } \
>
> ​    image:tag

*take note 1. paths need to be absolute paths 2. mounted destination's content will always be overwritten*

#### pros and cons

- tied to specific host filesystem thus not portable
- container conflicts eg. cassandra compete for same set of files on same host location
- more towards specialized concerns than generalized application / platforms

### in-memory storage

sensitive information should be stored in-memory

> docker run --rm \
>
> ​	--mount type=tmpfs, dst=/tmp, tmpfs-size=16k, tmpfs-mode=1770 \
>
> ​	--entrypoint mount \
>
> ​	alpine:latest -v

anything writen to /tmp will be in-memory.

### docker volumes

named filesystem managed by Docker. they can be a disk storage on host filesystem or cloud storage. using this method is a way to decouple storage from specialized locations.

#### container-independent data management

a volume is a tool segmenting and sharing data that has a scope of life cycle that's independent of a single container. volume separates concerns and create modularity for architecture components to allow reusability. image is for static contents and volume for dynamic contents. *polymorphic tool* maintains a consistent interface with several implementations to do different things.

> docker run --name some_service -v volume_name:dst/location

*the preferred way to bind mount instead of using* `--mount type=volume`

also volumes is created if it doesn't exists already

### shared mount points and sharing files

able to share access to same set of files between containers is where volumes shines. anonymous volumes existed to address name conflict issue with the unique identifies instead of human friendly names and we can use `--volume-from` flag to copy mount definition from container to container.

#### limitation of volume-from flag

- if the container build needs a shared volume mounted to a different location (no remapping mount points / it just copy exact)
- if volume sources collides only the latest is being mounted
- if different access permission for each mount point

*remember the mount point definition is copy exact*

## cleaning up volumes

anonymous volumes are deleted when the respective creating container is being deleted or manual deletion through `docker volume remove`. names volumes always need to be deleted manually. any volume attached to container in any stage is not delete-able.

## volume plugins

Docker provides volume plugin to extend default dockerengine capabilities by allowing users to use all types of backing storage including cloud, network filesystem mounts, specialized storage hardware and on-prem cloud solutions.