import streamlit as st
from ui.cards_income import render_income_board
from ui.cards_debts import render_debt_board
from ui.panel_property import render_property_panel
from ui.disclosures import render_disclosures


def render_layout(scn):
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        st.subheader("Data entry")
        st.info("Select an item to edit from the main panel.")
        st.subheader("Disclosures")
        render_disclosures(warnings=[])
    with col_b:
        render_income_board(scn)
    with col_c:
        render_debt_board(scn)
        render_property_panel(scn)
