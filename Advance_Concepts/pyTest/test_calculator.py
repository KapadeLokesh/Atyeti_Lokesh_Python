# test_calculator.py

import pytest
from calculator import Calculator

@pytest.fixture
def calc():
    """Provides a Calculator instance."""
    return Calculator()

def test_addition(calc):
    """Test addition method."""
    assert calc.add(2, 3) == 5

def test_subtraction(calc):
    """Test subtraction method."""
    assert calc.subtract(5, 3) == 2

def test_multiplication(calc):
    """Test multiplication method."""
    assert calc.multiply(3, 4) == 12

def test_division(calc):
    """Test division method."""
    assert calc.divide(8, 2) == 4

def test_division_by_zero(calc):
    """Test division by zero raises ValueError."""
    with pytest.raises(ValueError):
        calc.divide(10, 0)

"""Code Explanation:

The code imports pytest and the Calculator class, which has four basic arithmetic methods: add(), subtract(), multiply(), divide() (raises a ValueError if the divisor is zero).
A pytest fixture (calc) creates a new Calculator instance before each test.
This ensures each test runs independently without affecting others.
Each test function (e.g., test_addition(), test_subtraction()) receives the calc fixture as an argument.
These functions use the Calculator instance to verify if the methods work correctly.
Example: test_addition() checks if add() returns the correct sum.
"""