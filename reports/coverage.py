def generate_coverage_report(functions: list, classes: list) -> dict:
    """
    Generates a documentation coverage report.
    """
    total = 0
    documented = 0

    # Count standalone functions
    for func in functions:
        total += 1
        if func["has_docstring"]:
            documented += 1

    # Count class methods
    for cls in classes:
        for method in cls["methods"]:
            total += 1
            if method["has_docstring"]:
                documented += 1

    missing = total - documented
    coverage = (documented / total * 100) if total > 0 else 0

    return {
        "total": total,
        "documented": documented,
        "missing": missing,
        "coverage": round(coverage, 2)
    }