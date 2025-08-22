"""Debt cards board and helpers."""
import streamlit as st
import uuid


def add_debt_card(scn, typ="installment"):
    cid = uuid.uuid4().hex[:8]
    scn.setdefault("debt_cards", []).append({"id": cid, "type": typ, "name": "", "monthly_payment": 0.0})
    st.session_state["active_editor"] = {"kind": "debt", "id": cid}
    st.session_state["drawer_open"] = True
    return cid


def select_debt_card(card_id):
    st.session_state["active_editor"] = {"kind": "debt", "id": card_id}
    st.session_state["drawer_open"] = True


def render_debt_board(scn):
    st.subheader("All Debts/Liabilities")
    if st.button("Add debt card"):
        add_debt_card(scn)
    for card in scn.get("debt_cards", []):
        label = card.get("name") or card.get("type", "Debt")
        if st.button(f"{label}", key=f"deb_{card['id']}"):
            select_debt_card(card["id"])
