# Simple calculator module

def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b (a - b)."""
    return a - b


def divide(a, b):
    """Return the division of a by b.

    Note: This naive implementation does not handle division by zero specially.
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b
