import ast
import pathlib
import sys


SRC_DIR = "src"
MIN_COVERAGE = 90


def count_items(source):
    tree = ast.parse(source)
    total = 0
    documented = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            total += 1
            if ast.get_docstring(node):
                documented += 1

    return total, documented


def main():
    total_items = 0
    documented_items = 0

    for file in pathlib.Path(SRC_DIR).rglob("*.py"):
        source = file.read_text(encoding="utf-8")
        t, d = count_items(source)
        total_items += t
        documented_items += d

    if total_items == 0:
        print("No items found.")
        sys.exit(1)

    coverage = (documented_items / total_items) * 100
    print(f"Documentation coverage: {coverage:.2f}%")

    if coverage < MIN_COVERAGE:
        print("Coverage below required threshold.")
        sys.exit(1)

    print("Documentation check passed.")


if __name__ == "__main__":
    main()
