#!/bin/bash
cd /usr/src/snort_src

wget https://www.snort.org/downloads/snort/snort-2.9.9.0.tar.gz
tar xvfz snort-2.9.9.0.tar.gz

cd snort-2.9.9.0

./configure --enable-sourcefire
make
sudo make install
