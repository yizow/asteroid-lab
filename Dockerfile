# A Docker container to serve as the privileged monitor of all other
# Docker containers.

FROM resin/rpi-raspbian:latest

RUN apt-get update
# TODO add all packages for wondershaper + snort
RUN apt-get install -y iputils-ping dnsutils wget curl iptables net-tools \
                       whois tcpdump

COPY ["config.yaml", "config.py", "start_experiment.py", "."]
COPY ["snort/snort.conf", "/etc/snort/snort.conf"]

ENTRYPOINT ["python", "config.py", "config.yaml"]
