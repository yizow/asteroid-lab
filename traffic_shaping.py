#!/usr/bin/env python3
import subprocess
import shlex

def _fix_queuelen(length=1000):
    subprocess.Popen(shlex.split("sudo ifconfig docker0 txqueuelen " + str(length)), \
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def limit_bandwidth(upload_bw, download_bw):
    # Make sure txqueuelen is nonzero for Wondershaper
    # TODO find better values than 1000?
    _fix_queuelen()

    if upload_bw == None or upload_bw <= 1 or download_bw == None or download_bw <= 1:
        raise ValueError("Upload bandwidth and download bandwidth must be greater than 1")

    process = subprocess.Popen(shlex.split("sudo wondershaper docker0 " + str(download_bw) + " " + str(upload_bw)), \
                                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()
    exit_code = process.wait()
    return exit_code


def reset():
    subprocess.Popen(shlex.split("sudo wondershaper clear docker0"), \
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
