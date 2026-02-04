import sys
import os
import ast

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from analyzer.parser import parse_code
from generator.styled_generator import generate_docstring
from config.config_loader import load_config


config = load_config()
docstring_style = config["docstring_style"].capitalize()


st.set_page_config(
    page_title="Docstring Review Prototype",
    layout="wide"
)


st.title("Docstring Review Interface")
st.write(
    "This interface allows developers to review generated docstrings "
    "before they are applied to the source file."
)


uploaded_file = st.file_uploader(
    "Upload Python File for Review",
    type=["py"]
)


if uploaded_file:
    source_code = uploaded_file.read().decode("utf-8")
    tree = ast.parse(source_code)
    lines = source_code.splitlines()

    st.subheader("Source Code")
    st.code(source_code, language="python")

    st.subheader("Docstring Suggestions")

    found = False

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if ast.get_docstring(node) is None:
                found = True

                start = node.lineno - 1
                end = node.end_lineno

                original = "\n".join(lines[start:end])

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

                st.markdown(f"### {node.__class__.__name__}: `{node.name}`")
                st.code(original, language="python")
                st.markdown("Generated Docstring")
                st.code(doc, language="python")

    if not found:
        st.success("All functions and classes already have docstrings.")