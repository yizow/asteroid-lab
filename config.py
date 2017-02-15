#!/usr/bin/env python3
import os
import stat
import yaml

CONFIG_YAML = "config.yaml"

RUN_TEMPLATE = "run.sh.tmpl"
RUN_OUTPUT = "run.sh"

RULES_OUTPUT = "asteroid.rules"

directions = {
    "both": "<>",
    "to": "->",
    "from": "<-"
}

def read_file(filename):
    data = None
    with open(filename, "r") as fd:
        data = fd.read()

    return data

def write_file(filename, data):
    with open(filename, "w") as fd:
        fd.write(data)

def main():
    config_data = read_file(CONFIG_YAML)
    config_yaml = yaml.load(config_data)

    tmpl_data = read_file(RUN_TEMPLATE)
    run_out = tmpl_data.format(
        filename=RULES_OUTPUT,
        download_bw=config_yaml["bandwidth-limits"]["download"],
        upload_bw=config_yaml["bandwidth-limits"]["upload"]
    )

    write_file(RUN_OUTPUT, run_out)
    os.chmod(RUN_OUTPUT, stat.S_IRWXU|stat.S_IRWXG)

    rule_out = ""

    for rule in config_yaml["ip-rules"]:
        rule_out += "{behavior} {protocol} any any {direction} {ip} {port}\n".format(
            behavior=rule["behavior"],
            protocol=rule["protocol"],
            direction=directions[rule["direction"]],
            ip=rule["ip"],
            port=rule["port"]
        )

    write_file(RULES_OUTPUT, rule_out)

    print("Files generated. Please run {}.".format(RUN_OUTPUT))

if __name__ == "__main__":
    main()
