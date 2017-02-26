#!/bin/bash
mkdir /usr/src/snort_src
cd /usr/src/snort_src

wget https://www.snort.org/downloads/snort/daq-2.0.6.tar.gz
tar xvfz daq-2.0.6.tar.gz

cd daq-2.0.6

./configure
make
sudo make install                  
