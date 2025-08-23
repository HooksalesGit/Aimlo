import streamlit as st
from ui.utils import show_sidebar, hide_sidebar, toggle_sidebar

def test_visibility_sequence():
    st.session_state.clear()
    show_sidebar()
    assert st.session_state["drawer_open"]
    toggle_sidebar()
    assert not st.session_state["drawer_open"]
    toggle_sidebar()
    assert st.session_state["drawer_open"]
    hide_sidebar()
    assert not st.session_state["drawer_open"]
