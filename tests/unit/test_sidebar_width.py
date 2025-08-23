import streamlit as st
import ui.sidebar_editor as sidebar_editor
from ui.layout_helpers import SIDEBAR_WIDTH


def test_sidebar_drawer_width(monkeypatch):
    captured = []

    def fake_markdown(html, unsafe_allow_html=False):
        captured.append(html)

    monkeypatch.setattr(st, 'markdown', fake_markdown)

    class DummySidebar:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(st, 'sidebar', DummySidebar())
    monkeypatch.setattr(sidebar_editor, 'render_context_form', lambda *a, **k: None)
    st.session_state.clear()
    sidebar_editor.render_drawer({})

    combined = "".join(captured)
    width_css = f"min(90vw, {SIDEBAR_WIDTH}px)"
    assert "section[data-testid='stSidebar']" in combined
    assert width_css in combined


def test_sidebar_hidden(monkeypatch):
    captured = []

    def fake_markdown(html, unsafe_allow_html=False):
        captured.append(html)

    monkeypatch.setattr(st, 'markdown', fake_markdown)

    class DummySidebar:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(st, 'sidebar', DummySidebar())
    monkeypatch.setattr(sidebar_editor, 'render_context_form', lambda *a, **k: None)
    st.session_state.clear()
    st.session_state['drawer_open'] = False
    sidebar_editor.render_drawer({})

    combined = "".join(captured)
    assert 'display:none' in combined
    assert 'collapsedControl' in combined
    assert 'stAppViewContainer' in combined and 'margin-left:0' in combined
