#!/usr/bin/env python3
import argparse
import subprocess
import shlex
import yaml

CONFIG_FILE = "config.yaml"

def read_file(filename):
    data = None
    with open(filename, "r") as fd:
        data = fd.read()

    return data

def main():
    print("Starting experiment")
    parser = argparse.ArgumentParser(description="Start a jailed experiment container.")
    parser.add_argument("image_name", help="Name of image to start")
    args = parser.parse_args()

    image_name = args.image_name
    print("Image name: {}".format(image_name))

    config_data = read_file(CONFIG_FILE)
    config_yaml = yaml.load(config_data)

    # client = docker.from_env()
    # client.containers.run(image_name, "hello")

    cmd = "docker run"
    if "cpus" in config_yaml:
        cmd += " --cpus=" + str(config_yaml["cpus"])
    if "cpuset-cpus" in config_yaml:
        cmd += " --cpuset-cpus=" + str(config_yaml["cpuset-cpus"])
    if "memory" in config_yaml:
        cmd += " --memory=" + str(config_yaml["memory"])
    
    subprocess.call(shlex.split("docker run " + image_name))

if __name__ == "__main__":
    main()
