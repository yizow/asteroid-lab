FROM resin/rpi-raspbian:latest

MAINTAINER cwang395

RUN apt-get update
RUN apt-get install -y iputils-ping net-tools bridge-utils \
                    	 wget

ENTRYPOINT ["wget"]
CMD ["-O /dev/null http://speedtest.fremont.linode.com/100MB-fremont.bin"]
