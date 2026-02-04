import ast


def inject_docstrings(source_code: str, style: str) -> str:
    """Function inject_docstrings."""
    lines = source_code.splitlines()
    tree = ast.parse(source_code)

    inserts = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if ast.get_docstring(node):
                continue

            indent = " " * node.col_offset
            doc_indent = indent + " " * 4

            if isinstance(node, ast.ClassDef):
                doc = f'{doc_indent}"""Class {node.name}."""'
            else:
                doc = f'{doc_indent}"""Function {node.name}."""'

            inserts.append((node.body[0].lineno - 1, doc))

    for lineno, doc in sorted(inserts, reverse=True):
        lines.insert(lineno, doc)

    return "\n".join(lines)