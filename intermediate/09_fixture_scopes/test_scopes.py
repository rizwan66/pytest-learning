# INTERMEDIATE LEVEL — LESSON 9: Fixture Scopes
#
# RUN: pytest intermediate/09_fixture_scopes/ -v -s
#      (-s shows print output so you can observe setup/teardown timing)

import pytest
from conftest import call_log


class TestFunctionScope:
    """function-scoped fixture: fresh for each test method."""

    def test_first(self, function_scoped):
        assert function_scoped == "function"
        # function_setup ran for THIS test

    def test_second(self, function_scoped):
        assert function_scoped == "function"
        # function_setup ran AGAIN — a brand new fixture


class TestModuleScope:
    """module-scoped fixture: created once for the whole file."""

    def test_first(self, module_scoped):
        assert module_scoped == "module"

    def test_second(self, module_scoped):
        # Same fixture instance — module_setup did NOT run again
        assert module_scoped == "module"


class TestSessionScope:
    """session-scoped fixture: created once for the whole test run."""

    def test_a(self, session_scoped):
        assert session_scoped == "session"

    def test_b(self, session_scoped):
        assert session_scoped == "session"


def test_expensive_resource_is_reused(expensive_resource):
    assert "connection" in expensive_resource


def test_expensive_resource_same_object(expensive_resource):
    # session scope: same dict object — no re-creation
    assert expensive_resource["pool_size"] == 5


# --- Mixing scopes: narrower can use wider, not vice versa ---

def test_function_uses_session(function_scoped, session_scoped):
    # A function-scoped fixture can freely use a session-scoped one
    assert function_scoped == "function"
    assert session_scoped == "session"


# --- Observing the call log ---

def test_call_log_shows_scope_behavior():
    # By this point in the run, you can inspect what was called
    # (session and module fixtures appear only once in the log)
    session_setups = call_log.count("session_setup")
    assert session_setups == 1, "session fixture should only set up once"


# EXERCISE:
# 1. Add a class-scoped fixture. Run with -v -s and watch when it sets up/tears down.
# 2. Create a mutable list in a module-scoped fixture. Show how two tests share it.
# 3. Why would you NOT use session scope for a fixture that creates users in a DB?
