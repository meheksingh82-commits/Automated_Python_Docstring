from injector.docstring_injector import inject_docstrings

code = """
def add(a, b):
    return a + b
"""

updated = inject_docstrings(code, "Google")
print(updated)