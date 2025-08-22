import streamlit as st, uuid
from core.calculators import (
    w2_row_to_monthly, schc_rows_to_monthly, k1_rows_to_monthly, c1120_rows_to_monthly,
    rentals_schedule_e_monthly, rentals_75pct_gross_monthly, other_income_rows_to_monthly
)
from core.presets import CONV_MI_BANDS, FHA_TABLE, VA_TABLE, USDA_TABLE, DISCLAIMER

HELP_MAP={
 "W-2":{"annual_salary":"Paystub YTD/Base; W-2 Box 1 context","hourly_rate":"Paystub rate","hours_per_week":"Offer/VOE","ot_ytd":"Paystub YTD OT","bonus_ytd":"Paystub YTD Bonus","comm_ytd":"Paystub YTD Commission","months_ytd":"Months covered by YTD","ot_ly":"W-2/Last Year OT","bonus_ly":"W-2/Last Year Bonus","comm_ly":"W-2/Last Year Comm","months_ly":"Months for LY variable"},
 "Schedule C":{"net_profit":"1040 Schedule C Line 31","depreciation":"Line 13","non_ded_meals":"Line 24b","use_of_home":"Line 30"},
 "K-1":{"guaranteed_pmt":"1065 Line 4c","ordinary":"Line 1","net_rental_other":"Lines 2-3","notes_lt1yr":"Schedule L (current liabilities)"},
 "1120":{"taxable_income":"1120 Line 30","total_tax":"1120 Line 31","notes_lt1yr":"Sched L <1yr notes"},
 "Rental":{"rents":"Schedule E Line 3","expenses":"Schedule E Line 20","depreciation":"Schedule E Line 18"},
 "Other":{"gross_monthly":"Award letter or bank statements","gross_up_pct":"If non-taxable, agency gross-up"}
}
def _id(): return uuid.uuid4().hex[:8]
def render_guidance_center(scn, warnings):
    tab = st.segmented_control(
        "Info Box", ["Disclosures", "Warnings", "Guides", "Where to find"], key="gc_tab"
    )
    if tab == "Disclosures":
        st.caption(DISCLAIMER)
    elif tab == "Warnings":
        if not warnings:
            st.info("No warnings currently.")
        else:
            for r in warnings:
                if r["severity"] == "critical":
                    st.error(f"[{r['code']}] {r['message']}")
                elif r["severity"] == "warn":
                    st.warning(f"[{r['code']}] {r['message']}")
                else:
                    st.info(f"[{r['code']}] {r['message']}")
    elif tab == "Guides":
        st.markdown(
            """- **W-2**: Base = salary or hourly × hours × 52/12. Variable income requires stability (≥12 months).
- **Schedule C**: Two-year average of adjusted income (L31 + add-backs).
- **K-1**: Use only with verified distributions or documented business liquidity.
- **1120**: Only if 100% owner.
- **Rental**: Choose Schedule E (add back depreciation) **or** 75% of gross (subject: use 75% market rent − PITIA).
- **Other**: Support income needs ≥3 years continuance. Gross-up only if non-taxable and allowed."""
        )
    else:
        st.markdown("**Where to find common fields**")
        for typ, fmap in HELP_MAP.items():
            st.write(f"**{typ}**")
            for f, desc in fmap.items():
                st.caption(f"- {f}: {desc}")
def render_income_new(scn):
    typ = st.selectbox("Income type", ["W-2","Schedule C","K-1","1120","Rental","Other"], key="new_income_typ")
    if st.button("Create income card"):
        cid=_id()
        defaults={
          "W-2":{"borrower_id":1,"employer":"","pay_type":"Salary","annual_salary":0.0,"hourly_rate":0.0,"hours_per_week":40.0,"ot_ytd":0.0,"bonus_ytd":0.0,"comm_ytd":0.0,"months_ytd":0.0,"ot_ly":0.0,"bonus_ly":0.0,"comm_ly":0.0,"months_ly":0.0,"include_variable":0},
          "Schedule C":{"borrower_id":1,"business_name":"","year":2024,"net_profit":0.0,"nonrecurring":0.0,"depletion":0.0,"depreciation":0.0,"non_ded_meals":0.0,"use_of_home":0.0,"amort_casualty":0.0,"business_miles":0.0,"mile_dep_rate":0.0},
          "K-1":{"borrower_id":1,"entity_name":"","type":"1065","year":2024,"ownership_pct":0.0,"ordinary":0.0,"net_rental_other":0.0,"guaranteed_pmt":0.0,"nonrecurring":0.0,"depreciation":0.0,"depletion":0.0,"amort_casualty":0.0,"notes_lt1yr":0.0,"non_ded_tande":0.0,"verified_distributions":False,"analyzed_liquidity":False},
          "1120":{"borrower_id":1,"corp_name":"","year":2024,"ownership_pct":0.0,"taxable_income":0.0,"total_tax":0.0,"nonrecurring":0.0,"other_inc_loss":0.0,"depreciation":0.0,"depletion":0.0,"amort_casualty":0.0,"notes_lt1yr":0.0,"non_ded_tande":0.0,"dividends_paid":0.0},
          "Rental":{"borrower_id":1,"method":"Schedule E","lines":[{"id":_id(),"borrower_id":1,"property":"","year":2024,"rents":0.0,"expenses":0.0,"depreciation":0.0}],"gross_rents_annual":0.0,"subject_market_rent":0.0,"subject_pitia":0.0},
          "Other":{"borrower_id":1,"type":"Social Security","gross_monthly":0.0,"gross_up_pct":0.0,"continuance_3yr":False},
        }
        scn["income_cards"].append({"id":cid,"type":typ,"payload":defaults[typ]})
        st.session_state["selected"]={"kind":"income","id":cid}; st.rerun()
def render_debt_new(scn):
    typ = st.selectbox("Debt type", ["installment","revolving","student_loan","support"], key="new_debt_typ")
    if st.button("Create debt card"):
        cid=_id()
        scn["debt_cards"].append({"id":cid,"borrower_id":1,"type":typ,"name":"","monthly_payment":0.0,"remaining_payments":None,"exclude_lt_10":False,"pay_off_at_close":False,"sl_balance":0.0,"sl_documented_payment":0.0,"sl_amortizing":False})
        st.session_state["selected"]={"kind":"debt","id":cid}; st.rerun()
def render_income_editor(card):
    t=card["type"]; p=card["payload"]
    st.number_input("Borrower ID (1-6)", value=int(p.get("borrower_id",1)), min_value=1, max_value=6, step=1, key=f"ed_bid_{card['id']}")
    if t=="W-2":
        p["employer"]=st.text_input("Employer", value=p.get("employer",""))
        pt=st.radio("Pay Type", ["Salary","Hourly"], index=0 if p.get("pay_type","Salary")=="Salary" else 1, horizontal=True); p["pay_type"]=pt
        if pt=="Salary":
            p["annual_salary"]=st.number_input("Annual Salary", value=float(p.get("annual_salary",0.0)), help=HELP_MAP["W-2"]["annual_salary"])
        else:
            c1,c2=st.columns(2)
            p["hourly_rate"]=c1.number_input("Hourly Rate", value=float(p.get("hourly_rate",0.0)), help=HELP_MAP["W-2"]["hourly_rate"])
            p["hours_per_week"]=c2.number_input("Hours/Week", value=float(p.get("hours_per_week",40.0)), help=HELP_MAP["W-2"]["hours_per_week"])
        st.markdown("**Variable Income (YTD/LY)**")
        c1,c2,c3,c4=st.columns(4)
        p["ot_ytd"]=c1.number_input("OT YTD", value=float(p.get("ot_ytd",0.0)))
        p["bonus_ytd"]=c2.number_input("Bonus YTD", value=float(p.get("bonus_ytd",0.0)))
        p["comm_ytd"]=c3.number_input("Comm YTD", value=float(p.get("comm_ytd",0.0)))
        p["months_ytd"]=c4.number_input("Months YTD", value=float(p.get("months_ytd",0.0)))
        d1,d2,d3,d4=st.columns(4)
        p["ot_ly"]=d1.number_input("OT LY", value=float(p.get("ot_ly",0.0)))
        p["bonus_ly"]=d2.number_input("Bonus LY", value=float(p.get("bonus_ly",0.0)))
        p["comm_ly"]=d3.number_input("Comm LY", value=float(p.get("comm_ly",0.0)))
        p["months_ly"]=d4.number_input("Months LY", value=float(p.get("months_ly",0.0)))
        p["include_variable"]=1 if st.checkbox("Include Variable Income", value=bool(p.get("include_variable",0))) else 0
        st.caption(f"Monthly preview: ${w2_row_to_monthly(p):,.2f}")
    elif t=="Schedule C":
        p["business_name"]=st.text_input("Business Name", value=p.get("business_name",""))
        cols=st.columns(3)
        p["year"]=cols[0].number_input("Year", value=int(p.get("year",2024)), min_value=1990, max_value=2100, step=1)
        p["net_profit"]=cols[1].number_input("Net Profit (L31)", value=float(p.get("net_profit",0.0)))
        p["nonrecurring"]=cols[2].number_input("Nonrecurring", value=float(p.get("nonrecurring",0.0)))
        cols2=st.columns(4)
        p["depletion"]=cols2[0].number_input("Depletion", value=float(p.get("depletion",0.0)))
        p["depreciation"]=cols2[1].number_input("Depreciation", value=float(p.get("depreciation",0.0)))
        p["non_ded_meals"]=cols2[2].number_input("Non-ded Meals", value=float(p.get("non_ded_meals",0.0)))
        p["use_of_home"]=cols2[3].number_input("Use of Home", value=float(p.get("use_of_home",0.0)))
        cols3=st.columns(3)
        p["amort_casualty"]=cols3[0].number_input("Amort/Casualty", value=float(p.get("amort_casualty",0.0)))
        p["business_miles"]=cols3[1].number_input("Business Miles", value=float(p.get("business_miles",0.0)))
        p["mile_dep_rate"]=cols3[2].number_input("Mile Deprec. Rate", value=float(p.get("mile_dep_rate",0.0)))
        st.caption(f"Monthly preview: ${schc_rows_to_monthly([p]):,.2f}")
    elif t=="K-1":
        p["entity_name"]=st.text_input("Entity Name", value=p.get("entity_name",""))
        cols=st.columns(4)
        p["type"]=cols[0].selectbox("Type", ["1065","1120S"], index=0 if p.get("type","1065")=="1065" else 1)
        p["year"]=cols[1].number_input("Year", value=int(p.get("year",2024)), min_value=1990, max_value=2100, step=1)
        p["ownership_pct"]=cols[2].number_input("Ownership %", value=float(p.get("ownership_pct",0.0)), min_value=0.0, max_value=100.0)
        p["guaranteed_pmt"]=cols[3].number_input("Guaranteed Payments (1065 L4c)", value=float(p.get("guaranteed_pmt",0.0)))
        cols2=st.columns(4)
        p["ordinary"]=cols2[0].number_input("Ordinary (L1)", value=float(p.get("ordinary",0.0)))
        p["net_rental_other"]=cols2[1].number_input("Net Rental/Other (L2-3)", value=float(p.get("net_rental_other",0.0)))
        p["nonrecurring"]=cols2[2].number_input("Nonrecurring", value=float(p.get("nonrecurring",0.0)))
        p["depreciation"]=cols2[3].number_input("Depreciation", value=float(p.get("depreciation",0.0)))
        cols3=st.columns(3)
        p["depletion"]=cols3[0].number_input("Depletion", value=float(p.get("depletion",0.0)))
        p["amort_casualty"]=cols3[1].number_input("Amort/Casualty", value=float(p.get("amort_casualty",0.0)))
        p["notes_lt1yr"]=cols3[2].number_input("Notes <1yr (Sched L)", value=float(p.get("notes_lt1yr",0.0)))
        p["non_ded_tande"]=st.number_input("Non-ded T&E", value=float(p.get("non_ded_tande",0.0)))
        g1,g2=st.columns(2)
        p["verified_distributions"]=g1.checkbox("Verified distributions history", value=bool(p.get("verified_distributions",False)))
        p["analyzed_liquidity"]=g2.checkbox("Analyzed business liquidity", value=bool(p.get("analyzed_liquidity",False)))
        st.caption(f"Monthly preview: ${k1_rows_to_monthly([p]):,.2f}")
    elif t=="1120":
        p["corp_name"]=st.text_input("Corporation Name", value=p.get("corp_name",""))
        cols=st.columns(4)
        p["year"]=cols[0].number_input("Year", value=int(p.get("year",2024)), min_value=1990, max_value=2100, step=1)
        p["ownership_pct"]=cols[1].number_input("Ownership %", value=float(p.get("ownership_pct",0.0)), min_value=0.0, max_value=100.0)
        p["taxable_income"]=cols[2].number_input("Taxable Income (L30)", value=float(p.get("taxable_income",0.0)))
        p["total_tax"]=cols[3].number_input("Total Tax (L31)", value=float(p.get("total_tax",0.0)))
        cols2=st.columns(4)
        p["nonrecurring"]=cols2[0].number_input("Nonrecurring", value=float(p.get("nonrecurring",0.0)))
        p["other_inc_loss"]=cols2[1].number_input("Other Inc/Loss", value=float(p.get("other_inc_loss",0.0)))
        p["depreciation"]=cols2[2].number_input("Depreciation", value=float(p.get("depreciation",0.0)))
        p["depletion"]=cols2[3].number_input("Depletion", value=float(p.get("depletion",0.0)))
        cols3=st.columns(4)
        p["amort_casualty"]=cols3[0].number_input("Amort/Casualty", value=float(p.get("amort_casualty",0.0)))
        p["notes_lt1yr"]=cols3[1].number_input("Notes <1yr", value=float(p.get("notes_lt1yr",0.0)))
        p["non_ded_tande"]=cols3[2].number_input("Non-ded T&E", value=float(p.get("non_ded_tande",0.0)))
        p["dividends_paid"]=cols3[3].number_input("Dividends Paid", value=float(p.get("dividends_paid",0.0)))
        st.caption("Preview uses 100% owner rows only.")
    elif t=="Rental":
        m=st.radio("Method", ["Schedule E","75% Gross"], index=0 if p.get("method","Schedule E")=="Schedule E" else 1, horizontal=True); p["method"]=m
        if m=="Schedule E":
            if st.button("Add line"): p["lines"].append({"id":_id(),"borrower_id":p.get("borrower_id",1),"property":"","year":2024,"rents":0.0,"expenses":0.0,"depreciation":0.0})
            rm=None
            for j,ln in enumerate(p["lines"]):
                with st.expander(f"Line {j+1}"):
                    ln["property"]=st.text_input("Property", value=ln.get("property",""), key=f"r_prop_{card['id']}_{j}")
                    c1,c2,c3,c4=st.columns(4)
                    ln["year"]=c1.number_input("Year", value=int(ln.get("year",2024)), min_value=1990, max_value=2100, step=1, key=f"r_yr_{card['id']}_{j}")
                    ln["rents"]=c2.number_input("Rents (L3)", value=float(ln.get("rents",0.0)), key=f"r_r_{card['id']}_{j}")
                    ln["expenses"]=c3.number_input("Expenses (L20)", value=float(ln.get("expenses",0.0)), key=f"r_e_{card['id']}_{j}")
                    ln["depreciation"]=c4.number_input("Depreciation (L18)", value=float(ln.get("depreciation",0.0)), key=f"r_d_{card['id']}_{j}")
                    if st.button("Remove", key=f"r_rm_{card['id']}_{j}"): rm=j
            if rm is not None: p["lines"].pop(rm)
            preview=rentals_schedule_e_monthly(p["lines"])
        else:
            p["gross_rents_annual"]=st.number_input("Total Gross Rents (Annual)", value=float(p.get("gross_rents_annual",0.0)))
            p["subject_market_rent"]=st.number_input("Subject Market Rent (Monthly)", value=float(p.get("subject_market_rent",0.0)))
            p["subject_pitia"]=st.number_input("Subject PITIA (Monthly)", value=float(p.get("subject_pitia",0.0)))
            preview=rentals_75pct_gross_monthly(p.get("gross_rents_annual",0.0)); preview+=0.75*float(p.get("subject_market_rent",0.0)) - float(p.get("subject_pitia",0.0))
        st.caption(f"Monthly preview: ${preview:,.2f}")
    else:
        p["type"]=st.selectbox("Type", ["Social Security","Disability","Alimony","Child Support","Housing Allowance","Other"], index=["Social Security","Disability","Alimony","Child Support","Housing Allowance","Other"].index(p.get("type","Social Security")) if p.get("type") in ["Social Security","Disability","Alimony","Child Support","Housing Allowance","Other"] else 0)
        c1,c2,c3=st.columns(3)
        p["gross_monthly"]=c1.number_input("Gross Monthly", value=float(p.get("gross_monthly",0.0)))
        p["gross_up_pct"]=c2.number_input("Gross-up % (if non-taxable)", value=float(p.get("gross_up_pct",0.0)), min_value=0.0, max_value=50.0)
        if p["type"] in ["Alimony","Child Support","Housing Allowance"]:
            p["continuance_3yr"]=c3.checkbox("≥ 3 years continuance", value=bool(p.get("continuance_3yr",False)))
        st.caption(f"Monthly preview: ${other_income_rows_to_monthly([p]):,.2f}")
def render_debt_editor(card, policy):
    d=card
    d["type"]=st.selectbox("Type", ["installment","revolving","student_loan","support"], index=["installment","revolving","student_loan","support"].index(d.get("type","installment")))
    d["name"]=st.text_input("Name/Description", value=d.get("name",""))
    c1,c2=st.columns(2)
    d["monthly_payment"]=c1.number_input("Monthly Payment", value=float(d.get("monthly_payment",0.0)))
    d["remaining_payments"]=c2.number_input("Remaining Payments (optional)", value=int(d.get("remaining_payments") or 0), min_value=0, step=1)
    c3,c4=st.columns(2)
    d["exclude_lt_10"]=c3.checkbox("Exclude if <10 remaining", value=bool(d.get("exclude_lt_10",False)))
    d["pay_off_at_close"]=c4.checkbox("Pay off at close", value=bool(d.get("pay_off_at_close",False)))
    if d["type"]=="student_loan":
        c5,c6,c7=st.columns(3)
        d["sl_balance"]=c5.number_input("Loan Balance", value=float(d.get("sl_balance",0.0)))
        d["sl_documented_payment"]=c6.number_input("Documented Payment", value=float(d.get("sl_documented_payment",0.0)))
        d["sl_amortizing"]=c7.checkbox("Fully amortizing?", value=bool(d.get("sl_amortizing",False)))
        st.caption(f"Policy in effect: {policy}")
def render_property_editor(h):
    st.number_input("Purchase Price", value=float(h.get("purchase_price",0.0)), step=1000.0, key="h_pp", on_change=lambda: h.update(purchase_price=st.session_state["h_pp"]))
    st.number_input("Down Payment $", value=float(h.get("down_payment_amt",0.0)), step=1000.0, key="h_dp", on_change=lambda: h.update(down_payment_amt=st.session_state["h_dp"]))
    st.number_input("Rate %", value=float(h.get("rate_pct",0.0)), step=0.125, format="%.3f", key="h_rate", on_change=lambda: h.update(rate_pct=st.session_state["h_rate"]))
    st.number_input("Term (years)", value=int(h.get("term_years",30)), min_value=1, max_value=40, step=1, key="h_term", on_change=lambda: h.update(term_years=int(st.session_state["h_term"])))
    st.number_input("Property Tax % (annual of price)", value=float(h.get("tax_rate_pct",1.25)), step=0.05, key="h_tax", on_change=lambda: h.update(tax_rate_pct=st.session_state["h_tax"]))
    st.number_input("HOA Monthly", value=float(h.get("hoa_monthly",0.0)), step=10.0, key="h_hoa", on_change=lambda: h.update(hoa_monthly=st.session_state["h_hoa"]))
    st.number_input("Homeowner's Insurance (annual $)", value=float(h.get("hoi_annual",1800.0)), step=50.0, key="h_hoi", on_change=lambda: h.update(hoi_annual=st.session_state["h_hoi"]))
    h["finance_upfront"]=st.checkbox("Finance upfront fee (FHA/VA/USDA)", value=bool(h.get("finance_upfront",False)))
    st.markdown("---"); st.markdown("### Program Tables (MI/MIP/Fees)"); st.caption("Edit defaults as needed (Conventional MI bands, FHA/VA/USDA upfront & annual).")
    st.json({"Conventional_MI_bands":CONV_MI_BANDS,"FHA":FHA_TABLE,"VA":VA_TABLE,"USDA":USDA_TABLE})
def render_sidebar(selected, scn, warnings):
    if selected is None or selected.get("kind") is None:
        st.info("Select an item to edit from the main panel.")
        return
    if selected["kind"]=="income_new":
        render_income_new(scn)
    elif selected["kind"]=="debt_new":
        render_debt_new(scn)
    elif selected["kind"]=="income":
        card=next((x for x in scn["income_cards"] if x["id"]==selected["id"]), None)
        if not card:
            st.info("No card found.")
        else:
            render_income_editor(card)
    elif selected["kind"]=="debt":
        card=next((x for x in scn["debt_cards"] if x["id"]==selected["id"]), None)
        if not card:
            st.info("No debt found.")
        else:
            policy=scn.get("settings",{}).get("student_loan_policy","Conventional")
            render_debt_editor(card, policy)
    elif selected["kind"]=="property":
        render_property_editor(scn["housing"])
