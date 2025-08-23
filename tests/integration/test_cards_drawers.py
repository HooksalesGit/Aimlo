import streamlit as st
from core.scenarios import default_scenario
from ui.cards_income import add_income_card, select_income_card
from ui.cards_debts import add_debt_card, select_debt_card
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

def test_select_existing_cards():
    scn = _setup()
    inc_id = add_income_card(scn)
    deb_id = add_debt_card(scn)
    # reset active_editor
    st.session_state["active_editor"] = None
    select_income_card(inc_id)
    assert st.session_state["active_editor"] == {"kind": "income", "id": inc_id}
    select_debt_card(deb_id)
    assert st.session_state["active_editor"] == {"kind": "debt", "id": deb_id}


def test_create_non_w2_income_from_selector(monkeypatch):
    scn = _setup()
    st.session_state["active_editor"] = {"kind": "income_new"}
    st.session_state["new_income_typ"] = "K-1"
    monkeypatch.setattr(st, "button", lambda label, **kwargs: True if label == "Create income card" else False)
    monkeypatch.setattr(st, "selectbox", lambda label, options, key=None, **kwargs: st.session_state.get(key, options[0]))
    monkeypatch.setattr(st, "rerun", lambda: None)
    render_context_form(st.session_state["active_editor"], scn, [])
    assert scn["income_cards"] and scn["income_cards"][0]["type"] == "K-1"
    new_id = scn["income_cards"][0]["id"]
    assert st.session_state["active_editor"] == {"kind": "income", "id": new_id}
