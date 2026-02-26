from analyzer.parser import parse_code

def test_parse_function():
    source = "def add(a, b): return a + b"
    functions, classes = parse_code(source)
    assert len(functions) == 1
