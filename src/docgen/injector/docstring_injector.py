import ast


def inject_docstrings(source_code: str, style: str = "Google") -> str:
    """
    Inject missing docstrings into functions and classes
    using Google style format.
    """
    tree = ast.parse(source_code)
    lines = source_code.splitlines()

    inserts = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):

            # Skip if docstring already exists
            if ast.get_docstring(node):
                continue

            indent = " " * node.col_offset
            doc_indent = indent + " " * 4

            if isinstance(node, ast.ClassDef):
                docstring = [
                    f'{doc_indent}"""',
                    f"{doc_indent}{node.name} class.",
                    f'{doc_indent}"""'
                ]
            else:
                docstring = [
                    f'{doc_indent}"""',
                    f"{doc_indent}{node.name} function.",
                    "",
                    f"{doc_indent}Args:",
                ]

                for arg in node.args.args:
                    docstring.append(f"{doc_indent}    {arg.arg}: Description.")

                docstring.extend([
                    "",
                    f"{doc_indent}Returns:",
                    f"{doc_indent}    Description.",
                    f'{doc_indent}"""'
                ])

            # Insert after function/class definition line
            insert_position = node.lineno
            inserts.append((insert_position, docstring))

    # Insert from bottom to top to avoid shifting issues
    for lineno, doc_lines in sorted(inserts, reverse=True):
        for line in reversed(doc_lines):
            lines.insert(lineno, line)

    return "\n".join(lines)