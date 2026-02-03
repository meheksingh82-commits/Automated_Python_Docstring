import ast
from generator.styled_generator import generate_docstring


def inject_docstrings(source_code, docstring_style):
    tree = ast.parse(source_code)
    lines = source_code.splitlines()

    insertions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if ast.get_docstring(node) is None:
                insert_line = node.body[0].lineno - 1
                indent = " " * node.col_offset

                if isinstance(node, ast.ClassDef):
                    params = []
                else:
                    params = [arg.arg for arg in node.args.args]

                doc = generate_docstring(
                    {
                        "name": node.name,
                        "params": params
                    },
                    docstring_style
                )

                formatted = [
                    indent + '"""',
                    indent + doc.strip().replace("\n", "\n" + indent),
                    indent + '"""'
                ]

                insertions.append((insert_line, formatted))

    offset = 0
    for line_no, doc_lines in sorted(insertions):
        index = line_no + offset
        lines[index:index] = doc_lines
        offset += len(doc_lines)

    return "\n".join(lines)
