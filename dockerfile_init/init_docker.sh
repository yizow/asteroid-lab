#!/bin/bash

sudo apt-get install -y libapparmor1 libltdl7

sudo mkdir /usr/src/docker
cd /usr/src/docker

sudo wget https://apt.dockerproject.org/repo/pool/main/d/docker-engine/docker-engine_1.13.1-0~raspbian-jessie_armhf.deb

sudo dpkg -i /usr/src/docker/docker-engine_1.13.1-0~raspbian-jessie_armhf.deb

sudo service docker start
