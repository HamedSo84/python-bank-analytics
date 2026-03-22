import os
#import matplotlib.pyplot as plt
import json

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

        new_transaction = {
            "type": transaction_type,
            "amount": amount,
            "balance": self.balance
        }
        data.append(new_transaction)

        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_transaction(self, transaction, amount):
        if transaction == "deposit":           
            self.balance += amount
            self.save_transactions(amount, transaction)
            return "Deposit successful"

        elif transaction == "withdraw":
            if amount > self.balance:
                return "Error: Insufficient funds!"

            self.balance -= amount
            self.save_transactions(amount, transaction)
            return "Withdraw successful"

        else:
            return "Invalid command"

def show_charts():
    if not os.path.exists():
        return "No transactions found! Please add some first"

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return "File is empty or corrupted"

    deposits = [0]
    withdrawals = [0]
    balance = [0]

    for item in data:
        balance.append(item["balance"])
        if item["type"] == "deposit":
            deposits.append(item["amount"])
        elif item["type"] == "withdraw":
            withdrawals.append(item["amount"])

    x_depo = range(len(deposits))
    x_with = range(len(withdrawals))
    x_balance = range(len(balance))

    plt.figure(1)
    plt.plot(x_depo, deposits, label="Deposits", color="green", marker="o")
    plt.plot(x_with, withdrawals, label="Withdrawals", color="red", marker="o")
    plt.title("Financial Report")
    plt.xlabel("Number of Transactions")
    plt.ylabel("Transaction Amount")
    plt.grid(True)
    plt.legend()

    plt.figure(2)
    plt.plot(x_balance, balance, label="Account_balance", color="blue", marker="o")
    plt.title("Account Balance History")
    plt.xlabel("Number of Transactions")
    plt.ylabel("Transaction Amount")
    plt.grid(True)
    plt.legend()

    plt.show()

if __name__ == "__main__":
    
    my_wallet = BankAccount("Ali")
    
    print(my_wallet.add_transaction("deposit", 1500))
    print(my_wallet.add_transaction("withdraw", 500))
    print(my_wallet.add_transaction("withdraw", 50000))
    
    #my_wallet.show_charts()
