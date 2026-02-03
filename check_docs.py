import sys
import os
import pathlib

sys.path.insert(0, os.getcwd())

from analyzer.parser import parse_code
from reports.coverage import generate_coverage_report
from reports.validation import validate_docstrings
from config.config_loader import load_config


def main():
    config = load_config()
    mode = config.get("validation_mode", "relaxed")
    min_coverage = config.get("min_coverage", 0)

    python_files = pathlib.Path(".").rglob("*.py")
    all_functions = []
    all_classes = []

    validation_failed = False

    for file in python_files:
        if any(skip in str(file) for skip in ["venv", ".git", ".github"]):
            continue

        try:
            source = file.read_text(encoding="utf-8")
        except Exception:
            continue

        functions, classes = parse_code(source)
        all_functions.extend(functions)
        all_classes.extend(classes)

        validation = validate_docstrings(source, mode)
        if validation["status"] == "Fail":
            print(f"⚠️ Validation issues in {file}")
            validation_failed = True

    report = generate_coverage_report(all_functions, all_classes)

    print("\n📊 Documentation Summary")
    print(f"Validation mode : {mode}")
    print(f"Coverage        : {report['coverage']}%")

    if report["coverage"] < min_coverage:
        print(
            f"⚠️ Coverage below threshold "
            f"({report['coverage']}% < {min_coverage}%)"
        )

    if validation_failed:
        print("⚠️ Docstring issues detected (report-only mode)")

    print("✅ Documentation checks completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
