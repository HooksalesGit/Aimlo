import streamlit as st
from core.scenarios import default_scenario
from ui.utils import borrower_selectbox


def test_borrower_selectbox(monkeypatch):
    st.session_state.clear()
    scn = default_scenario()
    st.session_state["scenarios"] = {"Default": scn}
    st.session_state["scenario_name"] = "Default"

    def fake_selectbox(label, options, index=0, key=None):
        assert label == "Borrower"
        return options[1]

    monkeypatch.setattr(st, "selectbox", fake_selectbox)
    selected_id = borrower_selectbox("Borrower", 1, key="test")
    assert selected_id == 2
