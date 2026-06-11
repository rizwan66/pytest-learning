from decimal import Decimal
from datetime import datetime
from typing import Optional


class InsufficientFundsError(Exception):
    pass


class AccountClosedError(Exception):
    pass


class BankAccount:
    def __init__(self, owner: str, initial_balance: Decimal = Decimal("0")):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner = owner
        self._balance = initial_balance
        self._is_open = True
        self._transactions: list[dict] = []

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def is_open(self) -> bool:
        return self._is_open

    def _require_open(self):
        if not self._is_open:
            raise AccountClosedError("Account is closed")

    def deposit(self, amount: Decimal) -> Decimal:
        self._require_open()
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._record("deposit", amount)
        return self._balance

    def withdraw(self, amount: Decimal) -> Decimal:
        self._require_open()
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount}; balance is {self._balance}"
            )
        self._balance -= amount
        self._record("withdraw", amount)
        return self._balance

    def transfer_to(self, other: "BankAccount", amount: Decimal):
        self._require_open()
        other._require_open()
        self.withdraw(amount)
        other.deposit(amount)

    def close(self):
        self._require_open()
        self._is_open = False

    def get_statement(self) -> list[dict]:
        return self._transactions.copy()

    def _record(self, kind: str, amount: Decimal):
        self._transactions.append({
            "type": kind,
            "amount": amount,
            "balance_after": self._balance,
            "timestamp": datetime.now().isoformat(),
        })
