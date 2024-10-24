import hashlib
import time
import os
import json


# This class represents a single block in the blockchain
class Block:
    def __init__(self, index, proof, previous_hash, data, timestamp=None):
        self.index = index  # The position of the block in the chain
        self.proof = proof  # The number that proves the block's validity
        self.previous_hash = previous_hash  # The hash of the previous block
        self.data = data  # The data stored in the block (like transactions)
        self.timestamp = timestamp or time.time()  # The time the block was created

    # This method calculates the hash of the block's content
    def calculate_hash(self):
        block_string = f"{self.index}{self.proof}{self.previous_hash}{self.data}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    # This makes it easier to display block information
    def __repr__(self):
        return f"Block(Index: {self.index}, Proof: {self.proof}, PrevHash: {self.previous_hash}, Data: {self.data}, Time: {self.timestamp})"


# This class manages the entire blockchain
class Blockchain:
    def __init__(self):
        self.chain = []  # The blockchain (list of blocks)
        self.pending_data = []  # Stores data waiting to be added to the next block
        self.create_genesis_block()  # Automatically create the first block
        self.load_transactions()  # Load existing transactions from file

    # Creates the first block with fixed values (called the "genesis" block)
    def create_genesis_block(self):
        self.create_new_block(proof=0, previous_hash="0")

    # Creates a new block and adds it to the chain
    def create_new_block(self, proof, previous_hash):
        block = Block(
            index=len(self.chain),
            proof=proof,
            previous_hash=previous_hash,
            data=self.pending_data,
        )
        self.pending_data = []  # Clear the pending data once it's added to a block
        self.chain.append(block)  # Add the new block to the chain
        self.save_transactions()  # Save updated transactions to file
        return block

    # Adds new data to the list of pending transactions
    def add_data(self, sender, receiver, amount):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        self.pending_data.append(transaction)
        self.append_transaction_log(transaction)  # Append to the transaction log
        return True

    # This method finds a valid proof number for the block (also called "mining")
    def proof_of_work(self, last_proof):
        proof = 0
        while not self.is_valid_proof(proof, last_proof):
            proof += 1  # Try different proofs until a valid one is found
        return proof

    # This checks if a proof is valid (it requires the hash to start with '0000')
    @staticmethod
    def is_valid_proof(proof, last_proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    # Returns the last block in the chain
    def last_block(self):
        return self.chain[-1]

    # Mines a new block and rewards the miner (sender gets 1 coin)
    def mine_block(self, miner_address, wallet):
        last_block = self.last_block()
        last_proof = last_block.proof
        proof = self.proof_of_work(last_proof)  # Find the proof for the new block

        previous_hash = last_block.calculate_hash()  # Hash of the last block
        new_block = self.create_new_block(proof, previous_hash)

        # Reward the miner after a successful mining
        if miner_address in wallet.wallet_codes.values():
            self.add_data(sender="0", receiver=miner_address, amount=1)  # Reward for mining
            wallet.add_balance(miner_address, 1)  # Add mining reward to miner's wallet
            wallet.save_balances()  # Save updated balances to file
        else:
            print(f"User '{miner_address}' does not have a wallet.")

        return new_block

    # Save all transactions to a file
    def save_transactions(self):
        with open("transactions.json", "w") as file:
            json.dump([block.data for block in self.chain], file)

    # Append a transaction to the transaction log
    def append_transaction_log(self, transaction):
        if os.path.exists("transactions_log.json"):
            with open("transactions_log.json", "r") as file:
                transactions = json.load(file)
        else:
            transactions = []
        transactions.append(transaction)
        with open("transactions_log.json", "w") as file:
            json.dump(transactions, file)

    # Load transactions from a file
    def load_transactions(self):
        if os.path.exists("transactions.json"):
            with open("transactions.json", "r") as file:
                transactions = json.load(file)
                for block_data in transactions:
                    block = Block(
                        index=len(self.chain),
                        proof=0,  # Placeholder value, as proof is not needed for loading past data
                        previous_hash="0",  # Placeholder value
                        data=block_data,
                    )
                    self.chain.append(block)


# This class represents a wallet, which stores users and their balances
class Wallet:
    def __init__(self):
        self.balances = {}  # Dictionary to store user balances
        self.wallet_codes = {}  # Dictionary to store user wallet codes
        self.load_wallet_codes()  # Load existing wallet codes from file
        self.load_balances()  # Load existing balances from file

    # Create a wallet for a new user with an initial balance of 0
    def create_wallet(self, user):
        if user not in self.balances:
            self.balances[user] = 0
            wallet_code = self.generate_wallet_code(user)
            self.wallet_codes[wallet_code] = user
            self.save_wallet_code_to_file(user, wallet_code)
            self.save_wallet_codes()  # Save updated wallet codes to file
            self.save_balances()  # Save updated balances to file
            print(f"Wallet created for '{user}' with wallet code: {wallet_code}")
        else:
            print(f"User '{user}' already has a wallet.")

    # Generate a unique wallet code for the user
    def generate_wallet_code(self, user):
        unique_string = f"{user}{time.time()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    # Save the user's wallet code to a text file
    def save_wallet_code_to_file(self, user, wallet_code):
        with open(f"{user}_wallet.txt", "w") as file:
            file.write(f"Wallet Code: {wallet_code}\n")

    # Save all wallet codes to a file
    def save_wallet_codes(self):
        with open("wallet_codes.json", "w") as file:
            json.dump(self.wallet_codes, file)

    # Load wallet codes from a file
    def load_wallet_codes(self):
        if os.path.exists("wallet_codes.json"):
            with open("wallet_codes.json", "r") as file:
                self.wallet_codes = json.load(file)

    # Save all balances to a file
    def save_balances(self):
        balances_with_codes = {wallet_code: {"user": user, "balance": self.balances[user]} for wallet_code, user in self.wallet_codes.items()}
        with open("balances.json", "w") as file:
            json.dump(balances_with_codes, file)

    # Load balances from a file
    def load_balances(self):
        if os.path.exists("balances.json"):
            with open("balances.json", "r") as file:
                balances_with_codes = json.load(file)
                for wallet_code, data in balances_with_codes.items():
                    user = data["user"]
                    balance = data["balance"]
                    self.wallet_codes[wallet_code] = user
                    self.balances[user] = balance

    # Add coins to a user's wallet
    def add_balance(self, user, amount):
        if user in self.balances:
            self.balances[user] += amount
        else:
            print(f"User '{user}' does not have a wallet.")

    # Deduct coins from a user's wallet
    def deduct_balance(self, user, amount):
        if user in self.balances:
            if self.balances[user] >= amount:
                self.balances[user] -= amount
            else:
                print(f"User '{user}' does not have enough balance to deduct {amount} coins.")
        else:
            print(f"User '{user}' does not have a wallet.")

    # Check if a user has enough coins to make a transaction
    def has_balance(self, user, amount):
        return self.balances.get(user, 0) >= amount

    # Send coins from one user to another
    def send_coins(self, sender, receiver, amount):
        if self.has_balance(sender, amount):
            self.deduct_balance(sender, amount)
            self.add_balance(receiver, amount)
            self.save_balances()  # Save updated balances to file
        else:
            print(f"Transaction failed. {sender} does not have enough balance.")

    # Get the current balance of a user
    def get_balance(self, user):
        return self.balances.get(user, 0)

    # Print all users and their balances
    def print_balances(self):
        print("\nUser Balances:")
        for user, balance in self.balances.items():
            print(f"{user}: {balance}")


# Now we use the blockchain and wallet together
blockchain = Blockchain()
wallet = Wallet()

# Start-up options for user
while True:
    print("\nWelcome to the Blockchain Wallet System")
    print("1. Create a new wallet")
    print("2. Log into existing wallet")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        user = input("Enter a username to create a wallet: ")
        wallet.create_wallet(user)

    elif choice == '2':
        wallet_code = input("Enter your wallet code: ")
        if wallet_code not in wallet.wallet_codes:
            print(f"Invalid wallet code. Please try again.")
            continue

        sender = wallet.wallet_codes[wallet_code]
        print(f"Successfully logged in as: {sender}")

        while True:
            print("\n1. Send coins")
            print("2. Mine a block")
            print("3. View account balance")
            print("4. Log out")
            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                receiver_code = input("Enter the receiver's wallet code: ")
                if receiver_code not in wallet.wallet_codes:
                    print(f"Invalid receiver wallet code. Please try again.")
                    continue

                receiver = wallet.wallet_codes[receiver_code]

                try:
                    amount = float(input("Enter the amount to send: "))
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    continue

                if wallet.has_balance(sender, amount):
                    # Perform the transaction
                    wallet.send_coins(sender=sender, receiver=receiver, amount=amount)
                    blockchain.add_data(sender=sender, receiver=receiver, amount=amount)

                    # Display the updated balances after the transaction
                    wallet.print_balances()

                    # Display the updated blockchain
                    print("*** Updated blockchain after transaction ***")
                    print(blockchain.chain)
                else:
                    print(f"{sender} does not have enough balance to send {amount} coins.")

            elif sub_choice == '2':
                # Mine a block for the user
                blockchain.mine_block(miner_address=sender, wallet=wallet)
                print(f"*** Block mined successfully by {sender} ***")
                print(blockchain.chain)

            elif sub_choice == '3':
                # View account balance
                balance = wallet.get_balance(sender)
                print(f"{sender}'s account balance: {balance} coins")

            elif sub_choice == '4':
                print(f"Logging out {sender}...")
                break

            else:
                print("Invalid choice. Please try again.")

    elif choice == '3':
        print("Exiting... Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
