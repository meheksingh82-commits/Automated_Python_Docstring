from analyzer.parser import parse_code
from generator.baseline import generate_baseline_docstring
from reports.coverage import generate_coverage_report


def main():
    """Function main."""
    print("RUN_PARSER STARTED")

    with open("sample.py", "r") as f:
        source_code = f.read()

    print("\nSOURCE CODE READ:\n")
    print(source_code)

    functions, classes = parse_code(source_code)

    print("\nGENERATED DOCSTRINGS:\n")

    # Standalone functions
    for func in functions:
        print(generate_baseline_docstring(func))
        print()

    # Class methods
    for cls in classes:
        print(f"Class: {cls['name']}")
        for method in cls["methods"]:
            print(generate_baseline_docstring(method))
            print()

    report = generate_coverage_report(functions, classes)

    print("\nDOCUMENTATION COVERAGE REPORT:")
    print(f"Total items: {report['total']}")
    print(f"Documented: {report['documented']}")
    print(f"Missing docstrings: {report['missing']}")
    print(f"Coverage: {report['coverage']}%")


if __name__ == "__main__":
    main()