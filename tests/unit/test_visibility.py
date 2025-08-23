import streamlit as st
from ui.utils import show_sidebar, hide_sidebar

def test_sidebar_toggle():
    st.session_state.clear()
    show_sidebar()
    assert st.session_state["drawer_open"] is True
    hide_sidebar()
    assert st.session_state["drawer_open"] is False

