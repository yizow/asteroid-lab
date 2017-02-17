import subprocess
from subprocess import PIPE

def run_ping_from_file(hostname_filename):
    with open(hostname_filename) as hostname_file:
        hostnames = hostname_file.read().strip().split("\n")

    run_ping(hostnames, 50)

def run_ping(hostnames, num_packets):
    raw_results = {}
    agg_results = {}

    for hostname in hostnames:
        process = subprocess.Popen(["ping", "-c", str(num_packets+1), hostname], stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        exitcode = process.returncode # TODO do something with this
        rtts, drop_rate = parse_ping_output(out, num_packets)
        filtered_rtts = [x for x in rtts if x != -1.0]
        raw_results[hostname] = rtts
        agg_results[hostname] = {"drop_rate": drop_rate, "max_rtt": max_rtt, "median_rtt": median_rtt}


def plot_median_rtt_cdf(agg_ping_results_filename):
    with open(agg_ping_results_filename) as file:
    medians = [agg_results[hostname]["median_rtt"] for hostname in agg_results]
    filtered_medians = [x for x in medians if x != -1.0]


def plot_ping_cdf(raw_ping_results_filename):
    with open(raw_ping_results_filename) as file:
    for hostname in raw_results:
        rtts = raw_results[hostname]
        filtered_rtts = [x for x in rtts if x != -1.0]


def parse_ping_output(output, expected_packets=10):
    """
    Returns [rtt1, rtt2, ...], drop_rate
    """
    output = output.strip()
    print output
    rtts = []
    lines = output.split("\n")[1:]
    num_packets_seen = 0
    for line in lines:
        if line == "" or num_packets_seen == expected_packets:
            break
        if "bytes from" in line and "Communication prohibited" not in line:
            rtt = float(line.split(" ")[-2].split("=")[-1])
            rtts.append(rtt)
        else:
            rtts.append(-1.0)
        num_packets_seen += 1

    drop_rate = float(sum(1 for a in rtts if a == -1)) / len(rtts) * 100.0
    return rtts, drop_rate

def main():
    run_ping_from_file("alexa_top_5")

if __name__ == "__main__":
    main()