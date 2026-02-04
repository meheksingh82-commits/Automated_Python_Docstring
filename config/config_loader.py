import tomllib
from pathlib import Path


DEFAULT_CONFIG = {
    "validation_mode": "strict",
    "min_coverage": 80,
    "inject_docstrings": False,
    "docstring_style": "google"
}


def load_config():
    """Function load_config."""
    config_path = Path("pyproject.toml")

    if not config_path.exists():
        return DEFAULT_CONFIG

    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    return data.get("tool", {}).get("docstring_analyzer", DEFAULT_CONFIG)