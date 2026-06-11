# INTERMEDIATE LEVEL — LESSON 6: conftest.py + yield fixtures
#
# KEY CONCEPTS:
#   - Fixtures from conftest.py are available without importing
#   - yield fixtures guarantee teardown even when tests fail
#   - Fixtures compose: db_with_users depends on db
#
# RUN: pytest intermediate/06_conftest/ -v

import pytest


def test_empty_database(db):
    users = db.get_all_users()
    assert users == []


def test_insert_user(db, sample_user_data):
    uid = db.insert_user(**sample_user_data)
    assert isinstance(uid, int)
    assert uid > 0


def test_retrieve_inserted_user(db, sample_user_data):
    db.insert_user(**sample_user_data)
    user = db.get_user_by_email(sample_user_data["email"])
    assert user is not None
    assert user["name"] == sample_user_data["name"]
    assert user["role"] == "user"


def test_user_not_found(db):
    user = db.get_user_by_email("nonexistent@example.com")
    assert user is None


def test_preloaded_users(db_with_users):
    users = db_with_users.get_all_users()
    assert len(users) == 3


def test_find_admin_user(db_with_users):
    alice = db_with_users.get_user_by_email("alice@example.com")
    assert alice["role"] == "admin"


def test_delete_user(db_with_users):
    db_with_users.delete_user("bob@example.com")
    users = db_with_users.get_all_users()
    assert len(users) == 2
    assert db_with_users.get_user_by_email("bob@example.com") is None


def test_duplicate_email_raises(db, sample_user_data):
    db.insert_user(**sample_user_data)
    with pytest.raises(Exception):  # sqlite3.IntegrityError (UNIQUE constraint)
        db.insert_user(**sample_user_data)


def test_each_test_gets_fresh_db(db):
    # Even though db_with_users inserts 3 rows, this test has its own clean db
    users = db.get_all_users()
    assert len(users) == 0


# EXERCISE:
# 1. Add a fixture `admin_db` that seeds one admin and three regular users.
# 2. Write a test that verifies deleting a non-existent email doesn't raise.
# 3. Add a module-scoped fixture (scope="module") and observe it runs once.
