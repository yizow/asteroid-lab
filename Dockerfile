# A Docker container to serve as the privileged monitor of all other
# Docker containers.

FROM resin/rpi-raspbian:latest

RUN apt-get update
RUN apt-get install -y vim
# Commented out for now 'cause it takes quite a while to execute,
# and is not needed for Wondershaper testing.
# RUN apt-get upgrade -y

### INSTALLATIONS ###

# Python 3

RUN apt-get install -y python3 python3-pip
COPY ["dockerfile_init/init_pipinstall.sh", "/home/init_pipinstall.sh"]
RUN bash /home/init_pipinstall.sh
# RUN pip install pyyaml docker

# Wondershaper

RUN apt-get install -y make git 

# Interestng observation:  

# If the next 4 lines are included, an error is thrown on the 4th line.
# RUN cd home
# RUN git clone https://github.com/magnific0/wondershaper.git
# RUN cd wondershaper
# RUN make install wondershaper

# However, if a bash script containing these 4 lines is copied over
# and run like so, no error is thrown, and the script executes
# as expected.
COPY ["dockerfile_init/init_wondershaper.sh", "/home/init_wondershaper.sh"]
RUN bash /home/init_wondershaper.sh

# Snort

# Pre-installation
RUN apt-get install -y iputils-ping dnsutils wget curl iptables net-tools \
                       whois tcpdump

RUN apt-get install -y flex bison build-essential checkinstall libpcap-dev \
                       libnet1-dev libpcre3-dev libnetfilter-queue-dev \
                       iptables-dev libdumbnet-dev zlib1g-dev

# DAQ installation
COPY ["dockerfile_init/init_daq.sh", "/home/init_daq.sh"]
RUN bash /home/init_daq.sh

# Snort installation
COPY ["dockerfile_init/init_snortinstall.sh", "/home/init_snortinstall.sh"]
RUN bash /home/init_snortinstall.sh

# Snort post-installation
COPY ["dockerfile_init/init_snortpostinstall.sh", "/home/init_snortpostinstall.sh"]
RUN bash /home/init_snortpostinstall.sh

# Snort copy config and rules files
COPY ["snort/snort.conf", "/etc/snort/snort.conf"]
COPY ["snort/rules/local.rules", "/etc/snort/rules/local.rules"]
COPY ["snort/rules/white_list.rules", "/etc/snort/rules/white_list.rules"]
COPY ["snort/rules/black_list.rules", "/etc/snort/rules/black_list.rules"]

### COPYING FILES POST-INSTALLATION ###

# General Config
COPY ["config.yaml", "config.py", "start_experiment.py", "/home/"]

# Snort
# Not 100% sure where this needs to go:
COPY ["asteroidlab-iptables-backup", "/home/"]

# ENTRYPOINT ["python3", "config.py"]
ENTRYPOINT ["bash"]
