#!bin/bash

apt-get update

apt-get -y install iputils-ping wondershaper speedtest-cli trickle \
                   docker


usermod -aG docker $(whoami)
