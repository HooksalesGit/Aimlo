"""UI helper utilities."""
import streamlit as st

def show_sidebar():
    st.session_state["drawer_open"] = True

def hide_sidebar():
    st.session_state["drawer_open"] = False

def toggle_sidebar():
    st.session_state["drawer_open"] = not st.session_state.get("drawer_open", False)


def borrower_selectbox(label: str, current_id: int, key: str) -> int:
    """Render a selectbox of borrower names and return selected borrower ID."""
    scn = st.session_state["scenarios"][st.session_state["scenario_name"]]
    borrowers = scn.get("borrowers", {})
    ids = sorted(borrowers)
    def _name(b):
        return f"{b.get('first_name','')} {b.get('last_name','')}".strip() or "Borrower"
    names = [_name(borrowers[bid]) for bid in ids]
    id_map = dict(zip(ids, names))
    current_name = id_map.get(current_id, names[0] if names else "")
    chosen = st.selectbox(label, names, index=names.index(current_name), key=key)
    return next((bid for bid, nm in id_map.items() if nm == chosen), current_id)


def borrower_name(scn: dict, borrower_id: int) -> str:
    """Return formatted borrower full name for the given ID."""
    b = scn.get("borrowers", {}).get(borrower_id, {})
    return f"{b.get('first_name', '')} {b.get('last_name', '')}".strip() or "Borrower"
