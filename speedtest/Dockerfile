FROM resin/rpi-raspbian:latest

MAINTAINER cwang395

RUN apt-get update
RUN apt-get install -y iputils-ping \
	python-pip python-dev build-essential
	# speedtest-cli
RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv
RUN pip install speedtest-cli

# COPY netpps.sh ~/
# COPY netspeed.sh ~/

# RUN wget -O speedtest  https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py
# RUN chmod +x speedtest

# ENTRYPOINT ["~/netspeed.sh", "eth0"]
# ENTRYPOINT ["ping", "google.com"]
CMD ["speedtest-cli"]
