# BEGINNER LEVEL — LESSON 3: Fixtures
#
# KEY CONCEPTS:
#   - @pytest.fixture creates reusable setup code
#   - fixtures are injected by name into test function parameters
#   - fixtures replace repetitive setUp/tearDown boilerplate
#   - fixtures can depend on other fixtures
#
# RUN: pytest beginner/03_fixtures/ -v

import pytest
from user import User


# --- Defining a fixture ---

@pytest.fixture
def basic_user():
    # This runs before each test that requests it
    return User(name="Alice", email="alice@example.com", age=25)


@pytest.fixture
def minor_user():
    return User(name="Bob", email="bob@example.com", age=16)


@pytest.fixture
def user_with_cart(basic_user):
    # Fixtures can depend on other fixtures — just add them as parameters
    basic_user.add_to_cart("apple")
    basic_user.add_to_cart("banana")
    return basic_user


# --- Tests using fixtures ---

def test_user_starts_active(basic_user):
    assert basic_user.is_active is True


def test_user_name(basic_user):
    assert basic_user.name == "Alice"


def test_user_deactivate(basic_user):
    basic_user.deactivate()
    assert basic_user.is_active is False


def test_adult_user(basic_user):
    assert basic_user.is_adult() is True


def test_minor_user(minor_user):
    assert minor_user.is_adult() is False


# --- Fixtures with state ---

def test_cart_starts_empty(basic_user):
    assert basic_user._cart == []


def test_add_item_to_cart(basic_user):
    basic_user.add_to_cart("apple")
    assert "apple" in basic_user._cart


def test_cart_fixture_has_items(user_with_cart):
    assert len(user_with_cart._cart) == 2
    assert "apple" in user_with_cart._cart


def test_cart_total(user_with_cart):
    prices = {"apple": 1.50, "banana": 0.75}
    total = user_with_cart.cart_total(prices)
    assert total == pytest.approx(2.25)


def test_fixtures_are_independent(basic_user):
    # Each test gets a FRESH fixture — changes in one test don't leak
    assert basic_user._cart == []  # Not affected by test_add_item_to_cart


# --- tmpdir: a built-in fixture ---

def test_write_and_read_file(tmp_path):
    # tmp_path is a pytest built-in fixture — a temporary directory
    file = tmp_path / "notes.txt"
    file.write_text("hello pytest")
    assert file.read_text() == "hello pytest"


def test_multiple_tmp_files(tmp_path):
    (tmp_path / "a.txt").write_text("aaa")
    (tmp_path / "b.txt").write_text("bbb")
    files = list(tmp_path.iterdir())
    assert len(files) == 2


# EXERCISE:
# 1. Create a fixture called `admin_user` with age=30 and name="Admin".
# 2. Write a test that deactivates the user and confirms the cart is still accessible.
# 3. Use tmp_path to write a JSON file and read it back.
