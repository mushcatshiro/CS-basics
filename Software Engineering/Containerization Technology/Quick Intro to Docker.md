[TOC]

# docker

## docker under the hood

[youtube Coding Tech](https://www.youtube.com/watch?v=-NzfOhSAZpA&ab_channel=CodingTech)

docker vs VM

- VM run on top of hypervisor - guest OS
- docker run on top of host operating system

both

- runs on top of host OS and infrastructure (hardware)

## namespaces

linux namespaces, *mount namespaces*, *pid*, network namespaces, interprocess communication, *unix timesharing system*, user id

## networking with docker

## bind mounts

a file or directory on the host machine is mounted to a container and is referenced by its absolute path on the host machine; in contrast if we use a volume a new directory is created within docker storage directory on the host machine

## main commands

```dockerfile
# Dockerfile
FROM nginx:latest # image:tag
WORKDIR /your/work/dir
COPY . . # copy all files from $(pwd) to workdir
```

```dockerfile
# docker-compose
version: '3'
services:
  app:
  	container_name: docker-node-name
  	restart: always
  	build: . # specify where the docker file location is
  	ports:
  	  - '80:3000'
  	links:
  	  - mongo # in the app we can specify the ip address eg. localhost to the word 'mongo'
  mongo:
  	container_name: docker-mongo-db
  	image: mongo
  	ports:
  	  - '27017:27017'
```

> .dockerignore similar to .gitignore

```bash
>> docker-compose up -d
>> docker-compose down
```

## some pointers

- images name are not necessarily as you remembered it, go docker hub to check eg apache http server is named httpd
- also for images settings eg database setups visit docker hub too
- remoting to docker container 

> docker container exec -it containername bash

## addressing the k8s deprecation of docker

what k8s deprecate is the redundant components from docker and decouples the reliance on dockershim. instead it will be using containerd as the container runtime. images build by `docker build` complies to the open container initiative thus images will be runnable in any container runtime including containerd, CRI-O or docker.