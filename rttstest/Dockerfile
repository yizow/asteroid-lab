FROM resin/rpi-raspbian

RUN apt-get update
RUN apt-get install -y python python-pip \
                       dnsutils

COPY rtts.py .
COPY alexa_top_5 .

ENTRYPOINT ["python"]
CMD ["rtts.py"]