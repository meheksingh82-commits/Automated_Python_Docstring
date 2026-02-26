"""
Demo module for documentation coverage example.
"""


def add(a, b):
    """
    Add two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Sum of a and b.
    """
    return a + b


def subtract(a, b):
    """
    Subtract second number from first.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Difference of a and b.
    """
    return a - b


def multiply(a, b):
    """
    Multiply two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Product of a and b.
    """
    return a * b


def divide(a, b):
    return a / b  


class Calculator:
    """
    Basic calculator class.
    """

    def power(self, base, exponent):
        """
        Raise base to exponent.

        Args:
            base: Base number.
            exponent: Power value.

        Returns:
            base ** exponent
        """
        return base ** exponent