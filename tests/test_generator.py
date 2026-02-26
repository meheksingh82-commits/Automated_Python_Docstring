from generator.styled_generator import generate_google_style

def test_generate_docstring_structure():
    func = {"name": "add", "params": ["a", "b"]}
    doc = generate_google_style(func)
    assert "Args:" in doc
