import streamlit as st, json, tempfile, os
from ui.topbar import render_topbar
from ui.layout import render_income_column, render_debt_column, render_property_snapshot
from ui.sidebar_editor import render_sidebar
from ui.bottombar import render_bottombar
from ui.tabs_dashboard import render_dashboard
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
from core.presets import DISCLAIMER
st.set_page_config(page_title="AMALO v2", layout="wide")
if "scenarios" not in st.session_state:
    st.session_state["scenarios"]={"Default": default_scenario()}
    st.session_state["scenario_name"]="Default"
st.session_state.setdefault("selected", {"kind":None,"id":None})
st.session_state.setdefault("sidebar_visible", True)
st.session_state.setdefault("bottombar_visible", True)
st.session_state.setdefault("view_mode","Data Entry")
render_topbar()
left, main, right = st.columns([2,5,3], gap="medium")
scn = st.session_state["scenarios"][st.session_state["scenario_name"]]
with left:
    st.subheader("Data entry")
    from ui.sidebar_editor import render_sidebar as _render_sidebar
    _render_sidebar(st.session_state.get("selected"), scn, warnings=[])
with main:
    render_income_column(scn)
    render_debt_column(scn)
with right:
    render_property_snapshot(scn)
# Compute totals
h=scn["housing"]
comp=piti_components(h["purchase_price"],h["down_payment_amt"],h["rate_pct"],h["term_years"],h["tax_rate_pct"],h["hoi_annual"],h["hoa_monthly"],h["program"],h["finance_upfront"])
total_income=0.0
for c in scn["income_cards"]:
    t=c.get("type"); p=c.get("payload",{})
    if t=="W-2": total_income+=w2_row_to_monthly(p)
    elif t=="Schedule C": total_income+=schc_rows_to_monthly([p])
    elif t=="K-1": total_income+=k1_rows_to_monthly([p])
    elif t=="1120": total_income+=c1120_rows_to_monthly([p])
    elif t=="Rental":
        if p.get("method")=="Schedule E": total_income+=rentals_schedule_e_monthly(p.get("lines",[]))
        else: total_income+=rentals_75pct_gross_monthly(p.get("gross_rents_annual",0.0)); total_income += 0.75*float(p.get("subject_market_rent",0.0)) - float(p.get("subject_pitia",0.0))
    elif t=="Other": total_income+=other_income_rows_to_monthly([p])
policy = scn.get("settings",{}).get("student_loan_policy","Conventional")
other_debts = debts_monthly_total(scn["debt_cards"], policy)
FE,BE=dti(comp["PITIA"], other_debts, total_income)
summary={"TotalIncome":total_income,"PITIA":comp["PITIA"],"OtherDebts":other_debts,"FE":FE,"BE":BE,"FE_target":st.session_state.get("fe_target",0.31),"BE_target":st.session_state.get("be_target",0.43)}
render_bottombar(st.session_state["bottombar_visible"], summary)
st.write("---")
if st.button("Open Dashboard"):
    flags={"k1_gate_ok": all((p.get("payload",{}).get("verified_distributions") or p.get("payload",{}).get("analyzed_liquidity")) for p in scn["income_cards"] if p.get("type")=="K-1") if any(p.get("type")=="K-1" for p in scn["income_cards"]) else True,
           "c1120_all_100pct": all(p.get("payload",{}).get("ownership_pct",100.0)>=100.0 for p in scn["income_cards"] if p.get("type")=="1120") if any(p.get("type")=="1120" for p in scn["income_cards"]) else True,
           "support_continuance_ok": all(p.get("payload",{}).get("continuance_3yr",True) for p in scn["income_cards"] if p.get("type")=="Other" and p.get("payload",{}).get("type") in ["Alimony","Child Support","Housing Allowance"]) if any(p.get("type")=="Other" for p in scn["income_cards"]) else True,
           "rental_method_conflict": False, "rental_negative": False,
           "high_ltv_cap": comp["LTV"]>97.0 and h["program"]=="Conventional",
           "property_sanity_warn": (h["tax_rate_pct"]<0.5 or h["tax_rate_pct"]>3.0 or h["hoi_annual"]<600 or h["hoi_annual"]>6000),
           "debt_lt_10_excluded": any(d.get("exclude_lt_10") and (d.get("remaining_payments") or 0)<10 for d in scn["debt_cards"]),
           "debt_payoff": any(d.get("pay_off_at_close") for d in scn["debt_cards"]),
           "sl_policy_applied": any(d.get("type")=="student_loan" for d in scn["debt_cards"])}
    checklist=[]; types=[c["type"] for c in scn["income_cards"]]
    if "W-2" in types: checklist+=["30 days paystubs","2 years W-2s","VOE"]
    if "Schedule C" in types: checklist+=["1040s (2 years) incl. Sch C","Proof of business activity"]
    if "K-1" in types: checklist+=["K-1s (2 years)","Distribution history or liquidity analysis"]
    if "1120" in types: checklist+=["1120 returns (2 years)"]
    if "Rental" in types: checklist+=["Schedule E or lease/market rent docs"]
    if any(c.get("payload",{}).get("type") in ["Alimony","Child Support","Housing Allowance"] for c in scn["income_cards"] if c.get("type")=="Other"): checklist+=["Court order and proof of 3-year continuance"]
    from ui.tabs_dashboard import render_dashboard as _render_dashboard
    rules=_render_dashboard(summary, flags, checklist, st.session_state["scenario_name"])
    from export.pdf_export import build_prequal_pdf
    critical=any(r.get("severity")=="critical" for r in rules); override=None
    if critical: override=st.text_area("Override reason to export anyway")
    if (not critical) or (critical and override):
        if st.button("Export PDF"):
            import tempfile, os
            tmp=tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            deal={"Scenario":st.session_state["scenario_name"],"Program":h["program"],"Rate":h["rate_pct"],"TermYears":h["term_years"],"PurchasePrice":h["purchase_price"],"BaseLoan":comp["BaseLoan"],"AdjustedLoan":comp["AdjustedLoan"],"LTV":comp["LTV"]}
            build_prequal_pdf(tmp.name, deal, summary, rules, checklist, DISCLAIMER)
            with open(tmp.name,"rb") as f: st.download_button("Download PDF", data=f.read(), file_name=f"amalo_{st.session_state['scenario_name']}.pdf"); os.unlink(tmp.name)
