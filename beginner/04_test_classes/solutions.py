# SOLUTIONS — Lesson 04: Test Classes

import pytest
from calculator import Calculator


class TestEdgeCases:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.calc = Calculator()

    def test_add_zero_zero(self):
        assert self.calc.add(0, 0) == 0

    def test_multiply_by_one_identity(self):
        for x in [-5, 0, 1, 100]:
            assert self.calc.multiply(1, x) == x

    def test_multiply_by_negative_one(self):
        assert self.calc.multiply(-1, 7) == -7

    def test_divide_zero_by_nonzero(self):
        # 0 / 5 = 0.0 — should NOT raise
        assert self.calc.divide(0, 5) == 0.0

    def test_history_subtract_entry(self):
        self.calc.subtract(10, 3)
        op, a, b, result = self.calc.history[0]
        assert op == "subtract"
        assert a == 10
        assert b == 3
        assert result == 7
