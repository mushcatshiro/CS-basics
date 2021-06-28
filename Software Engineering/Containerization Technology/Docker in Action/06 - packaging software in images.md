[TOC]

# packaging software in images

keywords: building images, flat images, image versioning

we can create docker image with *Dockerfile*. any changes made to the file system will be written as new layers (recall union file system and copy on write).

## reviewing filesystem changes

```bash
>> docker container run -it --name image-dev ubuntu:latest /bin/bash
(docker container) >>> apt-get update
(docker container) >>> apt-get -y install git
(docker container) >>> touch /helloworld
(docker container) >>> rm /bin/vi
(docker container) >>> echo "asdf" >> .bashrc # assuming there exists a .bashrc file
(docker container) >>> exit
```

and we have a container with ubuntu image, git installed and a directory under root named helloworld. we can check the changes made with `docker container diff image-dev`. the output should look something like this (omitting git as it might be a bit complicated as an example)

```bash
# output
#     A /helloworld
#     C /bin
#     D /bin/vi
#     C /home
#     C /home/user
#     C /home/user/.bashrc
```

take note that delete is a two step process which the parent folder is changed and then the delete operation; change operates similarly too.

## committing a new image

we use `docker container commit` to create an image from a modified container. two important flag including `-a` for adding authorname and `-m` for commit message. we can also set entrypoint such that some program is execute when the container is started with `--entrypoint` flag.

when we commit, a new layer is added. the filesystem snapshot is not the only recorded change, other information including,

- environment variables
- working directory
- exposed ports
- volume definitions
- entrypoint
- command and arguments

are also recorded or carried forward, these values are either inherited or updated.

## deep dive on docker images and layers

### the union filesystem

understanding ufs allows authors,

- impact of modification (adding, deleting and changing) files
- relation between layers and how layers relate to images, repos and tags

imagine viewing the changes from a top-down view, that is what a union filesystem looks like. each time a change is committed the new layer is written on top of the image. any read operation is done by reading the top most layer where that file exists. on delete, the file actually still exists on n-1 layer however there will be a delete record on the top most layer which hides that file from top-down view. on modification it first copies the file to the top-most layer then modifies the content, with this the bottom layer is also hidden.

> note that all layer below the writable layer is immutable

although only file operation (RWX) is discussed here but other filesystem operation are also recorded similarly including eg. ownership and permission. this approach of updating the layers should alarm one when trying to modify large amount of files (be it in one go or multiple attempts), which results in redundant file copies are created. this is the KEY concept to union filesystem, not only image size is impacted, runtime performance will get impacted too.

### images, layers, repositories and tags

UFS is made up of stack layers and new layers are added to the top of the stack. each layers is a collection of changes made in the layer and metadata of that layer. a metadata layer includes a generated identifier, the identifier of the layer below (its a graph!) and the execution context of the container. for each commit a new ID is generated for it and the mentioned data. this further clarifies what a `commit` does.

images are stacks of layers traversing the layer dependencies graph from the top, which implies the layer ID of the top layer is also the ID of the image that it and its dependencies form.

repositories (docker) allows human to work with images ID (hexadecimal numbers) by providing location name pairs that point to a set of specific layer identifiers. each repository contains at least one tag that points to a specific layer ID.

### managing image size and layer limits

supposed we take the image created earlier (ubuntu + git), remove git and commit, the image size actually increases all thanks to UFS as it marks a file as deleted by adding a file to the top layer. this file + file under the top layer still present in the image. user `docker image history`to check

- abbreviated layer ID
- layer age
- initial command of creating container
- total file size of that layer

we can flatten the image by saving the image to a TAR file with `docker image save` and importing it back with `docker image import`, however its not a good approach as we will lose the original image's metadata, change history and more. instead its recommended to branch and build image through an automated fashion. other options including trimming image history or flatten an image.

> earlier there is a max layer limit posed, now its a significant huge number that we are not likely to reach

## exporting and importing flat filesystems

some occasions we are required to work with files destined for an image outside the context of UFS or a container. docker allows exporting and importing archives of files. `docker container export` will stream the full contents of a flattened UFS to stdout or an output file as tarball. `docker import` will stream the content of a tarball into a new image. importing filesystems is a simple way to get a complete minimum set of files into an image.

## versioning best practices

we maintain multiple versions of a same software through tagging. by providing multiple tags for the same version allows user to get the correct version they desired, a bad example would be only tagging say version 1.9.1 to 1.9 and latest and then tags version 1.9.2 with latest and 1.9, this may leads to unexpected behavior. instead provide flexibility by having major version tag eg major version 1 refers to which ever latest major version, minor version 1.9 always to the latest minor patch, and users can choose specific build/revision.

for latest version, provide at least an additional version tag to inform user the exact version they are using. also latest doesn't means latest, it means latest stable version.