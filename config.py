#!/usr/bin/env python3
import atexit
import pdb
import snort
import stat
import sys
import traffic_shaping
import yaml

atexit.register(traffic_shaping.reset)
atexit.register(snort.restore_iptables)

def read_file(filename):
    data = None
    with open(filename, "r") as fd:
        data = fd.read()

    return data

def main():
    if len(sys.argv) != 2:
        print("Please provide a config file.")
        return
    config_file = sys.argv[1]

    config_data = read_file(config_file)
    config_yaml = yaml.load(config_data)

    bw_dict = config_yaml.get("bandwidth-limits")
    if bw_dict != None:
        traffic_shaping.limit_bandwidth(bw_dict.get("upload"), bw_dict.get("download"))
    snort.set_iptables()
    snort.add_rules(config_yaml.get("ip-rules"))
    snort.add_blacklisted_ips(config_yaml.get("blacklisted-ips"))
    snort.add_whitelisted_ips(config_yaml.get("whitelisted-ips"))
    snort.start_snort()

if __name__ == "__main__":
    main()
