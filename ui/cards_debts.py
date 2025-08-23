"""Debt cards board and helpers."""
import streamlit as st
import uuid
import copy
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


def duplicate_debt_card(scn, card: dict) -> str:
    """Duplicate a debt card and return new card ID."""
    new_card = copy.deepcopy(card)
    new_card["id"] = uuid.uuid4().hex[:8]
    scn.setdefault("debt_cards", []).append(new_card)
    st.session_state["active_editor"] = {"kind": "debt", "id": new_card["id"]}
    return new_card["id"]


def remove_debt_card(scn, card_id: str) -> None:
    """Remove a debt card by ID."""
    scn["debt_cards"] = [c for c in scn.get("debt_cards", []) if c["id"] != card_id]
    if st.session_state.get("active_editor") == {"kind": "debt", "id": card_id}:
        st.session_state["active_editor"] = None


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
            c1, c2, c3 = st.columns(3)
            if c1.button("Edit", key=f"deb_edit_{card['id']}"):
                select_debt_card(card["id"])
            if c2.button("Duplicate", key=f"deb_dup_{card['id']}"):
                duplicate_debt_card(scn, card)
                st.rerun()
            if c3.button("Remove", key=f"deb_rm_{card['id']}"):
                remove_debt_card(scn, card["id"])
                st.rerun()
