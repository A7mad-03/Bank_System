from transaction_logger import TransactionLogger

class SDKBank:
    def __init__(self):
        self.customers = []
        self.passwords = []
        self.balances = []
        self.phone_numbers = []
        self.to_forget_pass = {}  ##### { key: username, || value: {"question":....., "answer": ......}  } #####
        self.transaction_logger = TransactionLogger()  # Replace the dictionary with this



    def create_account(self, username, password, phone, question, answer):
        if username in self.customers:
            return False
        self.customers.append(username)
        self.passwords.append(password)
        self.phone_numbers.append(phone)
        self.balances.append(0.0)
        self.to_forget_pass[username] = {"question": question, "answer": answer.lower()}
        self.transaction_logger.log_transaction(username, "account_creation", 0, {"phone": phone})
        return True



    def login_by_username(self, username, password):
        if username in self.customers:
            index = self.customers.index(username)
            if self.passwords[index] == password:
                return index
        return -1



    def login_by_phone(self, phone, password):
        if phone in self.phone_numbers:
            index = self.phone_numbers.index(phone)
            if self.passwords[index] == password:
                return index
        return -1



    def reset_password(self, username, answer, new_password):
        if username in self.to_forget_pass:
            stored = self.to_forget_pass[username]
            if stored["answer"] == answer.lower():
                index = self.customers.index(username)
                self.passwords[index] = new_password
                return True
        return False



    def deposit(self, index, amount):
        if amount > 0:
            self.balances[index] += amount
            username = self.customers[index]
            self.transaction_logger.log_transaction(username, "deposit", amount)
            return f"✅ Deposit successful. New Balance: {self.balances[index]} JD"
        return "❌ Invalid deposit amount."



    def withdraw(self, index, amount):
        if amount > 0:
            if self.balances[index] >= amount:
                self.balances[index] -= amount
                return f"✅ Withdrawal successful. Remaining Balance: {self.balances[index]} JD"
            return "❌ Insufficient balance."
        return "❌ Invalid withdrawal amount."

    def withdraw(self, index, amount):
        if amount > 0:
            if self.balances[index] >= amount:
                self.balances[index] -= amount
                username = self.customers[index]
                self.transaction_logger.log_transaction(username, "withdrawal", amount)
                return f"✅ Withdrawal successful. Remaining Balance: {self.balances[index]} JD"
            return "❌ Insufficient balance."
        return "❌ Invalid withdrawal amount."
    
    def get_user_transactions(self, index):
        username = self.customers[index]
        return self.transaction_logger.get_user_transactions(username)


    def check_balance(self, index):
        return self.balances[index]