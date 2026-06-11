# ADVANCED LEVEL — LESSON 10: Advanced Fixture Patterns
#
# RUN: pytest advanced/10_yield_fixtures/ -v
# RUN with env: pytest advanced/10_yield_fixtures/ --env=staging -v

import pytest


# --- Factory fixture ---

def test_create_single_file(make_temp_file):
    f = make_temp_file("hello.txt", "world")
    assert f.exists()
    assert f.read_text() == "world"


def test_create_multiple_files(make_temp_file):
    a = make_temp_file("a.txt", "aaa")
    b = make_temp_file("b.txt", "bbb")
    assert a.read_text() == "aaa"
    assert b.read_text() == "bbb"
    assert a != b  # different files


def test_factory_files_have_correct_names(make_temp_file):
    f = make_temp_file("data.json", '{"key": 1}')
    assert f.name == "data.json"


# --- request.addfinalizer ---

def test_resource_created(managed_resource):
    r = managed_resource("conn-1")
    assert r["closed"] is False


def test_multiple_resources_allocated(managed_resource):
    r1 = managed_resource("r1")
    r2 = managed_resource("r2")
    assert r1["name"] == "r1"
    assert r2["name"] == "r2"
    # After the test, cleanup() is called — r1 and r2 get closed=True


# --- Parametrized fixtures ---
# These 3 tests run 3 times each (once per db_backend param)
# You'll see: test_backend_is_connected[sqlite], ...[postgres], ...[mysql]

def test_backend_is_connected(db_backend):
    assert db_backend["connected"] is True


def test_backend_name_is_set(db_backend):
    assert db_backend["backend"] in ("sqlite", "postgres", "mysql")


def test_backend_specific_behavior(db_backend):
    if db_backend["backend"] == "sqlite":
        assert db_backend["backend"] == "sqlite"
    else:
        assert len(db_backend["backend"]) >= 5


# --- CLI option fixture ---

def test_env_fixture_default(env):
    # Run without --env: should be "test"
    # Run with --env=staging: should be "staging"
    assert env in ("test", "staging", "production", "dev")


def test_env_is_string(env):
    assert isinstance(env, str)
    assert len(env) > 0


# --- Nesting factory fixtures ---

@pytest.fixture
def make_user():
    """Factory for user dicts — keeps test data creation flexible."""
    counter = [0]

    def _make(name=None, role="user", active=True):
        counter[0] += 1
        return {
            "id": counter[0],
            "name": name or f"User{counter[0]}",
            "role": role,
            "active": active,
        }

    return _make


def test_make_single_user(make_user):
    u = make_user(name="Alice", role="admin")
    assert u["name"] == "Alice"
    assert u["role"] == "admin"


def test_make_multiple_users_have_unique_ids(make_user):
    users = [make_user() for _ in range(5)]
    ids = [u["id"] for u in users]
    assert len(set(ids)) == 5  # all unique


# EXERCISE:
# 1. Create a fixture `make_post` that takes a make_user fixture and creates
#    a post dict with an author field set to a user.
# 2. Add a --count CLI option and use it in a fixture that yields that many objects.
# 3. Combine parametrized fixture with a factory — run all backends × 3 user types.
