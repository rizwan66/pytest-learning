import time


class PaymentProcessor:
    def __init__(self, gateway="stripe"):
        self.gateway = gateway
        self.transactions = []

    def charge(self, amount: float, currency: str = "USD") -> dict:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if currency not in ("USD", "EUR", "GBP"):
            raise ValueError(f"Unsupported currency: {currency}")
        # Simulate network latency in real gateway
        tx = {
            "id": f"tx_{len(self.transactions) + 1:04d}",
            "amount": amount,
            "currency": currency,
            "status": "success",
            "gateway": self.gateway,
        }
        self.transactions.append(tx)
        return tx

    def refund(self, transaction_id: str) -> dict:
        for tx in self.transactions:
            if tx["id"] == transaction_id:
                return {**tx, "status": "refunded"}
        raise ValueError(f"Transaction {transaction_id!r} not found")

    def slow_reconcile(self) -> int:
        time.sleep(2)  # simulates slow bank API
        return len(self.transactions)
