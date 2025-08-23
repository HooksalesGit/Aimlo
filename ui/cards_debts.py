"""Debt cards board and helpers."""
import streamlit as st
import uuid
from core.calculators import student_loan_payment
from ui.utils import borrower_name


def add_debt_card(scn, typ="installment"):
    cid = uuid.uuid4().hex[:8]
    scn.setdefault("debt_cards", []).append(
        {"id": cid, "borrower_id": 1, "type": typ, "name": "", "monthly_payment": 0.0}
    )
    st.session_state["active_editor"] = {"kind": "debt", "id": cid}
    return cid


def select_debt_card(card_id):
    st.session_state["active_editor"] = {"kind": "debt", "id": card_id}


def debt_monthly(card: dict, policy: str) -> float:
    if card.get("type") == "student_loan":
        return student_loan_payment(
            policy,
            card.get("sl_balance", 0.0),
            card.get("sl_documented_payment", 0.0),
            bool(card.get("sl_amortizing", False)),
        )
    return float(card.get("monthly_payment", 0.0))


def render_debt_board(scn):
    st.subheader("All Debts/Liabilities")
    if st.button("Add debt card"):
        add_debt_card(scn)
    policy = scn.get("settings", {}).get("student_loan_policy", "Conventional")
    for card in scn.get("debt_cards", []):
        name = borrower_name(scn, int(card.get("borrower_id", 1)))
        monthly = debt_monthly(card, policy)
        with st.container(border=True):
            st.markdown(f"**Borrower:** {name}")
            st.markdown(f"**Type:** {card.get('type', '')}")
            st.markdown(f"**Title:** {card.get('name', '')}")
            st.markdown(f"**Monthly:** ${monthly:,.2f}")
            if st.button("Edit", key=f"deb_{card['id']}"):
                select_debt_card(card["id"])
