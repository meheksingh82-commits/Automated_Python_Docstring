# Automated Python Docstring Generator

This project analyzes Python files, measures documentation coverage,
and automatically injects Google-style docstrings if missing.

---

## Installation

1. Clone the repository:

git clone <repository-url>
cd Internship

2. Create virtual environment (recommended):

python -m venv venv
venv\Scripts\activate

3. Install in editable mode:

pip install -e .

---

## CLI Usage

Run:

docgen

This performs documentation coverage analysis.

---

## Run Streamlit UI

streamlit run ui/app.py

Features:
- Upload Python files
- View documentation coverage
- Auto inject missing docstrings
- Download improved file
- Export PDF report

---

## Run Tests

pytest

All tests should pass before submission.

---

## Project Structure

Internship/
│
├── src/
├── tests/
├── ui/
├── pyproject.toml
├── README.md
└── LICENSE

---

## License

MIT License