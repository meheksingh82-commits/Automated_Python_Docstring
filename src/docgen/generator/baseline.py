def generate_baseline_docstring(func_info: dict) -> str:
    """
    Generates a baseline docstring for a function.
    """
    lines = []
    lines.append('"""')
    lines.append(f"Function {func_info['name']}.")
    lines.append("")

    if func_info["params"]:
        lines.append("Args:")
        for param in func_info["params"]:
            lines.append(f"    {param}: parameter")
        lines.append("")

    lines.append("Returns:")
    lines.append("    value")
    lines.append('"""')

    return "\n".join(lines)