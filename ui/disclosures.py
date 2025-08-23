"""Disclosures component used within the drawer."""
import streamlit as st
from core.presets import DISCLAIMER


def render_disclosures(warnings):
    """Render only the disclosures and warnings tabs."""
    disc_tab, guides_tab, warn_tab, where_tab = st.tabs(
        ["Disclosures", "Guides", "Warnings", "Where to find"]
    )
    with disc_tab:
        st.caption(DISCLAIMER)
    with guides_tab:
        st.info("No guides available.")
    with warn_tab:
        if not warnings:
            st.info("No warnings currently.")
        else:
            for w in warnings:
                st.warning(w)
    with where_tab:
        st.info("No field sources available.")
