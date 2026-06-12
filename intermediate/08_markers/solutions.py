# SOLUTIONS — Lesson 08: Markers

import pytest
from payment import PaymentProcessor


@pytest.fixture
def proc():
    return PaymentProcessor()


@pytest.mark.smoke
def test_smoke_charge_succeeds(proc):
    tx = proc.charge(1.0)
    assert tx["status"] == "success"


@pytest.mark.smoke
def test_smoke_gateway_is_stripe(proc):
    assert proc.gateway == "stripe"


@pytest.mark.unit
def test_charge_multi_currency_eur(proc):
    tx = proc.charge(50.0, currency="EUR")
    assert tx["currency"] == "EUR"


@pytest.mark.unit
def test_charge_multi_currency_gbp(proc):
    tx = proc.charge(25.0, currency="GBP")
    assert tx["currency"] == "GBP"
