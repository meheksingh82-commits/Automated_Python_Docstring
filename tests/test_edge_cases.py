import pytest
from docgen.check_docs import count_items


def test_empty_file():
    """Test that empty source returns zero counts."""
    source = ""
    total, documented, missing = count_items(source, "empty.py")

    assert total == 0
    assert documented == 0
    assert missing == []


def test_nested_functions():
    """Test that nested functions are counted correctly."""
    source = """
def outer():
    \"\"\"Outer function docstring\"\"\"

    def inner():
        \"\"\"Inner function docstring\"\"\"
        pass

    return inner
"""
    total, documented, missing = count_items(source, "nested.py")

    assert total == 2
    assert documented == 2
    assert missing == []


def test_nested_missing_docstring():
    """Test detection when inner function lacks docstring."""
    source = """
def outer():
    \"\"\"Outer function docstring\"\"\"

    def inner():
        pass

    return inner
"""
    total, documented, missing = count_items(source, "nested_missing.py")

    assert total == 2
    assert documented == 1
    assert len(missing) == 1
    assert "inner" in missing[0]


def test_decorated_function():
    """Test that decorated functions are counted correctly."""
    source = """
def decorator(func):
    return func

@decorator
def my_function():
    \"\"\"This function has a docstring.\"\"\"
    pass
"""
    total, documented, missing = count_items(source, "decorated.py")

    # decorator + my_function
    assert total == 2
    assert documented == 1
    assert len(missing) == 1
    assert "decorator" in missing[0]


def test_class_without_methods_documented():
    """Test class without methods but with docstring."""
    source = """
class MyClass:
    \"\"\"This is a documented class.\"\"\"
    pass
"""
    total, documented, missing = count_items(source, "class_doc.py")

    assert total == 1
    assert documented == 1
    assert missing == []


def test_class_without_methods_missing_docstring():
    """Test class without methods and missing docstring."""
    source = """
class MyClass:
    pass
"""
    total, documented, missing = count_items(source, "class_missing.py")

    assert total == 1
    assert documented == 0
    assert len(missing) == 1
    assert "MyClass" in missing[0]


def test_syntax_error_handling():
    """Test that syntax errors raise SyntaxError."""
    source = "def broken_function("  # invalid Python syntax

    with pytest.raises(SyntaxError):
        count_items(source, "broken.py")