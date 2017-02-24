#!/usr/bin/env python3
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
    if len(sys.argv != 2):
        print("Please provide a config file.")
        return
    config_file = sys.argv[1]

    config_data = read_file(config_file)
    config_yaml = yaml.load(config_data)

    traffic_shaping.limit_bandwidth(config_yaml["bandwidth-limits"]["upload"],
                                    config_yaml["bandwidth-limits"]["download"])
    snort.set_iptables()
    snort.add_rules(config_yaml["ip-rules"])
    snort.add_blacklisted_ips(config_yaml["blacklisted-ips"])
    snort.add_whitelisted_ips(config_yaml["whitelisted-ips"])

if __name__ == "__main__":
    main()
