# SOLUTIONS — Lesson 05: Parametrize

import pytest
from validators import is_valid_password, classify_temperature


@pytest.mark.parametrize("password, expected", [
    ("P@ssw0rd", True),    # special chars are fine — validator only checks upper + digit + length
    ("Str0ng!!", True),
    ("weak",     False),
])
def test_password_with_special_chars(password, expected):
    assert is_valid_password(password) == expected


@pytest.mark.parametrize("celsius, expected", [
    (100,  "hot"),
    (-273, "freezing"),
    (-0.1, "freezing"),
    (29.9, "warm"),
    (30.0, "hot"),
])
def test_temperature_edge_cases(celsius, expected):
    assert classify_temperature(celsius) == expected


# Indirect parametrize example — see pytest docs for full usage
# @pytest.mark.parametrize("username", ["alice", "bob"], indirect=True)
