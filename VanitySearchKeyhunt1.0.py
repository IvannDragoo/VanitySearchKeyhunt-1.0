import os
import time
import requests
from lxml import html
import re
from bs4 import BeautifulSoup  # BeautifulSoup importieren
from queue import Queue
from threading import Thread

LOGO = """
                         _____ _   _  ___   _   _  ____________  ___  _____ _____ 
                        |_   _| | | |/ _ \ | \ | | |  _  \ ___ \/ _ \|  __ \  _  |
                          | | | | | / /_\ \|  \| | | | | | |_/ / /_\ \ |  \/ | | |
                          | | | | | |  _  || . ` | | | | |    /|  _  | | __| | | |
                         _| |_\ \_/ / | | || |\  | | |/ /| |\ \| | | | |_\ \ \_/ /
                         \___/ \___/\_| |_/\_| \_/ |___/ \_| \_\_| |_/\____/\___/ 

 _    __            _ __        _____                      __    __ __                       __     ___ ____ 
| |  / /___ _____  (_) /___  __/ ___/___  ____ ___________/ /_  / //_/__  __  ____  ______  / /_   <  // __ \

| | / / __ `/ __ \/ / __/ / / /\__ \/ _ \/ __ `/ ___/ ___/ __ \/ ,< / _ \/ / / / / / / __ \/ __/   / // / / /
| |/ / /_/ / / / / / /_/ /_/ /___/ /  __/ /_/ / /  / /__/ / / / /| /  __/ /_/ / /_/ / / / / /_    / // /_/ / 
|___/\__,_/_/ /_/_/\__/\__, //____/\___/\__,_/_/   \___/_/ /_/_/ |_\___/\__, /\__,_/_/ /_/\__/   /_(_)____/  
                      /____/                                           /____/                                


      Give me a Feedback on Github and when you want send a Donate for my work. Thanks and Good Luck
        
                                Github: https://github.com/IvannDragoo
                                Donate (BTC):111"""

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def rotating_loader():
    while True:
        for symbol in "|/-\\":
            yield symbol

def display_results(loader_gen, results_queue):
    # Initiales Drucken des Logos
    print(LOGO)
    print("\nGefundene Ergebnisse:")
    
    while True:
        # Dynamisch die Ergebnisse und das Lade-Symbol anzeigen
        with results_queue.mutex:
            results_list = list(results_queue.queue)

            # Ergebnisse anzeigen
        print("\033[J", end="")  # Gehe eine Zeile nach oben
        for result in results_list:
            print(result)

            # Lade-Symbol anzeigen (wird in der gleichen Zeile aktualisiert)
        print(f"\r[{next(loader_gen)}] Lade...", end="", flush=True)
        time.sleep(0.1)

def check_wallet_provider(addr):
    results = []
    try:
        # Provider 1: Atomic Wallet
        url1 = f"https://bitcoin.atomicwallet.io/address/{addr}"
        response1 = requests.get(url1)
        tree1 = html.fromstring(response1.content)
        balance1 = tree1.xpath('/html/body/main/div/div/div[1]/h4/div/span')
        if balance1:
            balance_value = balance1[0].text_content().strip().replace(' BTC', '')
            results.append((addr, balance_value, "Atomic Wallet"))

        # Provider 2: Blockchain.com
        url2 = f"https://www.blockchain.com/btc/address/{addr}"
        response2 = requests.get(url2)
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        balance2 = soup2.find('span', {'class': 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC'})
        if balance2:
            balance_value = balance2.text.strip().replace(' BTC', '')
            results.append((addr, balance_value, "Blockchain.com"))

        # Provider 3: Blockchair
        url3 = f"https://blockchair.com/bitcoin/address/{addr}"
        response3 = requests.get(url3)
        tree3 = html.fromstring(response3.content)
        balance3 = tree3.xpath('/html/body/main/div/div/div[1]/h4/div/span')
        if balance3:
            balance_value = balance3[0].text_content().strip().replace(' BTC', '')
            results.append((addr, balance_value, "Blockchair"))

    except Exception as e:
        print(f"Fehler bei der Überprüfung von {addr}: {e}")

    return results

def extract_wallet_addresses(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return re.findall(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b', content)
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return []

def save_results(results, output_file):
    with open(output_file, 'a') as f:
        for result in results:
            address, balance, provider = result
            f.write(f"Adresse: {address}, Balance: {balance}, Provider: {provider}\n")

def main():
    file_path = '/home/chiko/Bitcoin/keyhunt/VANITYKEYFOUND.txt'
    output_file = '/home/chiko/Schreibtisch/Found-Balance.txt'
    results_queue = Queue()
    loader_gen = rotating_loader()

    display_thread = Thread(target=display_results, args=(loader_gen, results_queue), daemon=True)
    display_thread.start()

    checked_addresses = set()
    while True:
        addresses = extract_wallet_addresses(file_path)
        for addr in addresses:
            if addr not in checked_addresses:
                checked_addresses.add(addr)
                results = check_wallet_provider(addr)
                if results:
                    for result in results:
                        address, balance, provider = result
                        if float(balance) > 0:  # Fehlerbehebung: Balance ist jetzt ein Float
                            results_queue.put(f"Adresse: {address}, Balance: {balance}, Provider: {provider}")
                            save_results([result], output_file)
        time.sleep(5)

if __name__ == "__main__":
    clear_console()
    main()

