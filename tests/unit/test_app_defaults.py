import streamlit as st
from core.scenarios import default_scenario


def test_app_defaults_open_sidebar():
    st.session_state.clear()
    if "scenarios" not in st.session_state:
        st.session_state["scenarios"] = {"Default": default_scenario()}
        st.session_state["scenario_name"] = "Default"
    st.session_state.setdefault("drawer_open", True)
    st.session_state.setdefault("active_editor", {"kind": "income_board"})
    assert st.session_state["drawer_open"] is True
    assert st.session_state["active_editor"] == {"kind": "income_board"}

