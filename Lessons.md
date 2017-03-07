# Asteroid Lab: Lessons Learned

## Contents

i.  Then, and Now
ii.  Supported Features
iii.  Networking in Docker

## I. Then, and Now

In a nutshell, the goal of Asteroid Lab was to implement a distributed virtual network as a testbed for networking experiments.  In deviating from its predecessors, such as Planet Lab and GENI,  we strove to accomplish this with modern, easily-accessible sofware and hardware:  running Docker on Raspberry Pi's.

The initial trajectory and scope for Asteroid Lab can be found in our repository's [README](https://github.com/yizow/asteroid-lab/blob/master/README.md).  However, over the several weeks following its drafing, both our focus as well as implementation direction have somewhat changed course.  Specifically, attention was heavily directed towards the feasibility of providing network security on behalf of the owner of a volunteered machine, whilst allowing otherwise raw network access to experimentors.

This document serves to describe the current implementation of Asteroid Lab, as well as the myriad difficulties and decisions encountered along the way.

## II. Supported Features

Asteriod Lab guarantees that any owner of a machine volunteered into Asteroid Lab's network can define limits on the hardware and network resources available to experiments.  Specifically, one can restrict operations or filter traffic by:

- CPU usage
- Memory usage
- Network bandwidth
- IP address
- Hostname
- Port
- Protocol

See our [Owner Specification](https://github.com/yizow/asteroid-lab/blob/master/Asteroid%20Lab%20Owner%20Specification.md) for a detailing of the semantics and extent to which each can be done.

## III. Networking in Docker

### Environment Setup

(Dockerfile details)

### Traffic Shaping

**Lessons learned:** Knowledge of Linux networking and terminology is helpful if you want to really understand the quirks of Docker networking. The solution to your problem may be simpler than you expect. 

**Problem:** We tried to use Wondershaper to throtle the bandwidth of our Docker containers, but if we used this tool to set *any* limit on the bandwidth, no matter how high, the traffic going in/out of the containers would eventually fall to 0.

**Attempted solutions:** Using a different OS, using other traffic-shaping tools (not helpful as most of them are based on the same `tc` and `qdisc` technology)

**Solution:** Was staring us in the face whenever we ran `ifconfig`. Wondershaper relied on the `txqueuelen` value of the `docker0` bridge, as suggested by [this GitHub issue](https://github.com/kubernetes/kubernetes/issues/25092) for Kubernetes:

> It seems the *fifo qdiscs default their packet limit to the txquelen of the interface (man tc-pfifo). It also seems most virtual interface types (bridge, etc) set a dev->tx_queue_len of 0. It further seems that pkg/util/bandwidth/linux.go relies on the default packet limit...

The value was `0` by default, so Wondershaper would end up dropping all packets. Easily fixed by running `sudo ifconfig docker0 txqueuelen <nonzero queue length>`

### Packet Sniffing/Dropping

**Lessons learned:** Adding `config daq-mode: inline` to a Snort rule file, or even specifying `--daq-mode inline` on the command line, is *not* equivalent to specifying `-Q`.

**Problem:** Snort wasn't reading any of the `drop` or `reject` rules we'd written in our rules file when we used the nfq daq, although we didn't realize this at first.

**Attempted solutions:** Proofreading the Snort file, adding `--daq-mode inline` on the command line

**Solutions:** Adding `-Q` to the call to Snort, via lucky guess.

### Ambiguous Packet Reassembly

(packet reassembly protection/attacks details)

