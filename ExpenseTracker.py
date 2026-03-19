import os
#import matplotlib.pyplot as plt
import json
FILE_NAME = "money.json"

def load_last_balance():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if len(data) > 0:
                    return data[-1]["balance"]
            except json.JSONDecodeError:
                return 0
    return 0

Account_balance = load_last_balance()

def save_transactions(amount, balance, transaction_type):
    data = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = [] 
    new_transaction = {
        "type": transaction_type,
        "amount": amount,
        "balance": balance
    }
    data.append(new_transaction)

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def add_transaction():
    while True:
        global Account_balance
        Value = input("Would you like to withdraw or deposit or back? w/d/b: ")
        if Value == "d":
            deposit = float(input("Enter the deposit amount: "))
            Account_balance += deposit
            balance = deposit
            transaction = "deposit"
            save_transactions(balance, Account_balance, transaction)

        elif Value == "w":
            withdraw = float(input("Enter the withdraw amount:"))
            Account_balance -= withdraw
            balance = withdraw
            transaction = "withdraw"
            save_transactions(balance, Account_balance, transaction)

        elif Value == "b":
            break
            
        else:
            print("Invalid command")

def show_charts():
    if not os.path.exists(FILE_NAME):
        print("No transactions found! Please add some first")
        return

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print("File is empty or corrupted")
            return
    deposits = []
    withdrawals = []

    for item in data:
        print(item)
        if item["type"] == "deposit":
            deposits.append(item["amount"])
        elif item["type"] == "withdraw":
            withdrawals.append(item["amount"])

    print(deposits)



def menu():
    while True:
        value = input("add_transaction or Check Balance or show_transactions or exit? a/ch/sh/e: ").lower()
        if value == "a":
            add_transaction()
        elif value == "ch":
            print(Account_balance)
        elif value == "sh":
            show_charts()
        elif value == "e":
            break
        else:
            print("Invalid command")

menu()