# LucasCoin

Blockchain Wallet System - README

 Overview
This project is a simple Blockchain Wallet System that allows users to create wallets, perform transactions, and mine new blocks to earn coins. The system uses a basic blockchain to store transactions and manages user balances using wallet codes.

Features
- Create a wallet with a unique wallet code.
- Log in using your wallet code.
- Send coins to other users.
- Mine blocks to earn new coins.
- View account balance and transaction history.
- Save user wallet balances and transactions persistently.

How to Use the Blockchain Wallet System


Runing the code 
1. Create a New Wallet
- Enter option `1` to create a new wallet.
- You will be prompted to enter a username.
- A new wallet will be created, and a unique wallet code will be generated.
- The wallet code will be saved in a text file named `<username>_wallet.txt`.

2. Log into an Existing Wallet
- Enter option `2` to log into an existing wallet.
- You will be prompted to enter your wallet code.
- If the wallet code is valid, you will be logged in, and presented with the following options:
  - Send Coins: Transfer coins to another user's wallet using their wallet code. You must have enough coins to complete the transaction.
  - Mine a Block: Mine a new block to earn 1 coin as a reward.
  - View Account Balance: View the balance in your wallet.
  - Log Out: Log out of your account.

3. Exit
- Enter option `3` to exit the program.

Data Persistence
- Wallet Codes: All wallet codes are saved in `wallet_codes.json` to allow users to log in in future sessions.
- Balances: User balances are saved in `balances.json`, which keeps track of each user's balance.
- Transactions: Transactions are logged in `transactions_log.json` for future reference.
- Blockchain: The blockchain with blocks and transactions is saved in `transactions.json`.

 Future Improvements
- Security Enhancements: Add password protection for wallets.
- Network Implementation: Expand the system to work over a network for multiple nodes to participate.
- GUI: Implement a graphical user interface for easier user interaction.

 License
This project is open-source and can be modified and used freely.

 Contact
If you have any questions or issues, feel free to contact me through GitHub.


