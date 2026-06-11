# INTERMEDIATE LEVEL — LESSON 5: Parametrize
#
# KEY CONCEPTS:
#   - @pytest.mark.parametrize runs one test with many inputs
#   - Eliminates copy-paste tests; each case is a separate test entry
#   - You can parametrize multiple arguments and combine parametrize decorators
#   - IDs make failures readable: FAILED test_email[bad@@email]
#
# RUN: pytest intermediate/05_parametrize/ -v

import pytest
from validators import is_valid_email, is_valid_password, is_valid_age, classify_temperature


# --- Basic parametrize ---

@pytest.mark.parametrize("email", [
    "user@example.com",
    "user.name+tag@domain.co.uk",
    "firstname.lastname@company.org",
])
def test_valid_emails(email):
    assert is_valid_email(email) is True


@pytest.mark.parametrize("email", [
    "notanemail",
    "missing@tld",
    "@nodomain.com",
    "spaces in@email.com",
    "",
])
def test_invalid_emails(email):
    assert is_valid_email(email) is False


# --- Parametrize with (input, expected) tuples ---

@pytest.mark.parametrize("password, expected", [
    ("Short1", False),          # too short
    ("alllowercase1", False),   # no uppercase
    ("ALLUPPERCASE1", True),    # has uppercase AND digit — valid!
    ("NoDigitsHere", False),    # no digit
    ("Valid1Pass", True),
    ("Another9Good", True),
])
def test_password_validation(password, expected):
    assert is_valid_password(password) == expected


# --- Parametrize with explicit IDs ---

@pytest.mark.parametrize("age, expected", [
    (0, True),
    (25, True),
    (150, True),
    (-1, False),
    (151, False),
    ("abc", False),
    (None, False),
], ids=[
    "zero", "adult", "max_age",
    "negative", "above_max", "string_input", "none_input",
])
def test_age_validation(age, expected):
    assert is_valid_age(age) == expected


# --- Parametrize with multiple arguments ---

@pytest.mark.parametrize("celsius, expected_category", [
    (-10, "freezing"),
    (5,   "cold"),
    (15,  "cool"),
    (25,  "warm"),
    (35,  "hot"),
    (0,   "cold"),       # boundary: 0 is NOT < 0, so falls to "cold"
    (10,  "cool"),       # boundary: 10 is NOT < 10, so falls to "cool"
])
def test_classify_temperature(celsius, expected_category):
    assert classify_temperature(celsius) == expected_category


# --- Combining parametrize decorators (cartesian product) ---
# This generates 2 × 3 = 6 test cases

@pytest.mark.parametrize("prefix", ["user", "admin"])
@pytest.mark.parametrize("domain", ["gmail.com", "outlook.com", "company.org"])
def test_email_formats(prefix, domain):
    email = f"{prefix}@{domain}"
    assert is_valid_email(email) is True


# EXERCISE:
# 1. Add a test case to test_password_validation for a password with special
#    characters like "P@ssw0rd" — does the validator accept it?
# 2. Parametrize a test for classify_temperature with 100 and -273 — edge cases.
# 3. Use indirect parametrize to inject a fixture value (look up pytest docs).
