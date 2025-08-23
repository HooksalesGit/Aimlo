import streamlit as st
from ui.cards_income import (
    add_income_card,
    select_income_card,
    render_income_board,
    duplicate_income_card,
    remove_income_card,
)
from ui.cards_debts import (
    add_debt_card,
    select_debt_card,
    duplicate_debt_card,
    remove_debt_card,
)


def test_income_card_add_sets_active():
    st.session_state.clear()
    scn = {"income_cards": []}
    cid = add_income_card(scn)
    assert st.session_state["active_editor"] == {"kind": "income", "id": cid}


def test_select_income_card_sets_active():
    st.session_state.clear()
    select_income_card("xyz")
    assert st.session_state["active_editor"] == {"kind": "income", "id": "xyz"}


def test_add_debt_card_sets_active():
    st.session_state.clear()
    scn = {"debt_cards": []}
    cid = add_debt_card(scn)
    assert st.session_state["active_editor"] == {"kind": "debt", "id": cid}


def test_select_debt_card_sets_active():
    st.session_state.clear()
    scn = {"debt_cards": [{"id": "abc", "type": "installment", "name": "", "monthly_payment": 0.0}]}
    select_debt_card("abc")
    assert st.session_state["active_editor"] == {"kind": "debt", "id": "abc"}


def test_render_income_board_sets_new(monkeypatch):
    st.session_state.clear()
    scn = {"income_cards": []}
    monkeypatch.setattr(st, "button", lambda label, **kwargs: True)
    render_income_board(scn)
    assert st.session_state["active_editor"] == {"kind": "income_new"}


def test_render_income_board_no_extra_kwargs(monkeypatch):
    """Ensure render_income_board uses only supported st.button parameters."""
    st.session_state.clear()
    scn = {"income_cards": []}

    def strict_button(label, key=None, help=None, on_click=None, args=None, kwargs=None, type="secondary", disabled=False, use_container_width=False):
        """A stub mimicking st.button without **kwargs to surface unexpected params."""
        return False

    monkeypatch.setattr(st, "button", strict_button)
    render_income_board(scn)


def test_duplicate_and_remove_income_cards():
    st.session_state.clear()
    card = {"id": "a", "type": "W-2", "payload": {}}
    scn = {"income_cards": [card]}
    new_id = duplicate_income_card(scn, card)
    assert len(scn["income_cards"]) == 2
    assert new_id != "a"
    remove_income_card(scn, "a")
    assert all(c["id"] != "a" for c in scn["income_cards"])


def test_duplicate_and_remove_debt_cards():
    st.session_state.clear()
    card = {"id": "a", "borrower_id": 1, "type": "installment", "name": "", "monthly_payment": 0.0}
    scn = {"debt_cards": [card]}
    new_id = duplicate_debt_card(scn, card)
    assert len(scn["debt_cards"]) == 2
    assert new_id != "a"
    remove_debt_card(scn, "a")
    assert all(c["id"] != "a" for c in scn["debt_cards"])
