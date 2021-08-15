[TOC]

# building images automatically with Dockerfile

keywords: image packaging, metadata and filesystem instructions, multiple stages, image attach surface

*Dockerfile* contains instructions for building an image. the image builder executes the file top to bottom and the instructions can configure or change anything about the image.

example from previous chapter ubuntu image with git

```dockerfile
# Dockerfile
FROM ubuntu:latest
LABEL maintainer="someone"
RUN apt-get update && apt-get install -y git
ENTRYPOINT ["git"]
```

and build with

```bash
>> docker image build --tag ubuntu-git:auto .
```

Dockerfile **must** start with `FROM` unless we are building image from scratch. docker image build image by following each instruction triggers the creation of a new container with the specified modification and commits the layer before moving ono to the next instruction and container created from the fresh layer. docker image builder will cache each layer, thus if there is a build fail, it could restart the build from the last checkpoint.

## Dockerfile primer

### metadata instruction

> ENV, ADD, COPY, LABEL, WORKDIR, VOLUME, EXPOSE, and USER

similar to gitignore, there exists dockerignore file that we can log down files that are not supposed to be copied over to the image. there only difference is we usually don't include the gitignore file itself but its the opposite for dockerignore file.

`WORKDIR` will create a location if it doesn't exists already, `EXPOSE` opens up a corresponding TCP port, `ENTRYPOINT` defines the program to run at container startup. entrypoint instruction have both `shell` form and `exec` form. `exec` form is a string array in which the first value is the command to execute and the remaining values are arguments. `shell` form would be executed as an argument to the default shell, specifically it will be executed as `/bin/sh -c 'exec ./yourfile.sh` at runtime. if `shell` form is used as entry point, all other arguments provided by `CMD` instruction or at runtime (docker container run extra arguments) will be ignored, thus less flexible.

`USER` sets user and group for all further build steps and containers created from the image. setting it in the base image would prevent downstream from installing software, additional layers will be created to change the permission. its recommended to setup the user and group accounts in the base image and let the implementations set the default user when they have finished building.

### filesystem instruction

> COPY, VOLUME, and ADD

`COPY` instruction has one unexpected behavior, any files copied will be copied with the file ownership set to root and there is no way around that. thus it is better to delay any `RUN` instruction to change file ownership until all the files that you need to update have been copied into the image.

#### CMD and ENTRYPOINT

`CMD` represents an argument list for entrypoint and the default entrypoint for a container is `/bin/sh`. if there exists multiple `CMD` only the last one is registered and passed to `ENTRYPOINT`. 

#### ADD and COPY

add fetch remote resource files if a URL is specified and extracts the files of any source determined to be an archive file. however using add to fetch remote files is not a good practice and it provides no mechanism to clean up the unused files.

## injecting downstream build-time behavior

`ONBUILD` is an important instruction for building base images. it defines other instructions to execute of the resulting image is used as a base for another build. we could use `ONBUILD` to compile a program that's provided by a downstream layer.

```dockerfile
ONBUILD COPY [".", "/var/myapp"]
ONBUILD RUN go build /var/myapp
```

the resulting image will copy the content of the build directory into a known location and compiles the code there. these instructions are not executed when their containing Dockerfile is build instead it is recorded in the resulting image's metadata under `ContainerConfig.OnBuild`. the metadata will be carry forward until the resulting image is used as the base for another Dockerfile build. when a downstream Dockerfile uses upstream image with `ONBUILD` instruction, in the `FROM` instruction those `ONBUILD` instructions are executed after the `FROM` instruction and before the next instruction in the Dockerfile.

## creating maintainable Dockerfiles

utilize metadata sharing and data between image's at build time helps creating maintainable Dockerfiles. `ARG` instruction provides a solution to address versioning with images by defining a variable that users can provide to Docker when building an image. Docker inserts the argument value into Dockerfile, allowing creation of parameterized Dockerfiles.

> docker image build --build-arg \<varname\>=\<value\>

```dockerfile
# ...
LABEL base.name="Mailer Archetype" \
	base.version="${VERSION}"
# ...
```

### multistage build

the approach manage important concerns by distinguishing between phases of an image build. a primary uses are reusing parts of another image, separating the build of an application from the build of an application runtime image and enhancing an application's runtime image with specialized test or debug tools. a multistage Dockerfile consist of multiple `FROM` instruction. each `FROM` instruction marks a new build stage whose final layer may be referenced in a downstream stage. each build stage is named by appending `AS <name>` to the `FROM` instruction which `name` is an identifier the user specify. the name can be used in the subsequent `FROM` and `COPY --from=<name|index>` instruction. multistage build will only result in a single docker image, the image produced from the final stage is executed in the Dockerfile.

### startup scripts and multiprocess containers

if the software we are running in the container requires startup assistance, supervision, monitoring and coordination with other in-container processes, a startup script or initialization program is needed to be install as the entrypoint.

failure modes are difficult to communicate and can catch the user off guard if the occur arbitrarily.. it make sense that some preconditions should be evaluated to ensure the software can keep running. Docker containers have no control over the environment where they are created but have control over their own execution. an author can introduce environment and dependency validation prior to execution of main task. preconditions are usually use-case specific, thus a carefully crafted script is usually used to start the program and validate as much of the assumed context as possible including

-  presumed links
- environment variables
- secrets
- network access
- network port availability
- root filesystem mount parameters (read-write or read-only)
- volumes
- current user

shell scripts are most common as it is commonly available and easily adapted. besides startup scripts, restarts policies can also be included to make reliable containers. however they are not perfect solutions. containers that failed and are waiting to be restarted are not running. the operator will not be able to execute another process within the container that's in the middle of a backoff window. the solution is to make sure the container never stops.

### initialization processes

unix based machines usually start with an initialization process and its responsible to start all other system services. init process typically use a file of set of files to describe the ideal state of the initialized system. they describes what program to start, when to start and what actions to take when they are stop. its the best way to launch multiple programs, clean up orphaned processes, monitor processes and automatically restart any failed processes.

if this approach is preferred, the user should use the init process as entrypoint of the application-oriented Docker container. depending on the init program used, the environment needs to be prepared beforehand with a startup script. factors to consider when evaluating any init program

- additional dependencies
- file size
- how the program passes signal to its child processes
- user access
- monitor and restart functionality
- zombie process cleanup

### health checks

`HEALTHCHECK` instruction, or CLI.

```dockerfile
FROM nginx:1.13-alpine
HEALTHCHECK --interval=5s --retries=2 \
	CMD nc -vz -w 2 localhost 80 || exit 1
```

the `HEALTHCHECK` command should be reliable, lightweight and does not interfere with the operation of the main application because it will be executed frequently. the exit status will be used to determine the container health which 0 is success, 1 is unhealthy and 2 is reserved (not to use).

when `HEALTHCHECK` is define `docker ps` reports the container's current health status in the STATUS column.

## build hardened application images

hardening image is the process of shaping it in a way that it will reduce the attach surface inside any Docker containers based on it. a general strategy is to reduce point of failures ie minimize software included. with fewer components it reduces the number of potential vulnerabilities.

- enforce images are build from a specific image
- regardless of how containers is build, a sensible default user is used
- eliminate a common path for root user escalation with `setuid` or `setgid`

### content addressable image identifiers

an image ID that includes the digest component is called content-addressable image identifier which refers to a specific layer containing specific content instead of simply referring to a particular and potentially changing layer. now image authors can enforce a build from a specific and unchanging starting point as long as that image is in a version 2 repo. use `docker image pull` and observer the line `Digest: ` using the CAIID we can use it as the identifier to `FROM` instructions in a Dockerfile. regardless of when and how many times its used to build an image, each build will use the content identified with CAIID as its base image.

### user permissions

docker user can always override image defaults when creating container, thus the best an author can do is to create nonroot usersand establish nonroot default user and group. in general we would like to drop privileges as soon as possible. however if its dropped to early the user may not have the permission to complete the instructions.