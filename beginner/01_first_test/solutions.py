# SOLUTIONS — Lesson 01: First Tests
# These are the answers to the EXERCISE at the bottom of test_math_utils.py.

from math_utils import multiply, divide, factorial
import pytest


def test_multiply_by_zero():
    assert multiply(0, 100) == 0


def test_divide_returns_float():
    result = divide(7, 2)
    assert result == 3.5
    assert isinstance(result, float)


def test_factorial_one():
    assert factorial(1) == 1
