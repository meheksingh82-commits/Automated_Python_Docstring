import sys
import os
import streamlit as st
import difflib
import time
from io import BytesIO
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analyzer.parser import parse_code
from reports.coverage import generate_coverage_report
from injector.docstring_injector import inject_docstrings


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Automated Python Docstring Generator",
    layout="wide",
    page_icon="📘"
)

# ---------------- THEME ----------------
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    background = "#0F172A"
    text_color = "white"
    card_color = "#1E293B"
else:
    background = "linear-gradient(180deg, #EAF6FF 0%, #F8FBFF 100%)"
    text_color = "#1F2937"
    card_color = "white"

st.markdown(f"""
<style>
.stApp {{
    background: {background};
    color: {text_color};
}}
.section {{
    background: {card_color};
    padding: 1.5rem;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
}}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙ Control Panel")

uploaded_files = st.sidebar.file_uploader(
    "Upload Python Files",
    type=["py"],
    accept_multiple_files=True
)

auto_inject = st.sidebar.toggle("Enable Auto Injection", value=True)

st.sidebar.markdown("---")
st.sidebar.caption("Automated Python Docstring Generator")


# ---------------- HEADER ----------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("## 📘 Automated Python Docstring Generator")
st.markdown("Smart documentation analyzer with automatic Google-style docstring upgrades.")
st.markdown("</div>", unsafe_allow_html=True)


# ---------------- PDF GENERATOR ----------------
def generate_pdf(results):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Documentation Coverage Report", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    for name, coverage, grade in results:
        line = f"File: {name} | Coverage: {coverage}% | Grade: {grade}"
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


# ---------------- MAIN PROCESS ----------------
if uploaded_files:

    overall_results = []

    for file in uploaded_files:

        source_code = file.read().decode("utf-8")
        functions, classes = parse_code(source_code)
        report = generate_coverage_report(functions, classes)
        coverage = report["coverage"]

        # -------- QUALITY SCORE --------
        if coverage >= 95:
            grade = "A+"
        elif coverage >= 85:
            grade = "A"
        elif coverage >= 70:
            grade = "B"
        else:
            grade = "C"

        overall_results.append((file.name, coverage, grade))

        # -------- FILE DASHBOARD --------
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader(f"📂 {file.name}")

        progress_bar = st.progress(0)
        for i in range(int(coverage)):
            time.sleep(0.003)
            progress_bar.progress(i + 1)

        col1, col2 = st.columns(2)
        col1.metric("Coverage", f"{coverage}%")
        col2.metric("Quality Score", grade)

        with st.expander("🔎 Functions & Classes"):
            for f in functions:
                icon = "✅" if f["has_docstring"] else "❌"
                st.write(f"{icon} Function: **{f['name']}**")
            for c in classes:
                icon = "✅" if c["has_docstring"] else "❌"
                st.write(f"{icon} Class: **{c['name']}**")

        st.markdown("</div>", unsafe_allow_html=True)

        # -------- AUTO INJECTION --------
        if coverage < 100 and auto_inject:

            updated_code = inject_docstrings(source_code, "Google")
            new_functions, new_classes = parse_code(updated_code)
            new_report = generate_coverage_report(new_functions, new_classes)
            new_coverage = new_report["coverage"]

            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.subheader("⚡ Smart Upgrade")

            col1, col2 = st.columns(2)
            col1.metric("Before", f"{coverage}%")
            col2.metric("After", f"{new_coverage}%")

            # -------- ENHANCED DIFF --------
            with st.expander("🔍 Code Differences (Enhanced View)"):

                original_lines = source_code.splitlines()
                updated_lines = updated_code.splitlines()
                diff = list(difflib.ndiff(original_lines, updated_lines))

                added_lines = []
                for line in diff:
                    if line.startswith("+ "):
                        added_lines.append(line[2:])

                st.markdown("### ✨ Injected Docstrings")

                if added_lines:
                    highlighted = ""
                    for line in added_lines:
                        highlighted += f"<div style='background-color:#E6FFED; padding:4px; border-radius:4px; margin-bottom:2px;'>{line}</div>"
                    st.markdown(highlighted, unsafe_allow_html=True)
                else:
                    st.info("No new lines were added.")

                st.markdown("---")
                st.markdown("### 📊 Side-by-Side Comparison")

                colA, colB = st.columns(2)
                with colA:
                    st.markdown("#### Before")
                    st.code(source_code, language="python")
                with colB:
                    st.markdown("#### After")
                    st.code(updated_code, language="python")

            st.download_button(
                "⬇ Download Improved File",
                updated_code,
                file_name=f"{file.name}_improved.py"
            )

            st.markdown("</div>", unsafe_allow_html=True)

    # -------- GLOBAL DASHBOARD --------
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📊 Global Documentation Dashboard")

    total_files = len(overall_results)
    avg_coverage = sum(r[1] for r in overall_results) / total_files

    if avg_coverage >= 95:
        overall_grade = "A+"
    elif avg_coverage >= 85:
        overall_grade = "A"
    elif avg_coverage >= 70:
        overall_grade = "B"
    else:
        overall_grade = "C"

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Files", total_files)
    col2.metric("Average Coverage", f"{avg_coverage:.2f}%")
    col3.metric("Overall Grade", overall_grade)

    file_names = [r[0] for r in overall_results]
    coverages = [r[1] for r in overall_results]

    fig = go.Figure(data=[go.Bar(x=file_names, y=coverages)])
    fig.update_layout(
        title="Coverage Per File",
        xaxis_title="Files",
        yaxis_title="Coverage %",
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -------- PDF EXPORT --------
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📄 Export Coverage Report")

    pdf_bytes = generate_pdf(overall_results)

    st.download_button(
        label="⬇ Download PDF Report",
        data=pdf_bytes,
        file_name="coverage_report.pdf",
        mime="application/pdf"
    )

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Upload one or more Python files from the sidebar to begin.")