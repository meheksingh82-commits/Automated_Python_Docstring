def generate_google_style(func):
    """
    Generate a Google-style docstring.
    """
    params = "\n".join(
        [f"    {param}: description" for param in func["params"]]
    )

    docstring = f'''"""
{func["name"]} function.

Args:
{params}

Returns:
    value
"""
'''
    return docstring


def generate_numpy_style(func):
    """
    Generate a NumPy-style docstring.
    """
    params = "\n".join(
        [f"{param} : type\n    description" for param in func["params"]]
    )

    docstring = f'''"""
{func["name"]} function.

Parameters
----------
{params}

Returns
-------
value
"""
'''
    return docstring


def generate_rest_style(func):
    """
    Generate a reStructuredText (reST) style docstring.
    """
    params = "\n".join(
        [f":param {param}: description" for param in func["params"]]
    )

    docstring = f'''"""
{func["name"]} function.

{params}
:return: value
"""
'''
    return docstring


def generate_docstring(func, style="google"):
    """
    Dispatcher function to select docstring style.
    """
    style = style.lower()

    if style == "google":
        return generate_google_style(func)
    elif style == "numpy":
        return generate_numpy_style(func)
    elif style == "rest":
        return generate_rest_style(func)
    else:
        raise ValueError("Unsupported docstring style")