import streamlit as st
from ui.layout import render_layout
from ui.utils import show_bottombar, hide_bottombar


def test_layout_smoke():
    st.session_state.clear()
    scn = {"income_cards": [], "debt_cards": [], "housing": {}}
    render_layout(scn)
    show_bottombar()
    assert st.session_state["bottombar_visible"] is True
    hide_bottombar()
    assert st.session_state["bottombar_visible"] is False
