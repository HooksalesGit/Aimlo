"""Disclosures component reused across layout and drawer."""
import streamlit as st
import yaml
from pathlib import Path
from core.presets import DISCLAIMER

_HINTS_CACHE = None

def _load_hints():
    global _HINTS_CACHE
    if _HINTS_CACHE is None:
        with open(Path("docs") / "field_hints.yml", "r", encoding="utf-8") as f:
            _HINTS_CACHE = yaml.safe_load(f) or {}
    return _HINTS_CACHE

def render_disclosures(warnings):
    hints = _load_hints()
    disc_tab, guides_tab, warn_tab, where_tab = st.tabs([
        "Disclosures",
        "Guides",
        "Warnings",
        "Where to find",
    ])
    with disc_tab:
        st.caption(DISCLAIMER)
    with guides_tab:
        if not hints:
            st.info("No guides available.")
        else:
            for key, meta in hints.items():
                st.write(f"**{meta.get('label', key)}**: {meta.get('definition', '')}")
    with warn_tab:
        if not warnings:
            st.info("No warnings currently.")
        else:
            for w in warnings:
                st.warning(w)
    with where_tab:
        if not hints:
            st.info("No field sources available.")
        else:
            for key, meta in hints.items():
                st.write(f"**{meta.get('label', key)}**: {meta.get('where', '')}")
