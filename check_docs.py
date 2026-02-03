import sys
import pathlib

from analyzer.parser import parse_code
from reports.coverage import generate_coverage_report
from reports.validation import validate_docstrings
from config.config_loader import load_config


def main():
    config = load_config()
    mode = config["validation_mode"]
    min_coverage = config["min_coverage"]

    python_files = pathlib.Path(".").rglob("*.py")
    all_functions = []
    all_classes = []

    for file in python_files:
        if "venv" in str(file) or ".git" in str(file):
            continue

        source = file.read_text(encoding="utf-8")

        functions, classes = parse_code(source)
        all_functions.extend(functions)
        all_classes.extend(classes)

        validation = validate_docstrings(source, mode)
        if validation["status"] == "Fail":
            print(f"❌ Docstring validation failed in {file}")
            sys.exit(1)

    report = generate_coverage_report(all_functions, all_classes)

    if report["coverage"] < min_coverage:
        print(
            f"❌ Documentation coverage too low "
            f"({report['coverage']}% < {min_coverage}%)"
        )
        sys.exit(1)

    print("✅ Documentation checks passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
