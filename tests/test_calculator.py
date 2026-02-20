# import pytest
import pytest
from app.calculator import Calculator


@pytest.fixture
def calculator():
    return Calculator()


def test_add(calculator):
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0
    assert calculator.add(0, 0) == 0


def test_subtract(calculator):
    assert calculator.subtract(5, 3) == 2
    assert calculator.subtract(3, 5) == -2
    assert calculator.subtract(0, 0) == 0


def test_multiply(calculator):
    assert calculator.multiply(2, 3) == 6
    assert calculator.multiply(-2, 3) == -6
    assert calculator.multiply(0, 5) == 0


def test_divide(calculator):
    assert calculator.divide(6, 3) == 2
    assert calculator.divide(-6, 3) == -2


def test_divide_by_zero(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(5, 0)

def test_add_2_plus_3(calculator):
    assert calculator.add(2, 3) == 5

def test_add_negative_numbers(calculator):
    assert calculator.add(-1, -1) == -2
    # assert calculator.add(-1, -1) == -2
