import streamlit as st
from ui.cards_income import render_income_board
from ui.cards_debts import render_debt_board
from ui.panel_property import render_property_panel


def render_layout(scn):
    """Main three-column layout with income, debts, and property boxes."""
    col_income, col_debts, col_prop = st.columns([1, 1, 1])
    with col_income:
        render_income_board(scn)
    with col_debts:
        render_debt_board(scn)
    with col_prop:
        render_property_panel(scn)
