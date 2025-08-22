import streamlit as st
from core.scenarios import default_scenario
from ui.cards_income import add_income_card
from ui.cards_debts import add_debt_card
from ui.sidebar_editor import render_context_form

def _setup():
    st.session_state.clear()
    scn = default_scenario()
    st.session_state["scenarios"] = {"Default": scn}
    st.session_state["scenario_name"] = "Default"
    return scn

def test_add_income_card_drawer_renders():
    scn = _setup()
    cid = add_income_card(scn)
    render_context_form(st.session_state["active_editor"], scn, [])
    assert st.session_state["active_editor"] == {"kind": "income", "id": cid}

def test_add_debt_card_drawer_renders():
    scn = _setup()
    cid = add_debt_card(scn)
    render_context_form(st.session_state["active_editor"], scn, [])
    assert st.session_state["active_editor"] == {"kind": "debt", "id": cid}
