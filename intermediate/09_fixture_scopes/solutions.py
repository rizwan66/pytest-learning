# SOLUTIONS — Lesson 09: Fixture Scopes

import pytest
from conftest import call_log


@pytest.fixture(scope="class")
def class_scoped():
    call_log.append("class_setup")
    yield "class"
    call_log.append("class_teardown")


class TestClassScopedFixture:
    def test_first(self, class_scoped):
        assert class_scoped == "class"

    def test_second(self, class_scoped):
        # Same instance — class_setup ran only once for this class
        assert class_scoped == "class"


@pytest.fixture(scope="module")
def shared_list():
    return []


def test_shared_list_first(shared_list):
    shared_list.append("a")
    assert "a" in shared_list


def test_shared_list_second(shared_list):
    # Module scope: same list — "a" is still there from the previous test
    assert "a" in shared_list
    shared_list.append("b")
    assert len(shared_list) == 2


# Q: Why NOT use session scope for a DB fixture that creates users?
# A: Tests that insert users would see each other's data. One test deleting
#    "alice" breaks another test that expects her to exist. Use function scope
#    so each test gets a clean database state.
