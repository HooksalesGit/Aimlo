import streamlit as st
from contextlib import nullcontext
from ui import sidebar_editor


def test_sidebar_opens_when_editor_active(monkeypatch):
    st.session_state.clear()
    st.session_state["drawer_open"] = False
    st.session_state["active_editor"] = {"kind": "income", "id": "1"}

    monkeypatch.setattr(st, "sidebar", nullcontext())
    monkeypatch.setattr(sidebar_editor, "render_context_form", lambda active, scn, warnings: None)
    monkeypatch.setattr(st, "markdown", lambda *args, **kwargs: None)

    sidebar_editor.render_drawer({})
    assert st.session_state["drawer_open"] is True
