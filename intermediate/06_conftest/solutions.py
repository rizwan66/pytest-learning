# SOLUTIONS — Lesson 06: conftest.py

import pytest
from database import Database


@pytest.fixture
def admin_db():
    """One admin + three regular users."""
    db = Database()
    db.insert_user("Admin", "admin@example.com", role="admin")
    db.insert_user("User1", "user1@example.com")
    db.insert_user("User2", "user2@example.com")
    db.insert_user("User3", "user3@example.com")
    yield db
    db.close()


def test_admin_db_has_one_admin(admin_db):
    users = admin_db.get_all_users()
    admins = [u for u in users if u["role"] == "admin"]
    assert len(admins) == 1


def test_delete_nonexistent_email_does_not_raise(admin_db):
    # Should silently do nothing
    admin_db.delete_user("ghost@example.com")
    assert len(admin_db.get_all_users()) == 4


@pytest.fixture(scope="module")
def module_db():
    """Created once for the whole module — observe it in logs with -s."""
    print("\n[module_db] setup")
    db = Database()
    db.insert_user("Shared", "shared@example.com")
    yield db
    print("\n[module_db] teardown")
    db.close()


def test_module_db_first(module_db):
    assert module_db.get_user_by_email("shared@example.com") is not None


def test_module_db_second(module_db):
    # Same db instance — module_db setup ran only once
    assert module_db.get_all_users()[0]["name"] == "Shared"
