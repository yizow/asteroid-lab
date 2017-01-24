# Asteroid-Lab

Asteroid-Lab allows researchers, academic or not, to perform experiments on a virtual network, achieved by creating a distributed system comprised of cheap yet widespread hardware.

Though there are previous concepts that have tackled this idea, specifically GENI and Planet-Lab, we aim to improve upon these by modernizing their architecture using technologies such as Docker and low-cost computers like the Raspberry Pi.

Specifically, Asteroid-Lab will accomplish this through the following:

1. Raspberry Pis (nodes) will run a consistent Docker container.
2. Researchers will have a mechanism to specify an experiment, specify its resource requirements, and submit said experiment.
    1. Submitted experiments will be able to run on selected nodes.
3. Owners of nodes will have a mechanism to specify resource usage permissions on said nodes.
4. Researchers will have raw network access to the nodes running their experiment.

# Motivation

A major benefit to having a distributed experimentation system such as Asteroid-Lab is its ability to be geographically distributed. Being able to have individual experiment nodes and clusters of nodes located in different locales allows researchers to collect data that differs by location such as latency and local network topology. In addition, it allows us to build a more robust system that can remain online in the face of failure in certain nodes.

We choose to utilize containerization technologies, specifically Docker, as it simplifies system deployment, being a commonly-used system, as well as consistency regardless of the host's hardware. Docker also provides security by isolating all the system resources from the host.

# Prior Research

Asteroid-Lab is inspired by two other organizations that provide essentially the same services, GENI and Planet-Lab. However, the infrastructure behind these two have aged a fair amount and do not take advantage of modern frameworks, and as a result the methodology to get a node running or to perform an experiment are more complicated than necessary.

For example, Planet-Lab relies on VMs and specialized hardware in its implementation of experiment slices across physical machines. While the idea and architecture of Planet-Lab are useful, Docker containers are much lighter than VMs.

GENI also requires the installation of specialized hardware, creating a significant effective cost and effort barrier to hosting a GENI experiment site. By implementing an architecture similar to GENI and Planet-Lab on inexpensive and easily obtainable Raspberry Pis, we hope to address this major shortcoming in the GENI framework.

# Methodology

## Broad Architecture

An experimenter on Asteroid-Lab requests a "slice" of resources for their experiment, with minimum CPU, bandwidth, and memory requirements. Each slice represents a share of resources across multiple Asteroid-Lab nodes, and in practice is implemented as a network of Docker containers across multiple Docker hosts.

## Specifics

### Nodes
Each node is a Raspberry Pi with Docker Engine installed, hosting at most one container per experiment running in the Asteroid-Lab universe. A "slice" of resources therefore consists of containers spanning multiple machines, with each machine hosting a "sliver", or piece of the slice. 

### Node discovery and resource allocation
We are currently exploring two different ways of doing this.

In the first, each Raspberry Pi is preconfigured with the public IP addresses of tracking servers. When a new node it boots up, it contacts one or more of these tracking servers (chosen according to location, or at random, etc.). The node and server perform some authentication handshake to associate this node with an owner’s account. It also informs the tracking server of the hardware resources the node's owner has chosen to make available for Asteroid-Lab, and periodically updates this information. Tracking servers are responsible for maintaining a list of uniquely identifiable nodes, tracking what resources are available on each node, and responding to resource allocation requests. In this way, they play a similar role to Aggregate Managers in the [GENI architecture](http://www.geni.net/documentation/geni-architecture/) and Management Authorities in the [Planet-Lab architecture](https://www.planet-lab.org/files/pdn/PDN-06-031/pdn-06-031.pdf).

Resource allocation requests come from a server interface used by experimenters. This server will ask each tracking server for a lease on resources that match a hardware requirement specification provided by the experimenter. The particular details of the specification still need to be hashed out.

We’ve also considered having nodes self-organize to reduce the load on tracking servers. However, this opens up a number of other questions, such as: who does the experimenters interface contact in order to make a resource allocation request? What bounds on efficiency can we make if there is no central service that is aware of what resources are available? How do nodes communicate directly with each other, given that most of these nodes will be behind NATs (1 possible way to mitigate this: require nodes to have a public IP?)?

It seems possible that we could merge these two designs by, for example, having the nodes choose other nodes as tracking servers for various time intervals.

### Node control and isolation
We hope to leverage [Docker Swarm](https://docs.docker.com/engine/swarm/) to orchestrate the nodes in a single slice for each experiment and keep experiments isolated from each other and from the host machines.

### Raw network access for experiments
Our research indicates that Docker does the hard work for us here. By default, containers have their own network interface, isolated from the host. We’re still determining how exactly to make containers networks isolated from each other, but this is certainly possible. [Overlay networks in Swarm mode](https://docs.docker.com/engine/userguide/networking/#/an-overlay-network-with-docker-engine-swarm-mode) look particularly promising.

# Materials

We are requesting as many Raspberry Pis, with peripherals, as is possible. Because of the distributed nature of our system, we require a cluster of Raspberry Pi that we can control. At the least, we would like to have 10.

- $N$ of Raspberry Pi Model 3 B, with peripherals for each:
    - 32 GB microSD card
    - Cat5e Ethernet cable
    - USB micro-B to USB A cable
- Power strips
- USB power hubs
- Gigabit Ethernet switch

