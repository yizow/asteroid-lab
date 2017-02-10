#!/bin/bash

apt-get update

apt-get install -y iputils-ping wondershaper speedtest-cli trickle
apt-get install -y apt-transport-https ca-certificates
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
deb https://apt.dockerproject.org/repo raspbian-jessie main

apt-get update
apt-cache policy docker-engine
apt-get update
apt-get install docker-engine
service docker start

