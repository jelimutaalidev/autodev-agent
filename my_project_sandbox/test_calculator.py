import pytest

def test_add():
    from calculator import add
    assert add(2, 3) == 5

def test_subtract():
    from calculator import subtract
    assert subtract(10, 5) == 5

def test_divide():
    from calculator import divide
    # Normal case
    assert divide(10, 2) == 5
    
    # Edge case: Division by zero MUST raise ValueError
    # (The agent usually forgets this or raises ZeroDivisionError instead, causing a failure)
    with pytest.raises(ValueError):
        divide(10, 0)
