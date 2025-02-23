import re
import os
import traceback
import requests
import concurrent.futures
from lxml import html
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import sys
import pygame  # Import pygame for audio

# Initialize pygame mixer for sound
pygame.mixer.init()

# Debugging: Print to check initialization
print("Pygame initialized:", pygame.mixer.get_init())

# Check the current working directory to ensure it's correct
print("Current working directory:", os.getcwd())

# Define the path to the beep sound
beep_sound_path = os.path.join(os.getcwd(), "beep.wav")

# Check if the beep sound file exists in the directory
if os.path.exists(beep_sound_path):
    beep_sound = pygame.mixer.Sound(beep_sound_path)
    print("Beep sound loaded successfully.")
else:
    print("Error: beep.wav not found in the current directory.")

# Function to play beep sound
def play_beep():
    if 'beep_sound' in globals():  # Check if beep_sound is loaded
        beep_sound.play()
        print("Beep sound played.")
    else:
        print("Beep sound is not loaded properly.")

LOGO = """
                         _____ _   _  ___   _   _  ____________  ___  _____ _____ 
                        |_   _| | | |/ _ \ | \ | | |  _  \ ___ \/ _ \|  __ \  _  |
                          | | | | | / /_\ \|  \| | | | | | |_/ / /_\ \ |  \/ | | |
                          | | | | | |  _  || . ` | | | | |    /|  _  | | __| | | |
                         _| |_\ \_/ / | | || |\  | | |/ /| |\ \| | | | |_\ \ \_/ /
                         \___/ \___/\_| |_/\_| \_/ |___/ \_| \_\_| |_/\____/\___/ 

     _   __          _ __       ____                 __   __ __         __             __    ___ ___ 
    | | / /__ ____  (_) /___ __/ __/__ ___ _________/ /  / //_/__ __ __/ /  __ _____  / /_  <  // _ \
    | |/ / _ `/ _ \/ / __/ // /\ \/ -_) _ `/ __/ __/ _ \/ ,< / -_) // / _ \/ // / _ \/ __/  / // // /
    |___/\_,_/_//_/_/\__/\_, /___/\__/\_,_/_/  \__/_//_/_/|_|\__/\_, /_//_/\_,_/_//_/\__/  /_(_)___/ 
                        /___/                                   /___/                                

      Give me a Feedback on Github and when you want send a Donate for my work. Thanks and Good Luck
        
                                Github: https://github.com/IvannDragoo
                                Donate (BTC):3EkQMZpLCyFHD9BD2jSH9jpwBsTmKbCpne
"""

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_console()
print(LOGO)

# Initialize status line
sys.stdout.write("Waiting, the program is searching for balances or transactions...\n")
sys.stdout.flush()

def get_wallet_info_atomic(addr, checked_addresses):
    if addr in checked_addresses:
        return "Error", "Error", "Error", addr, "atomic"
    
    checked_addresses.add(addr)

    try:
        urlblock = f"https://bitcoin.atomicwallet.io/address/{addr}"
        response_block = requests.get(urlblock)
        byte_string = response_block.content
        source_code = html.fromstring(byte_string)

        xpatch_balance = '/html/body/main/div/div/div[1]/h4/div/span'
        xpatch_trx = '/html/body/main/div/table/tbody/tr[5]/td[2]'
        xpatch_days = '/html/body/main/div/div[3]/div[1]/div[1]/div[2]/span/span'

        balance_elements = source_code.xpath(xpatch_balance)
        trx_elements = source_code.xpath(xpatch_trx)
        days_elements = source_code.xpath(xpatch_days)

        balance = balance_elements[0].text_content().strip() if balance_elements else "Not found"
        trx = trx_elements[0].text_content().strip() if trx_elements else "Not found"
        days = days_elements[0].text_content().strip() if days_elements else "No information"

        return balance, trx, days, addr, "atomic"

    except Exception:
        return "Error", "Error", "Error", addr, "atomic"


def get_wallet_info_blockchain(addr, checked_addresses):
    if addr in checked_addresses:
        return "Error", "Error", "Error", addr, "blockchain.com"
    
    checked_addresses.add(addr)

    try:
        urlblock = f"https://blockchain.info/balance?active={addr}"
        response_block = requests.get(urlblock)
        data = response_block.json()
        balance = data[addr]['final_balance'] / 1e8
        trx = data[addr]['n_tx']
        return str(balance), str(trx), "No information", addr, "blockchain.com"

    except Exception:
        return "Error", "Error", "Error", addr, "blockchain.com"


def get_wallet_info_with_timeout(addr, checked_addresses, provider_index):
    providers = [get_wallet_info_atomic, get_wallet_info_blockchain]
    provider = providers[provider_index % len(providers)]
    timeout = 5
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Print the address being tested
        sys.stdout.write(f"\rTesting address: {addr} ")
        sys.stdout.flush()

        balance, trx, days, address, provider_name = provider(addr, checked_addresses)
        if balance != "Not found" and trx != "Not found" and balance != "Error" and trx != "Error":
            return balance, trx, days, address, provider_name

    return "Error", "Error", "Error", addr, "unknown"


def extract_addresses_from_file(file_path):
    try:
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            content = f.read()
        addresses = re.findall(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b', content)
        return addresses
    except Exception:
        return []


def process_wallets_from_file(file_path):
    addresses = extract_addresses_from_file(file_path)
    if not addresses:
        return

    checked_addresses = set()
    provider_index = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for addr in addresses:
            futures.append(
                executor.submit(get_wallet_info_with_timeout, addr, checked_addresses, provider_index)
            )
            provider_index += 1

        for future in concurrent.futures.as_completed(futures):
            balance, trx, days, address, provider = future.result()

            try:
                balance_value = float(balance)
            except ValueError:
                balance_value = 0

            # If balance > 0, immediately write to the file and play the beep sound
            if balance_value > 0:
                with open('Found-Balance.txt', 'a') as balance_file:
                    balance_file.write(f"Provider: {provider}\nBitcoin Address: {address}\nBalance: {balance}\n\n")
                    balance_file.flush()
                play_beep()  # Play the beep sound when found
                sys.stdout.write(f"\rFound! Provider: {provider} | Address: {address} | Balance: {balance} BTC\n")
                sys.stdout.flush()

            # If transactions > 0, immediately write to the file
            if trx.isdigit() and int(trx) > 0:
                with open('Found-Trx.txt', 'a') as trx_file:
                    trx_file.write(f"Provider: {provider}\nBitcoin Address: {address}\nTransactions: {trx}\nLast Transaction Days: {days}\n\n")
                    trx_file.flush()
                play_beep()  # Play the beep sound when found
                sys.stdout.write(f"\rFound! Provider: {provider} | Address: {address} | Transactions: {trx}\n")
                sys.stdout.flush()


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            process_wallets_from_file(self.file_path)


def start_file_watcher(file_path):
    event_handler = FileEventHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def initial_test_and_wait(file_path):
    # Test the existing addresses if there are any
    process_wallets_from_file(file_path)
    
    # After processing the initial addresses, wait for new entries
    start_file_watcher(file_path)


if __name__ == "__main__":
    file_path = '/path/to/keyhunt/VANITYKEYFOUND.txt'
    initial_test_and_wait(file_path)
