"""Income cards board and helpers."""
import streamlit as st
import uuid
import copy
from core.calculators import (
    w2_row_to_monthly,
    schc_rows_to_monthly,
    k1_rows_to_monthly,
    c1120_rows_to_monthly,
    rentals_schedule_e_monthly,
    rentals_75pct_gross_monthly,
    other_income_rows_to_monthly,
)
from ui.utils import borrower_name


def add_income_card(scn, typ="W-2"):
    cid = uuid.uuid4().hex[:8]
    scn.setdefault("income_cards", []).append({"id": cid, "type": typ, "payload": {}})
    st.session_state["active_editor"] = {"kind": "income", "id": cid}
    return cid


def select_income_card(card_id):
    st.session_state["active_editor"] = {"kind": "income", "id": card_id}


def income_monthly(card: dict) -> float:
    t = card.get("type")
    p = card.get("payload", {})
    if t == "W-2":
        return w2_row_to_monthly(p)
    if t == "Schedule C":
        return schc_rows_to_monthly([p])
    if t == "K-1":
        return k1_rows_to_monthly([p])
    if t == "1120":
        return c1120_rows_to_monthly([p])
    if t == "Rental":
        if p.get("method") == "Schedule E":
            return rentals_schedule_e_monthly(p.get("lines", []))
        return rentals_75pct_gross_monthly(p.get("gross_rents_annual", 0.0)) + (
            0.75 * float(p.get("subject_market_rent", 0.0)) - float(p.get("subject_pitia", 0.0))
        )
    if t == "Other":
        return other_income_rows_to_monthly([p])
    return 0.0


def duplicate_income_card(scn, card: dict) -> str:
    """Duplicate an income card and return new card ID."""
    new_card = copy.deepcopy(card)
    new_card["id"] = uuid.uuid4().hex[:8]
    scn.setdefault("income_cards", []).append(new_card)
    st.session_state["active_editor"] = {"kind": "income", "id": new_card["id"]}
    return new_card["id"]


def remove_income_card(scn, card_id: str) -> None:
    """Remove an income card by ID."""
    scn["income_cards"] = [c for c in scn.get("income_cards", []) if c["id"] != card_id]
    if st.session_state.get("active_editor") == {"kind": "income", "id": card_id}:
        st.session_state["active_editor"] = None


def render_income_board(scn):
    st.subheader("All Income")
    if st.button("Add income card"):
        st.session_state["active_editor"] = {"kind": "income_new"}
    for card in scn.get("income_cards", []):
        p = card.get("payload", {})
        name = borrower_name(scn, int(p.get("borrower_id", 1)))
        employer = (
            p.get("employer")
            or p.get("business_name")
            or p.get("entity_name")
            or p.get("corp_name")
            or ""
        )
        monthly = income_monthly(card)
        with st.container(border=True):
            summary = (
                f"Borrower: {name}\n"
                f"Type: {card.get('type', '')}\n"
                f"Employer: {employer}\n"
                f"Monthly: ${monthly:,.2f}"
            )
            if st.button(summary, key=f"inc_sel_{card['id']}", use_container_width=True):
                select_income_card(card["id"])
            c1, c2 = st.columns(2)
            if c1.button("📄", key=f"inc_dup_{card['id']}", help="Duplicate"):
                duplicate_income_card(scn, card)
                st.rerun()
            if c2.button("🗑️", key=f"inc_rm_{card['id']}", help="Remove"):
                remove_income_card(scn, card["id"])
                st.rerun()
