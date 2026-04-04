import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates
import json
from datetime import datetime
from enum import Enum
import uuid
from typing import List
from dataclasses import dataclass, asdict, field
import logging


logging.basicConfig(
    filename="bank.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s")

class Transactiontype(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

@dataclass
class Transaction:
    transaction_id: str
    type: str
    amount: float
    balance: float
    timestamp: datetime = field(default_factory=datetime.now)

    @staticmethod
    def from_dict(d):
        return Transaction(
            transaction_id=d.get('transaction_id', str(uuid.uuid4())),
            type=d['type'],
            amount=d['amount'],
            balance=d['balance'],
            timestamp=datetime.fromisoformat(d['timestamp']),
        )

    def to_dict(self):
        d = asdict(self)
        d['timestamp'] = self.timestamp.isoformat()
        return d

class BankAccount:
    def __init__(self, owner: str, storage_file="_transactions.json"):
        self.owner = owner
        self._balance = 0.0
        self.transactions: List[Transaction] = []
        self.storage_file = f"{self.owner}{storage_file}"
        self.load_transactions()

    @property
    def balance(self):
        return self._balance

    def save_transactions(self):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.transactions], f, ensure_ascii=False, indent=4)

    def load_transactions(self):
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.transactions = [Transaction.from_dict(tr) for tr in data]
            if self.transactions:
                self._balance = self.transactions[-1].balance
            else:
                self._balance = 0.0
        except (FileNotFoundError, json.JSONDecodeError):
            self.transactions = []
            self._balance = 0.0

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive!")
        self._balance += amount
        t = Transaction(
            transaction_id=str(uuid.uuid4()),
            type=Transactiontype.DEPOSIT.value,
            amount=amount,
            balance=self._balance,
            timestamp=datetime.now()
        )
        self.transactions.append(t)
        self.save_transactions()
        logging.info(f"Deposit | amount={amount} | balance={self._balance}")
        return t

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive!")
        if amount > self._balance:
            raise ValueError("Insufficient balance!")
        self._balance -= amount
        t = Transaction(
            transaction_id=str(uuid.uuid4()),
            type=Transactiontype.WITHDRAW.value,
            amount=amount,
            balance=self._balance,
            timestamp=datetime.now()
        )
        self.transactions.append(t)
        self.save_transactions()
        logging.info(f"Withdraw | amount={amount} | balance={self._balance}")
        return t

class AccountAnalytics:
    def __init__(self, transactions):
        self.transactions = transactions

    def show_charts(self):
        if not self.transactions:
            return "No transactions to show."

        days = [t.timestamp for t in self.transactions]
        deposits = [t.amount if t.type == Transactiontype.DEPOSIT.value else 0 for t in self.transactions]
        withdrawals = [t.amount if t.type == Transactiontype.WITHDRAW.value else 0 for t in self.transactions]
        balances = [t.balance for t in self.transactions]

        plt.figure(1)
        plt.bar(days, deposits, label="Deposits", color='green', alpha=0.7)
        plt.bar(days, withdrawals, label="Withdrawals", color='red', alpha=0.7, bottom=deposits)
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Deposits and Withdrawals Over Time')
        plt.legend()

        plt.figure(2)
        plt.plot(days, balances, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Balance')
        plt.title('Account Balance History')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.grid(True)

        plt.show()
        
if __name__ == "__main__":
    acc = BankAccount("Ali")
    acc.deposit(2000)
    acc.withdraw(500)
    print("Current balance:", acc.balance)
    analytics = AccountAnalytics(acc.transactions)
    analytics.show_charts()
