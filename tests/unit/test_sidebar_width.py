import streamlit as st
from ui import sidebar_editor


def test_sidebar_width_css(monkeypatch):
    # Capture markdown calls to inspect applied CSS
    calls = []

    def fake_markdown(body, *args, **kwargs):
        calls.append(body)

    monkeypatch.setattr(st, "markdown", fake_markdown)
    # Avoid rendering the full context form
    monkeypatch.setattr(sidebar_editor, "render_context_form", lambda *a, **k: None)

    class DummySidebar:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(st, "sidebar", DummySidebar())

    sidebar_editor.render_drawer({}, warnings=[])

    assert any("width:1200px" in c for c in calls)
