import ast


def parse_code(source_code: str):
    """
    Parses Python source code and extracts functions and classes
    along with docstring presence metadata.
    """
    tree = ast.parse(source_code)
    functions = []
    classes = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "params": [arg.arg for arg in node.args.args],
                "has_docstring": ast.get_docstring(node) is not None,
                "type": "function"
            })

        elif isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "has_docstring": ast.get_docstring(node) is not None,
                "methods": [],
                "type": "class"
            }

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    class_info["methods"].append({
                        "name": item.name,
                        "params": [arg.arg for arg in item.args.args],
                        "has_docstring": ast.get_docstring(item) is not None,
                        "type": "method"
                    })

            classes.append(class_info)

    return functions, classes