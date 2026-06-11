# INTERMEDIATE LEVEL — LESSON 9: Fixture Scopes
#
# Scope controls HOW OFTEN a fixture is created and destroyed:
#
#   function (default) — new instance per test function
#   class              — shared within a test class
#   module             — shared across all tests in a .py file
#   session            — shared across the entire test run
#
# Use wider scopes for expensive setup (DB connection, server start).
# Never use wide scopes for mutable state — tests will bleed into each other.

import pytest


call_log = []  # global log to track fixture invocations across tests


@pytest.fixture(scope="function")
def function_scoped():
    call_log.append("function_setup")
    yield "function"
    call_log.append("function_teardown")


@pytest.fixture(scope="module")
def module_scoped():
    call_log.append("module_setup")
    yield "module"
    call_log.append("module_teardown")


@pytest.fixture(scope="session")
def session_scoped():
    call_log.append("session_setup")
    yield "session"
    call_log.append("session_teardown")


@pytest.fixture(scope="session")
def expensive_resource():
    """Simulates an expensive one-time resource (e.g., DB server, test container)."""
    call_log.append("expensive_resource_created")
    resource = {"connection": "db://localhost/testdb", "pool_size": 5}
    yield resource
    call_log.append("expensive_resource_destroyed")
