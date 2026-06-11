# BEGINNER LEVEL — LESSON 1: Your First Tests
#
# KEY CONCEPTS:
#   - pytest discovers tests in files named test_*.py or *_test.py
#   - test functions must start with "test_"
#   - use plain `assert` — pytest rewrites it to show detailed failures
#
# RUN THIS FILE:
#   cd beginner/01_first_test
#   pytest test_math_utils.py -v

import pytest
from math_utils import add, subtract, multiply, divide, is_even, factorial


# --- Simplest possible test ---

def test_add_two_positive_numbers():
    result = add(3, 4)
    assert result == 7


def test_add_negative_numbers():
    assert add(-1, -1) == -2


def test_add_positive_and_negative():
    assert add(10, -3) == 7


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(3, 5) == 15


# --- Testing exceptions with pytest.raises ---

def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError):
        divide(10, 0)


def test_divide_by_zero_error_message():
    # You can also inspect the exception message
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)


def test_divide_normal():
    assert divide(10, 2) == 5.0


# --- Boolean assertions ---

def test_is_even_with_even_number():
    assert is_even(4) is True


def test_is_even_with_odd_number():
    assert is_even(7) is False


def test_is_even_zero():
    assert is_even(0)  # 0 is even


# --- Factorial ---

def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_positive():
    assert factorial(5) == 120


def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-1)


# EXERCISE:
# 1. Write a test for multiply(0, 100) — what should it return?
# 2. Write a test that checks divide(7, 2) returns 3.5 (not 3!)
# 3. Write a test for factorial(1) — is it 1?
