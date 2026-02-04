import ast

def parse_code(source_code: str):
    """
    Parses Python source code and extracts functions and classes.
    """
    tree = ast.parse(source_code)
    functions = []
    classes = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "params": [arg.arg for arg in node.args.args],
                "has_docstring": ast.get_docstring(node) is not None
            })

        elif isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "methods": []
            }

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    class_info["methods"].append({
                        "name": item.name,
                        "params": [arg.arg for arg in item.args.args],
                        "has_docstring": ast.get_docstring(item) is not None
                    })

            classes.append(class_info)

    return functions, classes
print("parse_code is defined")