import os
from datetime import datetime

class TransactionLogger:
    def __init__(self, filename="transactions.txt"):
        # Define the target directory (C:\Users\Ahmad\Desktop\VS code\Final Project)
        self.base_dir = r"C:\Users\Ahmad\Desktop\VS code\Final Project"
        self.filename = os.path.join(self.base_dir, filename)
        
        # Create directory if it doesn't exist
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Initialize the file if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write("")  # Create empty file

    def log_transaction(self, username, transaction_type, amount, details=None):
        transaction = {
            "username": username,
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": details or {}
        }
        
        # Format the transaction as a readable string
        transaction_str = (
            f"Username: {transaction['username']}\n"
            f"Type: {transaction['type']}\n"
            f"Amount: {transaction['amount']}\n"
            f"Timestamp: {transaction['timestamp']}\n"
            f"Details: {transaction['details']}\n"
            "----------------------------------\n"
        )
        
        # Append to the text file
        with open(self.filename, 'a') as f:
            f.write(transaction_str)
        
        return transaction

    def get_user_transactions(self, username):
        user_transactions = []
        with open(self.filename, 'r') as f:
            content = f.read()
        
        # Split transactions by the separator
        transactions = content.split("----------------------------------\n")
        
        for tx in transactions:
            if f"Username: {username}" in tx:
                user_transactions.append(tx.strip())
        
    def get_user_transactions(self, username):
        user_transactions = []
        with open(self.filename, 'r') as f:
            content = f.read()
        
        # Split transactions by separator
        transactions = content.split("----------------------------------\n")
        
        for tx in transactions:
            if not tx.strip():  # Skip empty entries
                continue
            
            if f"Username: {username}" in tx:
                # Parse the text back into a dictionary
                tx_dict = {}
                for line in tx.strip().split('\n'):
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        tx_dict[key.lower()] = value
                
                # Convert 'amount' to float (if needed)
                if 'amount' in tx_dict:
                    tx_dict['amount'] = float(tx_dict['amount'])
                
                # Convert 'details' from string to dict (if needed)
                if 'details' in tx_dict:
                    try:
                        tx_dict['details'] = eval(tx_dict['details'])  # WARNING: eval can be unsafe
                    except:
                        tx_dict['details'] = {}
                
                user_transactions.append(tx_dict)
        
        return user_transactions
    def get_all_transactions(self):
        all_transactions = []
        with open(self.filename, 'r') as f:
            content = f.read()
        
        transactions = content.split("----------------------------------\n")
        
        for tx in transactions:
            if not tx.strip():
                continue
            
            tx_dict = {}
            for line in tx.strip().split('\n'):
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    tx_dict[key.lower()] = value
            
            if 'amount' in tx_dict:
                tx_dict['amount'] = float(tx_dict['amount'])
            
            if 'details' in tx_dict:
                try:
                    tx_dict['details'] = eval(tx_dict['details'])
                except:
                    tx_dict['details'] = {}
            
            all_transactions.append(tx_dict)
        
        return all_transactions