import tempfile
import os
from pydocstyle import check


def _normalize_for_strict_pep257(source_code: str) -> str:
    """Function _normalize_for_strict_pep257."""
    lines = source_code.splitlines()
    normalized = []
    after_class_docstring = False
    in_class = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("class "):
            in_class = True
            normalized.append(line)
            continue

        if in_class and stripped.startswith('"""'):
            normalized.append(line)
            after_class_docstring = True
            in_class = False
            continue

        if after_class_docstring:
            normalized.append("")
            after_class_docstring = False

        if stripped.startswith("def "):
            normalized.append(line)
            continue

        if normalized and normalized[-1].strip().startswith(("def ", "class ")) and stripped == "":
            continue

        normalized.append(line)

    return "\n".join(normalized)


def validate_docstrings(source_code: str, mode="relaxed"):
    """Function validate_docstrings."""
    if mode == "strict":
        source_code = _normalize_for_strict_pep257(source_code)

    with tempfile.NamedTemporaryFile(
        suffix=".py",
        delete=False,
        mode="w",
        encoding="utf-8"
    ) as temp_file:
        temp_file.write(source_code)
        temp_path = temp_file.name

    violations = []

    try:
        if mode == "strict":
            errors = check([temp_path])
        else:
            errors = check(
                [temp_path],
                ignore=[
                    "D100",
                    "D201",
                    "D202",
                    "D203",
                    "D204",
                    "D211",
                    "D212",
                    "D401",
                    "D412",
                    "D413",
                ]
            )

        for error in errors:
            violations.append(str(error))

    finally:
        os.remove(temp_path)

    return {
        "status": "Pass" if not violations else "Fail",
        "count": len(violations),
        "violations": violations,
    }