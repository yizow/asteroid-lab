import json
import subprocess
from subprocess import PIPE

def run_dig(hostname_filename, output_filename, dns_query_server=None):
    with open(hostname_filename) as hostname_file:
        hostnames = hostname_file.read().strip().split("\n")

    dig_results = [] # List of dictionaries corresponding to dig results
    for hostname in hostnames:
        for _ in range(5):
            dig_result = {}
            if dns_query_server:
                process = subprocess.Popen(["dig", hostname, "@" + dns_query_server], stdout=PIPE, stderr=PIPE)
            else:
                process = subprocess.Popen(["dig", "+trace", "+tries=1", "+nofail", hostname], stdout=PIPE, stderr=PIPE)
            out, err = process.communicate()
            print(out)
            success, queries = parse_dig(out)
            dig_result["Name"] = hostname
            dig_result["Success"] = success
            if success:
                dig_result["Queries"] = queries
            dig_results.append(dig_result)

    with open(output_filename, "w") as output_file:
        json.dump(dig_results, output_file)

def get_average_ttls(filename):
    """
    Returns [average TTL of root servers, average TTL of tld servers, average TTL of other nameservers,
        average TTL of terminating CNAME/A entry] in seconds
    """
    with open(filename) as file:
        dig_results = json.load(file)
    all_ttls_by_hostname = {}
    avg_ttls_by_hostname = {}

    for result in dig_results:
        hostname = result["Name"]
        if hostname not in all_ttls_by_hostname:
            all_ttls_by_hostname[hostname] = [[], [], [], []]
        result_ttls = [[], [], [], []] # root, tld, other NS, CNAME/A
        if result["Success"]:
            for query in result["Queries"]:
                for answer in query["Answers"]:
                    ttl = int(answer["TTL"])
                    if answer["Queried name"] == ".": # root servers
                        result_ttls[0].append(ttl)
                    elif answer["Queried name"].count(".") == 1: # tld servers
                        result_ttls[1].append(ttl)
                    elif answer["Type"] == "NS": # other NS servers
                        result_ttls[2].append(ttl)
                    elif answer["Type"] == "A" or answer["Type"] == "CNAME": # A/CNAME entries
                        result_ttls[3].append(ttl)
            for i, entry in enumerate(all_ttls_by_hostname[hostname]):
                entry.extend(result_ttls[i])

    avg_ttls /= len(all_ttls_by_hostname)
    return avg_ttls.tolist()

def _get_all_dig_times(dig_results):
    """
    Helper function that returns a dictionary of hostname -> [total_times, final_times]
    Takes in a list of dig results
    """
    all_times_by_hostname = {} # hostname -> [total_times, final_times]

    for result in dig_results:
        if result["Success"]:
            hostname = result["Name"]
            if hostname not in all_times_by_hostname:
                all_times_by_hostname[hostname] = [[], []]
            total_time, final_time = 0, 0
            for query in result["Queries"]:
                time = query["Time in millis"]
                is_final = False
                for answer in query["Answers"]:
                    if answer["Type"] == "A" or answer["Type"] == "CNAME":
                        is_final = True
                if is_final:
                    final_time = time
                total_time += time

        total_times, final_times = all_times_by_hostname[hostname]
        total_times.append(total_time)
        final_times.append(final_time)

    return all_times_by_hostname

def get_average_times(filename):
    """
    Return [average of total time to resolve a site, average of time to resolve final request]
    calculated across all the iterations of all the websites.
    """
    with open(filename) as file:
        dig_results = json.load(file)
    all_times_by_hostname = _get_all_dig_times(dig_results)
    avg_times_by_hostname = {}

    avg_times /= len(all_times_by_hostname)

    return avg_times.tolist()

def generate_time_cdfs(json_filename, output_filename):
    """
    Plot and save a CDF of the dig lookup times.
    """
    with open(json_filename) as file:
        dig_results = json.load(file)
    all_times_by_hostname = _get_all_dig_times(dig_results)
    total_times, final_times = [], []
    for hostname, times in all_times_by_hostname.iteritems():
        total_times.extend(times[0])
        final_times.extend(times[1])


def count_different_dns_responses(filename1, filename2):
    """
    Count the number of changes that occur between the two sets of dig runs in the two different
    filenames. Return (difference in file1 alone, difference between file1 and file2)
    """
    with open(filename1) as file1:
        dns_responses_1 = json.load(file1)
    with open(filename2) as file2:
        dns_responses_2 = json.load(file2)

    file1_differences = 0
    answers_by_hostname = {} # hostname -> [sets of answers]
    for result in dns_responses_1:
        hostname = result["Name"]
        if hostname not in answers_by_hostname:
            answers_by_hostname[hostname] = []
        if result["Success"]:
            for query in result["Queries"]:
                answer_set = set()
                for answer in query["Answers"]:
                    if answer["Type"] == "A" or answer["Type"] == "CNAME":
                        answer_set.add(answer["Data"])
                if len(answer_set) > 0 and answer_set not in answers_by_hostname[hostname]:
                    print('---------------------------------')
                    print('Found a different set of answers for {} in file1'.format(hostname))
                    print('Old answers:{}\nNew answers: {}'.format(hostname, answer_set))
                    file1_differences += 1 if len(answers_by_hostname[hostname]) > 0 else 0
                    answers_by_hostname[hostname].append(answer_set)
        elif set() not in answers_by_hostname[hostname]: # Count an empty set of answers if dig failed
            answers_by_hostname[hostname].append(set())
            file1_differences += 1

    file1_file2_differences = file1_differences
    for result in dns_responses_2:
        hostname = result["Name"]
        if result["Success"]:
            for query in result["Queries"]:
                answer_set = set()
                for answer in query["Answers"]:
                    if answer["Type"] == "A" or answer["Type"] == "CNAME":
                        answer_set.add(answer["Data"])
                if len(answer_set) > 0 and answer_set not in answers_by_hostname[hostname]:
                    print('---------------------------------')
                    print('Found a different set of answers for {} between file2 and file1'.format(hostname))
                    print('Old answers: {}\nNew answers: {}'.format(answers_by_hostname[hostname], answer_set))
                    file1_file2_differences += 1
                    answers_by_hostname[hostname].append(answer_set)
        elif set() not in answers_by_hostname[hostname]: # Count an empty set of answers if dig failed
            answers_by_hostname[hostname].append(set())
            file1_file2_differences += 1

    return file1_differences, file1_file2_differences

def parse_dig(output):
    """
    Returns success, list of queries where each query is formatted:
    "Time": integer representing the time taken to complete the query
    "Answers": a list of answers for the query. The format of each answer is:
        "Queried name": The name that was queried for (e.g., "." or ".com."). This is the first field in the dig output.
        "Data": result (e.g., for NS records, the name of a DNS server, or for A records, an IP address)
        "Type": type of the answer (e.g., "CNAME" or "A")
        "TTL": Integer representing the TTL of the answer
    """
    success = False
    queries = []

    for query in output.split("\n\n"):
        query_dict = {}
        answers = []
        query_split = query.split("\n")
        for line in query_split:
            words = line.split()
            print(words)
            if len(words) > 0:
                if words[0] == ";;" and "Received" in words:
                    query_dict["Time in millis"] = int(words[-2])
                elif words[0] == ";;" and "Query time" in line: # Output changes without +trace
                    if "ANSWER SECTION" in output:
                        queries[0]["Time in millis"] = int(words[-2])
                    else:
                        query_dict["Time in millis"] = int(words[-2])
                elif not words[0].startswith(";"):
                    queried_name = words[0]
                    ttl = words[1]
                    record_type = words[3]
                    data = words[4]
                    if record_type == "A" or record_type == "CNAME":
                        success = True
                    answers.append({
                        "Queried name": queried_name,
                        "Data": data,
                        "Type": record_type,
                        "TTL": ttl
                    })
        if len(answers) > 0:
            query_dict["Answers"] = answers
        if len(query_dict) > 0:
            queries.append(query_dict)

    return success, queries


def main():
    run_dig("alexa_top_5", "alexa_top_5_output")

if __name__ == "__main__":
    main()