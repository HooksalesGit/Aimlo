"""Income cards board and helpers."""
import streamlit as st
import uuid
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


def render_income_board(scn):
    st.subheader("All Income")
    if st.button("Add income card"):
        add_income_card(scn)
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
            st.markdown(f"**Borrower:** {name}")
            st.markdown(f"**Type:** {card.get('type', '')}")
            st.markdown(f"**Employer:** {employer}")
            st.markdown(f"**Monthly:** ${monthly:,.2f}")
            if st.button("Edit", key=f"inc_{card['id']}"):
                select_income_card(card["id"])
