from pathlib import Path


def test_no_experimental_rerun():
    """Ensure deprecated Streamlit rerun API is absent."""
    assert "experimental_rerun" not in Path("app.py").read_text()

