import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from analyzer.parser import parse_code
from generator.styled_generator import generate_docstring
from reports.coverage import generate_coverage_report
from reports.validation import validate_docstrings


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

h1 {
    color: #1F3D36;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

h2 {
    color: #1F3D36;
    font-weight: 600;
    margin-top: 1.6rem;
    margin-bottom: 0.8rem;
}

p {
    color: #2F2F2F;
    font-size: 15px;
}

.section-divider {
    height: 1px;
    background-color: #E6DCD2;
    margin: 2rem 0;
}

pre {
    background-color: #F3EEE8 !important;
    border-left: 4px solid #E8B7A4;
    border-radius: 10px;
}

div[data-testid="metric-container"] {
    background-color: #FFFDF9;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #E2D8CE;
}
</style>
""", unsafe_allow_html=True)


st.sidebar.title("Analysis Panel")
st.sidebar.markdown(
    "Upload a Python file and select the documentation style and "
    "validation mode before analysis."
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Python File",
    type=["py"]
)

doc_style = st.sidebar.selectbox(
    "Docstring Style",
    ["Google", "NumPy", "reST"]
)

validation_mode = st.sidebar.radio(
    "Validation Mode",
    ["Relaxed", "Strict"]
)

run_analysis = st.sidebar.button("Analyze Codebase")


st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.title("Automated Docstring Analysis Tool")
st.write(
    "A documentation-first static analysis tool designed to improve "
    "Python code quality using AST-based inspection."
)
st.markdown("</div>", unsafe_allow_html=True)


if uploaded_file and run_analysis:
    source_code = uploaded_file.read().decode("utf-8")

    functions, classes = parse_code(source_code)
    mode = "strict" if validation_mode == "Strict" else "relaxed"
    validation = validate_docstrings(source_code, mode)

    failing_lines = set()
    for issue in validation["violations"]:
        parts = issue.split(":")
        if len(parts) > 1 and parts[1].strip().isdigit():
            failing_lines.add(int(parts[1].strip()))

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("## Source Code")
    st.code(source_code, language="python")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("## Generated Docstrings")
    for f in functions:
        st.code(generate_docstring(f, doc_style), language="python")
    for cls in classes:
        for method in cls["methods"]:
            st.code(generate_docstring(method, doc_style), language="python")
    st.markdown("</div>", unsafe_allow_html=True)

    report = generate_coverage_report(functions, classes)

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("## Documentation Coverage")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", report["total"])
    c2.metric("Documented", report["documented"])
    c3.metric("Missing", report["missing"])
    c4.metric("Coverage %", report["coverage"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("## Validation Summary")

    status_color = "#2E7D32" if validation["status"] == "Pass" else "#C62828"
    st.markdown(
        f"<p style='font-weight:600;color:{status_color};'>Status: {validation['status']}</p>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Issues", validation["count"])
    c2.metric("Affected Lines", len(failing_lines))
    c3.metric("Validation Mode", validation_mode)

    if validation["status"] == "Fail":
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        for issue in validation["violations"]:
            st.code(issue)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("## Export Report")
    st.markdown("Download a summary of coverage and validation results.")

    export_text = f"""
AUTOMATED DOCSTRING ANALYSIS REPORT

Docstring Style   : {doc_style}
Validation Mode   : {validation_mode}

COVERAGE
Total Items       : {report['total']}
Documented        : {report['documented']}
Missing           : {report['missing']}
Coverage          : {report['coverage']}%

VALIDATION
Status            : {validation['status']}
Issues            : {validation['count']}
Affected Lines    : {len(failing_lines)}
"""

    st.download_button(
        "Download Analysis Report",
        export_text,
        file_name="docstring_analysis_report.txt"
    )

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("### Welcome")
    st.markdown(
        "Upload a Python file from the sidebar to analyze documentation "
        "coverage, generate docstrings, and validate against standards."
    )
    st.markdown("</div>", unsafe_allow_html=True)


st.caption("Docstring Analyzer • Clean Professional UI • Milestone 2")
