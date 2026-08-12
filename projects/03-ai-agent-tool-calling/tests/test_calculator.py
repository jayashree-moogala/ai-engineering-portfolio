# Unit tests for your calculate() function. It verifies that the calculator behaves
# correctly for both valid inputs and invalid or unsafe inputs.


# Import the pytest testing framework.
#
# Pytest automatically discovers functions whose names
# begin with "test_" and executes them.
import pytest

# Import the function we want to test.
from app.tools.calculator import calculate


# -------------------------------------------------------------------
# Parameterized Test
# -------------------------------------------------------------------
#
# Instead of writing six separate test functions,
# pytest runs the same test multiple times with
# different input values.
#
@pytest.mark.parametrize(
    # Names of the parameters that will be passed
    # into the test function.
    ("expression", "expected"),
    # Test cases.
    #
    # Each tuple contains:
    #
    # (input_expression, expected_result)
    #
    [
        ("2 + 3", 5),
        ("10 / 2", 5),
        ("5 * 6", 30),
        ("2 ** 3", 8),
        ("(10 + 5) * 2", 30),
        ("-5 + 2", -3),
    ],
)
def test_calculate(
    expression: str,
    expected: float,
) -> None:

    # Execute the calculator and verify that
    # the returned value matches the expected result.
    #
    # If they are different,
    # pytest automatically reports the failure.
    assert calculate(expression) == expected


# -------------------------------------------------------------------
# Security Test
# -------------------------------------------------------------------
#
# Ensure that unsafe Python code is rejected.
#
# The calculator should evaluate arithmetic,
# NOT execute arbitrary Python code.
#
def test_calculate_rejects_unsafe_code() -> None:

    # Verify that calculate() raises a ValueError.
    #
    # If no exception is raised,
    # the test automatically fails.
    with pytest.raises(ValueError):

        # Attempt to execute operating system code.
        #
        # A secure calculator must reject this.
        calculate("__import__('os').system('dir')")


# -------------------------------------------------------------------
# Validation Test
# -------------------------------------------------------------------
#
# Verify that an empty expression is not allowed.
#
def test_calculate_rejects_empty_expression() -> None:

    # Expect a ValueError.
    with pytest.raises(ValueError):

        # Empty input should not be accepted.
        calculate("")
