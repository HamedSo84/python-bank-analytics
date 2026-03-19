import os
import matplotlib.pyplot as plt
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

def add_transaction(transaction, amount):
    global Account_balance
    if transaction == "deposit":           
        Account_balance += amount
        save_transactions(amount, Account_balance, transaction)
        return "Deposit successful"

    elif transaction == "withdraw":
        if amount > Account_balance:
            return "Error: Insufficient funds!"

        Account_balance -= amount
        save_transactions(amount, Account_balance, transaction)
        return "Withdraw successful"

    else:
        return "Invalid command"

def show_charts():
    if not os.path.exists(FILE_NAME):
        return "No transactions found! Please add some first"

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return "File is empty or corrupted"

    deposits = [0]
    withdrawals = [0]

    for item in data:
        if item["type"] == "deposit":
            deposits.append(item["amount"])
        elif item["type"] == "withdraw":
            withdrawals.append(item["amount"])

    x_depo = range(len(deposits))
    x_with = range(len(withdrawals))

    plt.plot(x_depo, deposits, label="Deposits", color="green", marker="o")
    plt.plot(x_with, withdrawals, label="Withdrawals", color="red", marker="o")
    plt.title("Financial Report")
    plt.xlabel("Number of Transactions")
    plt.ylabel("Transaction Amount")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    
    testValiddeposit= add_transaction("deposit", 1500)
    print(testValiddeposit)
    
    testValidwithdraw = add_transaction("withdraw", 500)
    print(testValidwithdraw)
    
    testInvalidwithdraw = add_transaction("withdraw", 50000)
    print(testInvalidwithdraw)
    
    show_charts()
