# SOLUTIONS — Lesson 03: Fixtures

import json
import pytest
from user import User


@pytest.fixture
def admin_user():
    return User(name="Admin", email="admin@example.com", age=30)


def test_admin_user_is_adult(admin_user):
    assert admin_user.is_adult() is True


def test_admin_user_name(admin_user):
    assert admin_user.name == "Admin"


def test_deactivated_user_cart_still_accessible(admin_user):
    admin_user.add_to_cart("book")
    admin_user.deactivate()
    assert admin_user.is_active is False
    assert "book" in admin_user._cart  # cart survives deactivation


def test_write_json_with_tmp_path(tmp_path):
    data = {"user": "alice", "score": 42}
    file = tmp_path / "data.json"
    file.write_text(json.dumps(data))
    loaded = json.loads(file.read_text())
    assert loaded["user"] == "alice"
    assert loaded["score"] == 42
