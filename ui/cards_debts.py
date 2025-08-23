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
        card_id = card["id"]
        open_key = f"deb_open_{card_id}"
        dup_key = f"deb_dup_{card_id}"
        rm_key = f"deb_rm_{card_id}"
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([0.55, 0.25, 0.1, 0.1])
            with c1:
                st.write(f"{card.get('type', '')}: {card.get('name', '')}")
                st.caption(name)
            with c2:
                st.write(f"${monthly:,.2f}/mo")
            with c3:
                if st.button("📄", key=dup_key, help="Duplicate"):
                    duplicate_debt_card(scn, card)
                    st.rerun()
            with c4:
                if st.button("🗑️", key=rm_key, help="Remove"):
                    remove_debt_card(scn, card_id)
                    st.rerun()
            if st.button(" ", key=open_key, label_visibility="collapsed"):
                select_debt_card(card_id)
            st.markdown(
                f"""
                <style>
                button#{open_key} {{
                    position: absolute;
                    top: 0; left: 0; width: 100%; height: 100%;
                    border: none; background: none; padding: 0;
                    cursor: pointer; z-index: 0;
                }}
                button#{dup_key}, button#{rm_key} {{
                    position: relative; z-index: 1;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )
