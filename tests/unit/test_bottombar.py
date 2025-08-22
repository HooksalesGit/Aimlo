import streamlit as st
from ui.bottombar import render_bottombar


def test_render_bottombar_handles_string_targets():
    st.session_state.clear()
    summary = {"FE": 0.1, "BE": 0.2, "FE_target": "0.31", "BE_target": "0.43"}
    render_bottombar(True, summary)
