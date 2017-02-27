#!/usr/bin/env python3
import subprocess
from subprocess import PIPE, STDOUT
import shlex

def _fix_queuelen(length=1000):
    subprocess.call(shlex.split("sudo ifconfig docker0 txqueuelen " + str(length)), \
                                 stderr=STDOUT)

def limit_bandwidth(upload_bw, download_bw):
    # Make sure txqueuelen is nonzero for Wondershaper
    # TODO find better values than 1000?
    _fix_queuelen()

    if upload_bw == None or upload_bw <= 1 or download_bw == None or download_bw <= 1:
        raise ValueError("Upload bandwidth and download bandwidth must be greater than 1")

    subprocess.call(shlex.split("sudo wondershaper docker0 " + str(download_bw) + " " + str(upload_bw)), \
                    stderr=STDOUT)


def reset():
    subprocess.call(shlex.split("sudo wondershaper clear docker0"), \
                    stderr=STDOUT)
