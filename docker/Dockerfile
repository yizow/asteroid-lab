FROM ubuntu:16.04

RUN apt-get -y update && apt-get -y install iptables libnetfilter-queue-dev python python-scapy nfqueue-bindings-python tcpdump 

ADD run-docker-mon /usr/bin/run-docker-mon
ADD docker-mon /usr/bin/docker-mon

CMD ["/usr/bin/run-docker-mon"]
