import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from analyzer.parser import parse_code
from reports.coverage import generate_coverage_report
from reports.validation import validate_docstrings
from config.config_loader import load_config
from injector.docstring_injector import inject_docstrings


config = load_config()

validation_mode = config["validation_mode"]
docstring_style = config["docstring_style"].capitalize()
min_coverage = config["min_coverage"]
inject_enabled = config["inject_docstrings"]


st.set_page_config(
    page_title="Automated Docstring Analysis Tool",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background-color: #8FB5A9;
}
.main-card {
    background-color: #FFFDF9;
    padding: 2rem;
    border-radius: 14px;
    margin: 2.2rem auto;
    max-width: 1100px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)


st.sidebar.title("Analysis Panel")

uploaded_file = st.sidebar.file_uploader(
    "Upload Python File",
    type=["py"]
)

run_analysis = st.sidebar.button("Analyze Codebase")


st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.title("Automated Docstring Analysis Tool")
st.write(
    "This tool analyzes Python documentation using AST-based parsing, "
    "evaluates documentation coverage, validates PEP 257 compliance, "
    "and injects missing docstrings into the source code."
)
st.markdown("</div>", unsafe_allow_html=True)


if uploaded_file and run_analysis:
    source_code = uploaded_file.read().decode("utf-8")

    functions, classes = parse_code(source_code)

    validation = validate_docstrings(
        source_code,
        mode=validation_mode
    )

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("## Source Code")
    st.code(source_code, language="python")
    st.markdown("</div>", unsafe_allow_html=True)

    report = generate_coverage_report(functions, classes)

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("## Documentation Coverage")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Items", report["total"])
    c2.metric("Documented", report["documented"])
    c3.metric("Missing", report["missing"])
    c4.metric("Coverage %", report["coverage"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("## Validation Summary")
    st.metric("Status", validation["status"])
    st.metric("Issues", validation["count"])

    if report["coverage"] < min_coverage:
        st.error(
            f"Coverage below required threshold "
            f"({report['coverage']}% < {min_coverage}%)"
        )

    if validation["status"] == "Fail":
        for issue in validation["violations"]:
            st.code(issue)

    st.markdown("</div>", unsafe_allow_html=True)

    if inject_enabled:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("## Injected Source Code")

        updated_code = inject_docstrings(
            source_code,
            docstring_style
        )

        st.code(updated_code, language="python")

        st.download_button(
            "Download Updated File with Injected Docstrings",
            updated_code,
            file_name="updated_with_docstrings.py"
        )

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("### Welcome")
    st.markdown(
        "Upload a Python file and click **Analyze Codebase** "
        "to analyze documentation quality and inject missing docstrings."
    )
    st.markdown("</div>", unsafe_allow_html=True)