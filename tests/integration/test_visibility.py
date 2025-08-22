import streamlit as st
from ui.utils import show_sidebar, hide_sidebar, show_bottombar, hide_bottombar

def test_visibility_sequence():
    st.session_state.clear()
    show_sidebar()
    show_bottombar()
    assert st.session_state["sidebar_visible"]
    assert st.session_state["bottombar_visible"]
    hide_sidebar()
    hide_bottombar()
    assert not st.session_state["sidebar_visible"]
    assert not st.session_state["bottombar_visible"]
