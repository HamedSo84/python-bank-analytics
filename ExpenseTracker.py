import os
import matplotlib.pyplot as plt
import json
import datetime
from enum import Enum

class Transactiontype(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

class Transaction:
    def __init__(self, t_type, amount, balance):
        self.type = t_type
        self.amount = amount
        self.balance = balance
        self.time = datetime.datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "type": self.type,
            "amount": self.amount,
            "balance": self.balance,
            "time": self.time
        }

class BankAccount:
    def __init__(self, account_name):
        self.name = account_name
        self.file_name = f"{account_name}_money.json"
        self.balance = self.load_last_balance()

    def load_last_balance(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    if len(data) > 0:
                        return data[-1]["balance"]
                except json.JSONDecodeError:
                    return 0
        return 0

    def save_transactions(self, amount, transaction_type):
        data = []
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as file:
                    data = json.load(file)

            except (json.JSONDecodeError, FileNotFoundError):
                data = []
        t = Transaction(transaction_type, amount, self.balance)
        data.append(t.to_dict())

        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_transaction(self, transaction: Transactiontype, amount):
        if transaction == Transactiontype.DEPOSIT:           
            self.balance += amount
            self.save_transactions(amount, transaction)
            return "Deposit successful"

        elif transaction == Transactiontype.WITHDRAW:
            if amount > self.balance:
                return "Error: Insufficient funds!"

            self.balance -= amount
            self.save_transactions(amount, transaction)
            return "Withdraw successful"

        else:
            return "Invalid command"

    def show_charts(self):
        if not os.path.exists(self.file_name):
            return "No transactions found! Please add some first"

        with open(self.file_name, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return "File is empty or corrupted"

        deposits = []
        withdrawals = []
        balance = []
        days = []

        for item in data:
            days.append(int(item["time"].split("-")[2]))
            balance.append(item["balance"])
            if item["type"] == "deposit":
                deposits.append(item["amount"])
                withdrawals.append(0) 
            elif item["type"] == "withdraw":
                withdrawals.append(item["amount"])
                deposits.append(0) 
        x_transactions = range(len(deposits))

        plt.figure(1)
        plt.plot(x_transactions, deposits, label="Deposits", color="green", marker="o")
        plt.plot(x_transactions, withdrawals, label="Withdrawals", color="red", marker="o")
        plt.title(f"Financial Report - {self.name}")
        plt.xlabel("Number of Transactions")
        plt.ylabel("Transaction Amount")
        plt.grid(True)
        plt.legend()

        plt.figure(2)
        plt.plot(days, balance, label="Account_balance", color="blue", marker="o")
        plt.title(f"Account Balance History - {self.name}")
        plt.xlabel("Day of Month")
        plt.ylabel("Transaction Amount")
        plt.grid(True)
        plt.legend()

        plt.figure(3)
        total_depo = sum(deposits)
        total_with = sum(withdrawals)
        categories = ['Total Deposits', 'Total Withdrawals']
        values = [total_depo, total_with]
            
        plt.bar(categories, values, color=['green', 'red'], label="Total Amount")
            
        plt.title(f"Total Analysis (Bar Chart) - {self.name}")
        plt.xlabel("Transaction Category")
        plt.ylabel("Amount")
        plt.grid(axis='y', linestyle='--', alpha=0.7) 
        plt.legend()

        plt.show()
        
if __name__ == "__main__":
    
    my_wallet = BankAccount("Ali")
    
    print(my_wallet.add_transaction("deposit", 1500))
    print(my_wallet.add_transaction("withdraw", 500))
    print(my_wallet.add_transaction("withdraw", 50000))
    print(my_wallet.balance)
    my_wallet.show_charts()
