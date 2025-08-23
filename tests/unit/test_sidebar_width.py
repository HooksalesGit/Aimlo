import streamlit as st
import ui.sidebar_editor as sidebar_editor
from ui.layout_helpers import SIDEBAR_WIDTH


def test_sidebar_drawer_width(monkeypatch):
    captured = {}

    def fake_markdown(html, unsafe_allow_html=False):
        captured['html'] = html

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

    width = SIDEBAR_WIDTH * 2
    assert "section[data-testid='stSidebar']" in captured['html']
    assert f"width:{width}px" in captured['html']
    assert f"max-width:{width}px" in captured['html']
