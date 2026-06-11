# INTERMEDIATE LEVEL — LESSON 8: Markers
#
# KEY CONCEPTS:
#   - @pytest.mark.X tags tests for filtering with -m
#   - Built-in markers: skip, skipif, xfail, parametrize
#   - Custom markers: register them in pytest.ini [markers] section
#   - Run subsets:  pytest -m unit   or   pytest -m "not slow"
#
# RUN: pytest intermediate/08_markers/ -v
# RUN only unit tests: pytest intermediate/08_markers/ -m unit
# SKIP slow: pytest intermediate/08_markers/ -m "not slow"

import sys
import pytest
from payment import PaymentProcessor


@pytest.fixture
def processor():
    return PaymentProcessor()


# --- Custom markers ---

@pytest.mark.unit
def test_charge_returns_transaction_id(processor):
    tx = processor.charge(100.0)
    assert "id" in tx
    assert tx["id"].startswith("tx_")


@pytest.mark.unit
def test_charge_amount_stored_correctly(processor):
    tx = processor.charge(49.99)
    assert tx["amount"] == 49.99


@pytest.mark.unit
def test_charge_default_currency_is_usd(processor):
    tx = processor.charge(10.0)
    assert tx["currency"] == "USD"


@pytest.mark.unit
def test_charge_negative_amount_raises(processor):
    with pytest.raises(ValueError, match="Amount must be positive"):
        processor.charge(-10.0)


@pytest.mark.unit
def test_charge_unsupported_currency_raises(processor):
    with pytest.raises(ValueError, match="Unsupported currency"):
        processor.charge(10.0, currency="BTC")


@pytest.mark.integration
def test_charge_then_refund(processor):
    tx = processor.charge(200.0)
    refund = processor.refund(tx["id"])
    assert refund["status"] == "refunded"
    assert refund["amount"] == 200.0


@pytest.mark.integration
def test_refund_unknown_transaction_raises(processor):
    with pytest.raises(ValueError, match="not found"):
        processor.refund("tx_9999")


@pytest.mark.slow
def test_reconciliation_slow(processor):
    processor.charge(10.0)
    processor.charge(20.0)
    count = processor.slow_reconcile()
    assert count == 2


# --- Built-in skip markers ---

@pytest.mark.skip(reason="Gateway not configured in CI")
def test_live_gateway_charge(processor):
    # This test would call a real payment API
    tx = processor.charge(1.0)
    assert tx["status"] == "success"


@pytest.mark.skipif(sys.platform == "win32", reason="Windows payment SDK not supported")
def test_charge_on_non_windows(processor):
    tx = processor.charge(5.0)
    assert tx["gateway"] == "stripe"


# --- xfail: expected failures ---

@pytest.mark.xfail(reason="Refund on already-refunded tx not yet implemented")
def test_double_refund_raises(processor):
    tx = processor.charge(50.0)
    processor.refund(tx["id"])
    processor.refund(tx["id"])   # should raise — but doesn't yet


@pytest.mark.xfail(strict=False, reason="GBP sometimes fails in legacy gateway")
def test_gbp_charge_may_fail():
    p = PaymentProcessor()
    # strict=False (default): XPASS is allowed — test just shows as "xpassed"
    # Use strict=True when you want to enforce that a known bug is NOT fixed yet
    p.charge(10.0, currency="GBP")


# EXERCISE:
# 1. Run `pytest -m unit -v` — only unit tests should run.
# 2. Run `pytest -m "unit or integration" -v` — combined selection.
# 3. Add a @pytest.mark.smoke marker and two smoke tests.
