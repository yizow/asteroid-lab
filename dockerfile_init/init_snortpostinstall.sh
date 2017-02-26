#!/bin/bash

ldconfig
snort --version # verify snort version info is displayed

# If not displayed, uncomment the following to create symlink:

# sudo ln -s /usr/local/bin/snort /usr/sbin/snort
# snort --version

# Unrooting snort

sudo groupadd snort
sudo useradd snort -r -s /sbin/nologin -c SNORT_IDS -g snort

sudo mkdir /etc/snort
sudo mkdir /etc/snort/rules
sudo mkdir /etc/snort/preproc_rules
sudo touch /etc/snort/rules/white_list.rules /etc/snort/rules/black_list.rules /etc/snort/rules/local.rules
sudo touch /etc/snort/preproc_rules/decoder.rules /etc/snort/preproc_rules/preprocessor.rules /etc/snort/preproc_rules/sensitive-data.rules

sudo mkdir /var/log/snort

sudo mkdir /usr/local/lib/snort_dynamicrules

sudo chmod -R 5775 /etc/snort
sudo chmod -R 5775 /var/log/snort
sudo chmod -R 5775 /usr/local/lib/snort_dynamicrules
sudo chown -R snort:snort /etc/snort
sudo chown -R snort:snort /var/log/snort
sudo chown -R snort:snort /usr/local/lib/snort_dynamicrules

# Setting up config files
sudo cp /usr/src/snort_src/snort*/etc/*.conf* /etc/snort
sudo cp /usr/src/snort_src/snort*/etc/*.map /etc/snort

# Test snort
# snort -T -c /etc/snort/snort.conf
