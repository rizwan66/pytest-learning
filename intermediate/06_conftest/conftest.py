# conftest.py — INTERMEDIATE LEVEL — LESSON 6
#
# KEY CONCEPTS:
#   - conftest.py is auto-loaded by pytest — no import needed
#   - Fixtures defined here are available to ALL tests in this directory (and subdirs)
#   - This is the right place for shared setup: DB connections, HTTP clients, etc.
#   - yield fixtures: code before yield = setup, after yield = teardown

import pytest
from database import Database


@pytest.fixture
def db():
    """Fresh in-memory database for each test."""
    database = Database()
    yield database          # <-- test runs here
    database.close()        # teardown: always runs, even if test fails


@pytest.fixture
def db_with_users(db):
    """Database pre-loaded with sample users."""
    db.insert_user("Alice", "alice@example.com", role="admin")
    db.insert_user("Bob",   "bob@example.com",   role="user")
    db.insert_user("Carol", "carol@example.com", role="user")
    return db


@pytest.fixture
def sample_user_data():
    """Plain data fixture — no teardown needed."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "role": "user",
    }
