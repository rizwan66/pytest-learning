# ADVANCED LEVEL — LESSON 13: pytest Hooks & Plugins
#
# Run with: pytest advanced/13_plugins/ -v
# The terminal summary will show a "slow tests" section if any tests take > 100ms.

import time
import random
import pytest


# --- Test that uses the autouse test_name fixture ---

def test_name_fixture_is_injected(test_name):
    assert test_name == "test_name_fixture_is_injected"


def test_test_name_is_a_string(test_name):
    assert isinstance(test_name, str)
    assert len(test_name) > 0


# --- Smoke tests: will run first (sorted by hook) ---

@pytest.mark.smoke
def test_smoke_basic_assert():
    assert 1 + 1 == 2


@pytest.mark.smoke
def test_smoke_imports():
    import json
    assert json.dumps({"a": 1}) == '{"a": 1}'


# --- Slow tests: will run last (sorted by hook) ---

@pytest.mark.slow
def test_slow_operation():
    time.sleep(0.15)  # > 100ms threshold — appears in slow-tests summary
    assert True


# --- Retry marker ---

@pytest.mark.retry(2)
def test_retry_marker_is_registered():
    # The @retry marker is registered in conftest.pytest_configure.
    # Production retry: use `pytest-rerunfailures` (pip install pytest-rerunfailures)
    # then mark with: @pytest.mark.flaky(reruns=3)
    assert True


# --- Normal tests ---

def test_regular_test_runs_in_middle():
    data = {"key": "value", "number": 42}
    assert data["key"] == "value"
    assert isinstance(data["number"], int)


def test_another_regular_test():
    result = [x ** 2 for x in range(5)]
    assert result == [0, 1, 4, 9, 16]


# --- Observe hook behavior ---

def test_slow_test_reporting():
    # This test itself is fast, but it documents the hook behavior:
    # - Tests taking > 100ms appear in the "slow tests" section
    # - Run `pytest -v` and scroll to the bottom of the output
    assert True


# EXERCISE:
# 1. Add a pytest_runtest_logreport hook that writes failed test names to a file.
# 2. Create a custom marker @pytest.mark.db and a hook that prints a warning
#    when db tests run without a DATABASE_URL env var set.
# 3. Write a conftest fixture that captures all warnings and asserts none were raised.
