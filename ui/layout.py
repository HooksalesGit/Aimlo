import streamlit as st
from ui.cards_income import render_income_board
from ui.cards_debts import render_debt_board
from ui.panel_property import render_property_panel


def render_layout(scn):
    """Render the main boards for income, debts, and property."""

    render_property_panel(scn)
    col_inc, col_deb = st.columns(2)
    with col_inc:
        render_income_board(scn)
    with col_deb:
        render_debt_board(scn)

