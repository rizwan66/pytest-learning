# ADVANCED LEVEL — LESSON 14: TDD + Coverage
#
# KEY CONCEPTS:
#   - Test-Driven Development: Red → Green → Refactor
#   - Write the test FIRST, watch it fail, then write the minimum code to pass
#   - Coverage: `pytest --cov=bank_account --cov-report=term-missing`
#     shows which lines / branches are NOT exercised
#   - Goal: 100% branch coverage means every code path is tested
#
# RUN:   pytest advanced/14_tdd_coverage/ -v
# COVER: pytest advanced/14_tdd_coverage/ --cov=bank_account --cov-report=term-missing

from decimal import Decimal
import pytest
from bank_account import BankAccount, InsufficientFundsError, AccountClosedError


# --- Fixtures ---

@pytest.fixture
def account():
    return BankAccount(owner="Alice", initial_balance=Decimal("100.00"))


@pytest.fixture
def empty_account():
    return BankAccount(owner="Bob")


@pytest.fixture
def two_accounts():
    a = BankAccount("Alice", Decimal("500"))
    b = BankAccount("Bob",   Decimal("100"))
    return a, b


# ============================================================
# Construction
# ============================================================

def test_account_creation_stores_owner(account):
    assert account.owner == "Alice"


def test_account_creation_stores_balance(account):
    assert account.balance == Decimal("100.00")


def test_account_starts_open(account):
    assert account.is_open is True


def test_account_default_balance_is_zero(empty_account):
    assert empty_account.balance == Decimal("0")


def test_negative_initial_balance_raises():
    with pytest.raises(ValueError, match="cannot be negative"):
        BankAccount("Eve", Decimal("-1"))


# ============================================================
# Deposit
# ============================================================

def test_deposit_increases_balance(account):
    account.deposit(Decimal("50"))
    assert account.balance == Decimal("150.00")


def test_deposit_returns_new_balance(account):
    result = account.deposit(Decimal("25"))
    assert result == Decimal("125.00")


def test_deposit_zero_raises(account):
    with pytest.raises(ValueError, match="must be positive"):
        account.deposit(Decimal("0"))


def test_deposit_negative_raises(account):
    with pytest.raises(ValueError):
        account.deposit(Decimal("-10"))


def test_deposit_records_transaction(account):
    account.deposit(Decimal("50"))
    stmt = account.get_statement()
    assert len(stmt) == 1
    assert stmt[0]["type"] == "deposit"
    assert stmt[0]["amount"] == Decimal("50")


def test_deposit_to_closed_account_raises(account):
    account.close()
    with pytest.raises(AccountClosedError):
        account.deposit(Decimal("10"))


# ============================================================
# Withdraw
# ============================================================

def test_withdraw_decreases_balance(account):
    account.withdraw(Decimal("40"))
    assert account.balance == Decimal("60.00")


def test_withdraw_full_balance(account):
    account.withdraw(Decimal("100"))
    assert account.balance == Decimal("0")


def test_withdraw_returns_new_balance(account):
    result = account.withdraw(Decimal("30"))
    assert result == Decimal("70.00")


def test_withdraw_more_than_balance_raises(account):
    with pytest.raises(InsufficientFundsError):
        account.withdraw(Decimal("200"))


def test_withdraw_zero_raises(account):
    with pytest.raises(ValueError, match="must be positive"):
        account.withdraw(Decimal("0"))


def test_withdraw_from_closed_account_raises(account):
    account.close()
    with pytest.raises(AccountClosedError):
        account.withdraw(Decimal("10"))


def test_withdraw_records_transaction(account):
    account.withdraw(Decimal("30"))
    stmt = account.get_statement()
    assert stmt[0]["type"] == "withdraw"
    assert stmt[0]["balance_after"] == Decimal("70.00")


# ============================================================
# Transfer
# ============================================================

def test_transfer_moves_funds(two_accounts):
    a, b = two_accounts
    a.transfer_to(b, Decimal("200"))
    assert a.balance == Decimal("300")
    assert b.balance == Decimal("300")


def test_transfer_insufficient_funds_raises(two_accounts):
    a, b = two_accounts
    with pytest.raises(InsufficientFundsError):
        b.transfer_to(a, Decimal("999"))


def test_transfer_leaves_sender_unchanged_on_failure(two_accounts):
    a, b = two_accounts
    try:
        b.transfer_to(a, Decimal("999"))
    except InsufficientFundsError:
        pass
    assert b.balance == Decimal("100")  # unchanged


def test_transfer_to_closed_account_raises(two_accounts):
    a, b = two_accounts
    b.close()
    with pytest.raises(AccountClosedError):
        a.transfer_to(b, Decimal("10"))


# ============================================================
# Statement
# ============================================================

def test_statement_is_empty_on_new_account(empty_account):
    assert empty_account.get_statement() == []


def test_statement_records_multiple_operations(account):
    account.deposit(Decimal("50"))
    account.withdraw(Decimal("20"))
    stmt = account.get_statement()
    assert len(stmt) == 2
    assert stmt[0]["type"] == "deposit"
    assert stmt[1]["type"] == "withdraw"


def test_statement_returns_copy_not_reference(account):
    account.deposit(Decimal("10"))
    stmt1 = account.get_statement()
    stmt1.clear()  # mutating the copy
    stmt2 = account.get_statement()
    assert len(stmt2) == 1  # original unchanged


# ============================================================
# Close
# ============================================================

def test_close_marks_account_closed(account):
    account.close()
    assert account.is_open is False


def test_close_already_closed_raises(account):
    account.close()
    with pytest.raises(AccountClosedError):
        account.close()


# EXERCISE:
# 1. Run with --cov — which branches are missing coverage? Fill them.
# 2. Add an `interest(rate)` method (balance * rate added to balance).
#    Write the tests FIRST (TDD), then implement the method.
# 3. Add a test for the transaction timestamp — it should be a valid ISO string.
