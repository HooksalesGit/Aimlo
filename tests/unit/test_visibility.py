import streamlit as st
from ui.utils import show_sidebar, hide_sidebar, show_bottombar, hide_bottombar

def test_sidebar_toggle():
    st.session_state.clear()
    show_sidebar()
    assert st.session_state["drawer_open"] is True
    hide_sidebar()
    assert st.session_state["drawer_open"] is False

def test_bottombar_toggle():
    st.session_state.clear()
    show_bottombar()
    assert st.session_state["bottombar_visible"] is True
    hide_bottombar()
    assert st.session_state["bottombar_visible"] is False
