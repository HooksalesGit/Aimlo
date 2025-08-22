import streamlit as st

"""Income cards board and helpers."""
import streamlit as st
import uuid


def add_income_card(scn, typ="W-2"):
    cid = uuid.uuid4().hex[:8]
    scn.setdefault("income_cards", []).append({"id": cid, "type": typ, "payload": {}})
    st.session_state["active_editor"] = {"kind": "income", "id": cid}
    st.session_state["drawer_open"] = True
    return cid

def select_income_card(card_id):
    st.session_state["active_editor"] = {"kind": "income", "id": card_id}
    st.session_state["drawer_open"] = True


def render_income_board(scn):
    st.subheader("All Income")
    if st.button("Add income card"):
        add_income_card(scn)
    for card in scn.get("income_cards", []):
        label = card.get("type", "Income")
        if st.button(f"{label}", key=f"inc_{card['id']}"):
            select_income_card(card["id"])
