# ROOT conftest.py
#
# This file is at the project root, so pytest loads it first for every test
# in every subdirectory. Use it for:
#   - Project-wide fixtures (available everywhere without importing)
#   - Global hooks (timing, reporting)
#   - Shared test infrastructure
#
# KEY LESSON: conftest.py files cascade. A fixture defined here is visible
# in beginner/, intermediate/, and advanced/. A fixture in
# intermediate/06_conftest/conftest.py is only visible inside that folder.

import time
import pytest


# --- Global fixture: wall-clock timer for every test ---

@pytest.fixture(autouse=True)
def _record_test_time(request):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    # Attach as a node attribute so hooks and reports can access it
    request.node._elapsed_ms = round(elapsed * 1000, 1)


# --- Global fixture: environment guard ---

@pytest.fixture
def clean_env(monkeypatch):
    """Remove all PYTEST_* env vars so tests start from a clean slate."""
    import os
    for key in list(os.environ):
        if key.startswith("PYTEST_"):
            monkeypatch.delenv(key)


# --- Global hook: warn when a test takes more than 500 ms ---

def pytest_runtest_logreport(report):
    if report.when == "call":
        elapsed = getattr(report, "_elapsed_ms", None) or getattr(
            getattr(report, "node", None), "_elapsed_ms", None
        )
        if elapsed and elapsed > 500:
            print(f"\n  WARNING: {report.nodeid} took {elapsed}ms")
