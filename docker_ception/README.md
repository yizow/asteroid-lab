# Docker from Docker

This Dockerfile creates a Docker image that is able to spawn additional docker containers from within it. Note that these spawned containers are not 'children' containers, but 'siblings'. They won't have conflicting security profiles, will share a build cache, and wont lead to docker-within-docker-within-docker, etc.

To do this, the root Docker container must be run with this flag: 
`-v /var/run/docker.sock:/var/run/docker.sock`

## Demo

All the current Dockerfile image does is attempt to `docker run` the default `hello-world` container.

`sudo docker build . -t testing
sudo docker run -v /var/run/docker.sock:/var/run/docker.sock testing`
