import streamlit as st
from ui.summary_band import render_summary_band


def sample_summary():
    return {
        "TotalIncome": 5000.0,
        "PITIA": 1500.0,
        "FE": 0.3,
        "BE": 0.4,
        "LTV": 80.0,
        "FE_target": 0.31,
        "BE_target": 0.43,
        "Taxes": 200.0,
        "HOI": 100.0,
        "HOA": 50.0,
        "MI_MIP": 0.0,
        "PI": 1150.0,
        "AdjustedLoan": 200000.0,
        "Rate": 5.0,
        "Term": 30,
        "OtherDebts": 300.0,
        "DownPaymentPct": 0.2,
    }


def test_summary_band_toggle_and_kpis():
    st.session_state.clear()
    label = render_summary_band(sample_summary())
    assert "Total Income" in label
    assert "PITIA" in label
    assert st.session_state["summary_expanded"] is False

    st.session_state["summary_expanded"] = True
    label2 = render_summary_band(sample_summary())
    assert st.session_state["summary_expanded"] is True
    assert "Total Income" in label2

