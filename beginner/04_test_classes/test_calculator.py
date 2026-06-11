# BEGINNER LEVEL — LESSON 4: Grouping Tests with Classes
#
# KEY CONCEPTS:
#   - Test classes group related tests (no __init__ needed)
#   - Class-level fixtures use `self` — or use method-level fixtures
#   - Use class to share context; don't use it just for grouping names
#
# RUN: pytest beginner/04_test_classes/ -v

import pytest
from calculator import Calculator


class TestBasicArithmetic:
    """Tests for individual Calculator operations."""

    @pytest.fixture(autouse=True)
    def setup(self):
        # autouse=True: this fixture runs automatically for every test in the class
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(2, 3) == 5

    def test_subtract(self):
        assert self.calc.subtract(10, 4) == 6

    def test_multiply(self):
        assert self.calc.multiply(3, 7) == 21

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5.0

    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(5, 0)

    def test_divide_returns_float(self):
        result = self.calc.divide(7, 2)
        assert isinstance(result, float)
        assert result == 3.5


class TestCalculatorHistory:
    """Tests for the Calculator's history feature."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.calc = Calculator()

    def test_history_starts_empty(self):
        assert self.calc.history == []

    def test_operation_is_recorded(self):
        self.calc.add(1, 2)
        assert len(self.calc.history) == 1

    def test_history_contains_correct_operation(self):
        self.calc.add(1, 2)
        op, a, b, result = self.calc.history[0]
        assert op == "add"
        assert result == 3

    def test_multiple_operations_recorded(self):
        self.calc.add(1, 1)
        self.calc.subtract(5, 2)
        self.calc.multiply(3, 3)
        assert len(self.calc.history) == 3

    def test_last_result(self):
        self.calc.add(4, 6)
        assert self.calc.last_result() == 10

    def test_last_result_empty(self):
        assert self.calc.last_result() is None

    def test_clear_history(self):
        self.calc.add(1, 1)
        self.calc.clear_history()
        assert self.calc.history == []

    def test_history_isolated_between_tests(self):
        # autouse fixture gives a fresh Calculator — no cross-test contamination
        assert len(self.calc.history) == 0


# EXERCISE:
# 1. Add a TestEdgeCases class that tests add(0, 0), multiply(1, x)==x, etc.
# 2. What happens with divide(0, 5)? Write a test for it.
# 3. Test that history stores the subtract entry with correct a, b values.
