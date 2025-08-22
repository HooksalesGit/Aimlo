import streamlit as st
from ui.cards_income import add_income_card, select_income_card
from ui.cards_debts import add_debt_card, select_debt_card


def test_income_card_add_sets_active():
    st.session_state.clear()
    scn = {"income_cards": []}
    cid = add_income_card(scn)
    assert st.session_state["active_editor"] == {"kind": "income", "id": cid}
    assert st.session_state["drawer_open"] is True


def test_select_income_card_sets_active():
    st.session_state.clear()
    select_income_card("xyz")
    assert st.session_state["active_editor"] == {"kind": "income", "id": "xyz"}
    assert st.session_state["drawer_open"] is True


def test_add_debt_card_sets_active():
    st.session_state.clear()
    scn = {"debt_cards": []}
    cid = add_debt_card(scn)
    assert st.session_state["active_editor"] == {"kind": "debt", "id": cid}
    assert st.session_state["drawer_open"] is True


def test_select_debt_card_sets_active():
    st.session_state.clear()
    scn = {"debt_cards": [{"id": "abc", "type": "installment", "name": "", "monthly_payment": 0.0}]}
    select_debt_card("abc")
    assert st.session_state["active_editor"] == {"kind": "debt", "id": "abc"}
    assert st.session_state["drawer_open"] is True
