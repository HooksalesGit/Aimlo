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
        card_id = card["id"]
        open_key = f"inc_open_{card_id}"
        dup_key = f"inc_dup_{card_id}"
        rm_key = f"inc_rm_{card_id}"
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([0.55, 0.25, 0.1, 0.1])
            with c1:
                st.write(f"{card.get('type', '')}: {employer}")
                st.caption(name)
            with c2:
                st.write(f"${monthly:,.2f}/mo")
            with c3:
                if st.button("📄", key=dup_key, help="Duplicate"):
                    duplicate_income_card(scn, card)
                    st.rerun()
            with c4:
                if st.button("🗑️", key=rm_key, help="Remove"):
                    remove_income_card(scn, card_id)
                    st.rerun()
            if st.button(" ", key=open_key, label_visibility="collapsed"):
                select_income_card(card_id)
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
