"""UI helper utilities."""
import streamlit as st

def show_sidebar():
    st.session_state["sidebar_visible"] = True

def hide_sidebar():
    st.session_state["sidebar_visible"] = False

def show_bottombar():
    st.session_state["bottombar_visible"] = True

def hide_bottombar():
    st.session_state["bottombar_visible"] = False


def borrower_selectbox(label: str, current_id: int, key: str) -> int:
    """Render a selectbox of borrower names and return selected borrower ID."""
    scn = st.session_state["scenarios"][st.session_state["scenario_name"]]
    borrowers = scn.get("borrowers", {})
    names = [borrowers[b] for b in sorted(borrowers)]
    current_name = borrowers.get(current_id, names[0] if names else "")
    chosen = st.selectbox(label, names, index=names.index(current_name), key=key)
    return next((bid for bid, nm in borrowers.items() if nm == chosen), current_id)
