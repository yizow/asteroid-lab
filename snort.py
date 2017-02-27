#!/usr/bin/env python3
import subprocess
from subprocess import PIPE
import shlex

LOCAL_RULES_FILE = "/etc/snort/rules/local.rules"
BLACKLIST_FILE = "/etc/snort/rules/black_list.rules"
ASTEROIDLAB_IPTABLES_FILE = "asteroidlab-iptables-backup" #TODO fix path?
IPTABLES_BACKUP_FILE = "iptables-backup"
DAQ_DIR = "/usr/local/lib/daq"
SNORT_CONF = "/etc/snort/snort.conf"

directions = {
    "both": "<>",
    "to": "->",
    "from": "<-"
}

def _write_file(filename, data):
    with open(filename, "w") as fd:
        fd.write(data)

def add_rules(rules_list):
    if rules_list != None:
        rule_out = ""
        for rule in rules_list:
            rule_out += "{behavior} {protocol} any any {direction} {ip} {port}\n".format(
                behavior=rule["behavior"],
                protocol=rule["protocol"],
                direction=directions[rule["direction"]],
                ip=rule["ip"],
                port=rule["port"]
            )

        _write_file(LOCAL_RULES_FILE, rule_out)

def add_blacklisted_ips(ips_list):
    if ips_list != None:
        blacklist = ""
        for ip in ips_list:
            blacklist += "{address}\n".format(address=ip)

        _write_file(BLACKLIST_FILE, blacklist)

def add_whitelisted_ips(ips_list):
    if ips_list != None:
        whitelist = ""
        for ip in ips_list:
            whitelist += "{address}\n".format(address=ip)

        _write_file(WHITELIST_FILE, whitelist)

def set_iptables():
    subprocess.call(shlex.split("sudo iptables-backup > " + IPTABLES_BACKUP_FILE), \
                    stderr=PIPE)
    popen = subprocess.call(shlex.split("sudo iptables-restore < " + ASTEROIDLAB_IPTABLES_FILE), \
                            stderr=PIPE)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()

def restore_iptables():
    subprocess.call(shlex.split("sudo iptables-restore < " + IPTABLES_BACKUP_FILE), \
                    stderr=PIPE)

def start_snort():
    subprocess.call(shlex.split("sudo snort -Q --daq nfq --daq-dir " + DAQ_DIR + " -c " + SNORT_CONF), \
                    stderr=PIPE)
