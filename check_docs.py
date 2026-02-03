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

    validation_failed = False

    for file in python_files:
        if "venv" in str(file) or ".git" in str(file):
            continue

        source = file.read_text(encoding="utf-8")

        functions, classes = parse_code(source)
        all_functions.extend(functions)
        all_classes.extend(classes)

        validation = validate_docstrings(source, mode)
        if validation["status"] == "Fail":
            print(f"⚠️ Docstring validation issues in {file}")
            validation_failed = True

    report = generate_coverage_report(all_functions, all_classes)

    if report["coverage"] < min_coverage:
        print(
            f"⚠️ Documentation coverage below threshold "
            f"({report['coverage']}% < {min_coverage}%)"
        )

    print("📊 Documentation Summary")
    print(f"Validation mode: {mode}")
    print(f"Coverage: {report['coverage']}%")

    if validation_failed:
        print("⚠️ Some documentation issues were found (reported only)")

    print("✅ Documentation checks completed")
    sys.exit(0)


if __name__ == "__main__":
    main()

