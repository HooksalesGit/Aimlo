import streamlit as st
from ui.utils import show_sidebar, hide_sidebar, show_bottombar, hide_bottombar


def test_drawers_smoke():
    st.session_state.clear()

    st.session_state.setdefault("drawer_open", True)
    assert st.session_state["drawer_open"] is True
    assert st.session_state.get("bottombar_visible", False) is False
    show_sidebar()
    show_bottombar()

    assert st.session_state["drawer_open"] is True
    assert st.session_state["bottombar_visible"] is True
    hide_sidebar()
    hide_bottombar()
    assert st.session_state["drawer_open"] is False
    assert st.session_state["bottombar_visible"] is False
    show_sidebar()
    show_bottombar()
    assert st.session_state["drawer_open"] is True
    assert st.session_state["bottombar_visible"] is True
