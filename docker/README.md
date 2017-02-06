# Asteroid-Lab Administrative Docker Monitor

This contains a Dockerfile that is used to administratively monitor the network activity of other Docker containers. As such, it requires administrative privileges and the host network stack.

The container will modify the host's `iptables` entries to redirect traffic coming in and out of `docker0` to itself, where it will monitor all activity. It does this using `libnetfilter_queue` as well as the Scapy Python library.

# Building

`docker build -t cs194/asteroid-lab .`

# Running

`docker run --privileged -it --net=host cs194/asteroid-lab`
