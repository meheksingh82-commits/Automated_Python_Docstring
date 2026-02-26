import ast
import pathlib
import sys

SRC_DIR = "src"
MIN_COVERAGE = 100  # Set to 100 if you want strict enforcement


def count_items(source, filename="<unknown>"):
    """
    Count total functions/classes and documented ones in a source file.
    
    Returns:
        total (int): Total number of functions/classes
        documented (int): Number of documented functions/classes
        missing (list): List of undocumented item names
    """
    tree = ast.parse(source)
    total = 0
    documented = 0
    missing = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            total += 1
            name = node.name

            if ast.get_docstring(node):
                documented += 1
            else:
                missing.append(f"{filename} -> {name}")

    return total, documented, missing


def main():
    """
    Run documentation coverage check across all Python files in src directory.
    """
    total_items = 0
    documented_items = 0
    missing_items = []

    for file in pathlib.Path(SRC_DIR).rglob("*.py"):
        try:
            source = file.read_text(encoding="utf-8")
            t, d, m = count_items(source, file.name)

            total_items += t
            documented_items += d
            missing_items.extend(m)

        except SyntaxError:
            print(f"Syntax error in file: {file}")
            sys.exit(1)

    if total_items == 0:
        print("No functions or classes found.")
        sys.exit(1)

    coverage = (documented_items / total_items) * 100

    print(f"\nTotal items: {total_items}")
    print(f"Documented items: {documented_items}")
    print(f"Documentation coverage: {coverage:.2f}%\n")

    if missing_items:
        print("Undocumented items:")
        for item in missing_items:
            print(f" - {item}")
        print()

    if coverage < MIN_COVERAGE:
        print("Coverage below required threshold.")
        sys.exit(1)

    print("Documentation check passed.")


if __name__ == "__main__":
    main()