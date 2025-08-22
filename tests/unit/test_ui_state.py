import streamlit as st
from ui.utils import show_sidebar, hide_sidebar


def test_drawer_state():
    st.session_state.clear()
    show_sidebar()
    assert st.session_state.get("drawer_open") is True
    hide_sidebar()
    assert st.session_state.get("drawer_open") is False


def test_active_editor_mutations():
    st.session_state.clear()
    st.session_state["active_editor"] = None
    st.session_state["active_editor"] = {"kind": "w2", "id": "1"}
    assert st.session_state["active_editor"]["kind"] == "w2"
    st.session_state["active_editor"] = None
    assert st.session_state["active_editor"] is None
