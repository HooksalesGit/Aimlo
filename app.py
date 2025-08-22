import streamlit as st
from ui.topbar import render_topbar
from ui.layout import render_layout
from ui.sidebar_editor import render_drawer
from ui.bottombar import render_bottombar
from ui.utils import show_bottombar
from core.scenarios import default_scenario
from core.calculators import (
    piti_components,
    dti,
    debts_monthly_total,
    w2_row_to_monthly,
    schc_rows_to_monthly,
    k1_rows_to_monthly,
    c1120_rows_to_monthly,
    rentals_schedule_e_monthly,
    rentals_75pct_gross_monthly,
    other_income_rows_to_monthly,
)

st.set_page_config(page_title="Aimlo", layout="wide")
if "scenarios" not in st.session_state:
    st.session_state["scenarios"] = {"Default": default_scenario()}
    st.session_state["scenario_name"] = "Default"
st.session_state.setdefault("drawer_open", False)
st.session_state.setdefault("active_editor", None)
st.session_state.setdefault("bottombar_visible", False)

render_topbar()
scn = st.session_state["scenarios"][st.session_state["scenario_name"]]
render_layout(scn)

# Compute totals for bottom bar
h = scn["housing"]
comp = piti_components(
    h.get("purchase_price", 0),
    h.get("down_payment_amt", 0),
    h.get("rate_pct", 0),
    h.get("term_years", 0),
    h.get("tax_rate_pct", 0),
    h.get("hoi_annual", 0),
    h.get("hoa_monthly", 0),
    h.get("program", "Conventional"),
    h.get("finance_upfront", False),
)

total_income = 0.0
for c in scn.get("income_cards", []):
    t = c.get("type")
    p = c.get("payload", {})
    if t == "W-2":
        total_income += w2_row_to_monthly(p)
    elif t == "Schedule C":
        total_income += schc_rows_to_monthly([p])
    elif t == "K-1":
        total_income += k1_rows_to_monthly([p])
    elif t == "1120":
        total_income += c1120_rows_to_monthly([p])
    elif t == "Rental":
        if p.get("method") == "Schedule E":
            total_income += rentals_schedule_e_monthly(p.get("lines", []))
        else:
            total_income += rentals_75pct_gross_monthly(p.get("gross_rents_annual", 0.0))
            total_income += 0.75 * float(p.get("subject_market_rent", 0.0)) - float(p.get("subject_pitia", 0.0))
    elif t == "Other":
        total_income += other_income_rows_to_monthly([p])
policy = scn.get("settings", {}).get("student_loan_policy", "Conventional")
other_debts = debts_monthly_total(scn.get("debt_cards", []), policy)
FE, BE = dti(comp["PITIA"], other_debts, total_income)
summary = {
    "TotalIncome": total_income,
    "PITIA": comp["PITIA"],
    "OtherDebts": other_debts,
    "FE": FE,
    "BE": BE,
    "FE_target": st.session_state.get("fe_target", 0.31),
    "BE_target": st.session_state.get("be_target", 0.43),
}
render_bottombar(st.session_state["bottombar_visible"], summary)
if not st.session_state["bottombar_visible"]:
    if st.button("\u25b2", key="bottombar_show"):
        show_bottombar()
        st.experimental_rerun()

# Render drawer last
render_drawer(scn)
