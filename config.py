#!/usr/bin/env python3
import argparse
import atexit
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
    parser = argparse.ArgumentParser(description="Configure Asteroid-Lab monitor container with appropriate rules.")
    parser.add_argument("config", help="Config file to determine container limitations.")
    parser.add_argument("--snort-rules", help="User-provided Snort rules.")
    args = parser.parse_args()

    snort_rules_file = args.snort_rules

    config_data = read_file(args.config)
    config_yaml = yaml.load(config_data)

    bw_dict = config_yaml.get("bandwidth-limits")
    if bw_dict != None:
        traffic_shaping.limit_bandwidth(bw_dict.get("upload"), bw_dict.get("download"))

    snort.set_iptables()
    snort.add_rules(config_yaml.get("ip-rules"))
    snort.add_blacklisted_ips(config_yaml.get("blacklisted-ips"))
    snort.add_whitelisted_ips(config_yaml.get("whitelisted-ips"))
    snort.start_snort(snort_rules_file=snort_rules_file)

if __name__ == "__main__":
    main()
