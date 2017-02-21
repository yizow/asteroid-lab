# A Docker container with the basic net-testing tools, so I don't have to keep
# spinning up containers and installing manually

FROM resin/rpi-raspbian:latest

RUN apt-get update
RUN apt-get install -y iputils-ping dnsutils wget curl iptables net-tools \
                       whois tcpdump

ENTRYPOINT ["bash"]
