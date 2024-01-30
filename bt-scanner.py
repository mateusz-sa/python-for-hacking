# Import bluetooth from the PyBluez module.
import bluetooth
from colorama import Fore, Back, Style
from termcolor import colored

def scan_bluetooth_devices():
    try:
        # Discover Bluetooth devices with names and classes.
        discovered_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
        # Display information about the scanning process.
        print('\n[!] Scanning for active devices...')
        print(f"[!] Found {len(discovered_devices)} Devices\n")
        # Iterate through discovered devices and print their details.

        for addr, name, device_class in discovered_devices:
            print(colored(f'[+] Name: {name}','green'))
            print(colored(f'[+] Address: {addr}','green'))
            print(colored(f'[+] Device Class: {device_class}\n','green'))
    except Exception as e:
        # Handle and display any exceptions that occur during device discovery
        print(colored(f"[ERROR] An error occurred: {e}","red"))

# Call the Bluetooth device scanning function when the script is run
scan_bluetooth_devices()