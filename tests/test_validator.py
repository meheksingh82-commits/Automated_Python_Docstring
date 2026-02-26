import ast


def validate_docstrings(source_code: str, mode="relaxed"):
    """
    Validate that all functions and classes contain docstrings.

    Strict mode:
        Requires docstrings for all functions and classes.

    Relaxed mode:
        Only checks presence of docstrings.
    """
    tree = ast.parse(source_code)

    violations = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                violations.append(
                    f"{node.__class__.__name__} '{node.name}' is missing a docstring."
                )

    return {
        "status": "Pass" if not violations else "Fail",
        "count": len(violations),
        "violations": violations,
    }