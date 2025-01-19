                         _____ _   _  ___   _   _  ____________  ___  _____ _____ 
                        |_   _| | | |/ _ \ | \ | | |  _  \ ___ \/ _ \|  __ \  _  |
                          | | | | | / /_\ \|  \| | | | | | |_/ / /_\ \ |  \/ | | |
                          | | | | | |  _  || . ` | | | | |    /|  _  | | __| | | |
                         _| |_\ \_/ / | | || |\  | | |/ /| |\ \| | | | |_\ \ \_/ /
                         \___/ \___/\_| |_/\_| \_/ |___/ \_| \_\_| |_/\____/\___/

      Give me a Feedback on Github and when you want send a Donate for my work. Thanks and Good Luck
        
                                Github: https://github.com/IvannDragoo
                                Donate (BTC):3EkQMZpLCyFHD9BD2jSH9jpwBsTmKbCpne


This script uses Keyhunt to search for vanity addresses and checks the found addresses for transactions and balances. The found data is saved into different files depending on whether a balance was found or not.
Installation
1. Download and Install Keyhunt

First, you need to download and install Keyhunt. Follow these steps:

    Go to the Keyhunt GitHub repository.

    Click on "Code" and download the repository as a ZIP file, or clone it directly:

git clone https://github.com/albertobsd/keyhunt.git

Navigate to the downloaded directory:

cd keyhunt

Install all the required dependencies (if not done already):

    pip install -r requirements.txt

2. Add VanitySearchKeyhunt 1.0

    Download the VanitySearchKeyhunt1.0.py script.
    Copy the script into the Keyhunt directory, where the keyhunt.py file is located.

3. Install Dependencies

    Open a console/terminal in the Keyhunt folder and install the necessary modules for the script:

    pip install -r requirements.txt

4. Run the Script

Now, you can run the script:

python VanitySearchKeyhunt1.0.py

How It Works

    VanitySearchKeyhunt1.0.py uses Keyhunt to search for vanity addresses.
    When Keyhunt finds an address, it is saved to the VANITYFOUNDKEY.txt file.
    The script reads the VANITYFOUNDKEY.txt, checks each found address for:
        Transactions
        Balance
    If an address has a balance, it is written to the Found-Balance.txt file.
    If only transactions are found (but no balance), the address is written to the Found.Trx.txt file.
    The checking and saving process runs continuously.

Files

    VANITYFOUNDKEY.txt: Contains all the vanity addresses found by Keyhunt.
    Found-Balance.txt: Contains addresses with a positive balance.
    Found.Trx.txt: Contains addresses that have transactions but no balance.

Example Workflow:

    Keyhunt finds a vanity address and saves it to the VANITYFOUNDKEY.txt file.
    The script reads this file and checks the address for:
        If a balance is found, the address is saved to Found-Balance.txt.
        If only transactions are found, the address is saved to Found.Trx.txt.

Requirements

    Python 3.x
    The modules listed in requirements.txt

Example requirements.txt (optional):

You can create a requirements.txt file for the necessary dependencies. Here’s an example:

requests
web3

Notes:

    Keyhunt needs to be properly configured to generate vanity addresses. For more details on configuring Keyhunt, check the Keyhunt documentation.
    Make sure you have the necessary permissions to write files in the Keyhunt folder.

By following these instructions, you should be able to use the script to check the addresses Keyhunt finds and save the data accordingly.

Donate (BTC): 3EkQMZpLCyFHD9BD2jSH9jpwBsTmKbCpne
