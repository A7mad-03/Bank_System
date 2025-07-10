class Click:
    def __init__(self, bank):
        self.bank = bank  

    def transfer(self, index, phone_number, amount):
        if phone_number not in self.bank.phone_numbers:
            return "❌ Phone number not found."

        if amount <= 0:
            return "❌ Invalid amount."

        if amount > self.bank.balances[index]:
            return "❌ Insufficient balance."

        receiver_index = self.bank.phone_numbers.index(phone_number)
        sender = self.bank.customers[index]
        receiver = self.bank.customers[receiver_index]
        
        # Perform the transfer
        self.bank.balances[index] -= amount
        self.bank.balances[receiver_index] += amount
        
        # Log transaction for sender
        self.bank.transaction_logger.log_transaction(
            username=sender,
            transaction_type="transfer_out",
            amount=amount,
            details={
                "recipient": receiver,
                "recipient_phone": phone_number,
                "direction": "outgoing"
            }
        )
        
        # Log transaction for receiver
        self.bank.transaction_logger.log_transaction(
            username=receiver,
            transaction_type="transfer_in",
            amount=amount,
            details={
                "sender": sender,
                "sender_phone": self.bank.phone_numbers[index],
                "direction": "incoming"
            }
        )
        
        return f"✅ Transfer of {amount}JD to Mr.{receiver.capitalize()} is completed"