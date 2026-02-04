import ast
import os
import pathlib


SRC_DIR = "src"


def has_docstring(node):
    return ast.get_docstring(node) is not None


def generate_google_docstring(name, params):
    lines = [
        f"{name}.",
        "",
        "Args:",
    ]
    for p in params:
        lines.append(f"    {p}: description")
    lines.append("")
    lines.append("Returns:")
    lines.append("    description")
    return '\n'.join(lines)


def inject_docstrings(source):
    tree = ast.parse(source)
    lines = source.splitlines()
    inserts = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and not has_docstring(node):
            indent = " " * node.col_offset + " " * 4
            params = []

            if isinstance(node, ast.FunctionDef):
                params = [arg.arg for arg in node.args.args]

            doc = generate_google_docstring(node.name, params)
            doc_block = indent + '"""' + doc.replace("\n", "\n" + indent) + '"""'

            inserts.append((node.body[0].lineno - 1, doc_block))

    for lineno, doc in sorted(inserts, reverse=True):
        lines.insert(lineno, doc)

    return "\n".join(lines)


def main():
    for file in pathlib.Path(SRC_DIR).rglob("*.py"):
        source = file.read_text(encoding="utf-8")
        updated = inject_docstrings(source)

        if source != updated:
            file.write_text(updated, encoding="utf-8")
            print(f"Injected docstrings in {file}")


if __name__ == "__main__":
    main()
