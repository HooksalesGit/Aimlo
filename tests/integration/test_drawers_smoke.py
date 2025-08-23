import streamlit as st
from ui.utils import show_sidebar, hide_sidebar


def test_drawers_smoke():
    st.session_state.clear()

    st.session_state.setdefault("drawer_open", True)
    assert st.session_state["drawer_open"] is True
    show_sidebar()

    assert st.session_state["drawer_open"] is True
    hide_sidebar()
    assert st.session_state["drawer_open"] is False
    show_sidebar()
    assert st.session_state["drawer_open"] is True
