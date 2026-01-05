# ui/app.py

import sys
import os

# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from analyzer.parser import parse_code
from generator.baseline import generate_baseline_docstring
from reports.coverage import generate_coverage_report


# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Automated Docstring Generator",
    layout="centered"
)

# --------------------------------------------------
# Dark Blue – Minimal Professional Theme
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0F172A;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }

    h1 {
        color: #E5E7EB;
        font-weight: 700;
    }

    h2, h3 {
        color: #CBD5E1;
        font-weight: 600;
    }

    p, label {
        color: #E5E7EB;
        font-size: 15px;
    }

    section[data-testid="stFileUploader"] {
        background-color: #111827;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #1E293B;
    }

    .stButton > button {
        background-color: #2563EB;
        color: white;
        border-radius: 6px;
        height: 2.8em;
        font-size: 14px;
        font-weight: 600;
        border: none;
    }

    .stButton > button:hover {
        background-color: #1D4ED8;
    }

    pre {
        background-color: #020617 !important;
        border-radius: 8px;
        border-left: 4px solid #2563EB;
        padding: 1rem;
        color: #E5E7EB !important;
    }

    div[data-testid="metric-container"] {
        background-color: #111827;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #1E293B;
        color: #E5E7EB;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("📄 Automated Python Docstring Generator")

st.write(
    "Generate baseline docstrings and analyze documentation coverage "
    "using AST-based static analysis."
)

st.divider()

# --------------------------------------------------
# File Upload
# --------------------------------------------------
st.subheader("📁 Upload Python File")

uploaded_file = st.file_uploader(
    "Select a Python (.py) file to analyze 📄",
    type=["py"]
)

# --------------------------------------------------
# Main Logic
# --------------------------------------------------
if uploaded_file:
    source_code = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Source Code")
    st.code(source_code, language="python")

    st.divider()

    col_run, col_hint = st.columns([1, 2])
    with col_run:
        run_clicked = st.button("🚀 Generate Docstrings")
    with col_hint:
        st.caption("🔄 You can re-run after uploading a different file")

    if run_clicked:
        functions, classes = parse_code(source_code)

        st.success("✔ Analysis completed successfully")

        # --------------------------------------------------
        # Generated Docstrings
        # --------------------------------------------------
        st.subheader("🧾 Generated Docstrings")

        # Standalone functions
        if functions:
            st.markdown("### 📄 Functions")
            for func in functions:
                doc = generate_baseline_docstring(func)
                st.code(doc, language="python")
        else:
            st.info("ℹ No standalone functions found.")

        # Class methods
        if classes:
            for cls in classes:
                st.markdown(f"### 📁 Class: `{cls['name']}`")
                for method in cls["methods"]:
                    doc = generate_baseline_docstring(method)
                    st.code(doc, language="python")

        # --------------------------------------------------
        # Coverage Report
        # --------------------------------------------------
        report = generate_coverage_report(functions, classes)

        st.divider()
        st.subheader("🧾 Documentation Coverage Report")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📄 Total Items", report["total"])
        col2.metric("✔ Documented", report["documented"])
        col3.metric("❌ Missing", report["missing"])
        col4.metric("📊 Coverage (%)", report["coverage"])

else:
    st.info("⬆ Upload a Python file to get started")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption("📄 Automated Docstring Generator • Internship Project")
