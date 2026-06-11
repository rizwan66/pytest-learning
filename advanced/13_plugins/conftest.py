# ADVANCED LEVEL — LESSON 13: pytest Hooks & Plugins
#
# conftest.py acts as a local plugin — hook implementations here are
# auto-registered by pytest without any setup.py or pyproject.toml.
#
# Common hooks:
#   pytest_configure      — runs at startup, register markers / configure
#   pytest_runtest_setup  — runs before each test
#   pytest_runtest_call   — wraps the test call itself
#   pytest_runtest_makereport — access pass/fail result
#   pytest_collection_modifyitems — filter / sort collected tests
#   pytest_terminal_summary — append to the final summary output

import time
import pytest


# --- Track slow tests ---

_slow_tests = []  # populated by the hook below


def pytest_runtest_makereport(item, call):
    """Hook: fires after each test phase (setup / call / teardown)."""
    if call.when == "call":
        duration = call.stop - call.start
        if duration > 0.1:
            _slow_tests.append((item.nodeid, round(duration, 3)))


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Hook: appends a custom section to the terminal summary."""
    if _slow_tests:
        terminalreporter.write_sep("=", "slow tests (> 100ms)")
        for nodeid, duration in sorted(_slow_tests, key=lambda x: -x[1]):
            terminalreporter.write_line(f"  {duration:.3f}s  {nodeid}")


# --- Custom marker: retry flaky tests ---

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "retry(n): retry the test up to n times on failure"
    )
    # NOTE: implementing retry properly requires pytest-rerunfailures plugin.
    # Doing it via a raw hook is error-prone; use the plugin for production code.


# --- Sort tests: run smoke tests first ---

def pytest_collection_modifyitems(items, config):
    """Sort collected tests: smoke marker runs first, slow runs last."""
    smoke = [i for i in items if i.get_closest_marker("smoke")]
    slow  = [i for i in items if i.get_closest_marker("slow")]
    rest  = [i for i in items if i not in smoke and i not in slow]
    items[:] = smoke + rest + slow


# --- Fixture: inject test name into every test ---

@pytest.fixture(autouse=True)
def test_name(request):
    """Available in every test via `test_name` parameter."""
    return request.node.name
