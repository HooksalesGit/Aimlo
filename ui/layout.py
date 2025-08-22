import streamlit as st
from core.calculators import w2_row_to_monthly, schc_rows_to_monthly, k1_rows_to_monthly, c1120_rows_to_monthly, rentals_schedule_e_monthly, rentals_75pct_gross_monthly, other_income_rows_to_monthly
def render_income_column(scn):
    st.subheader("All Income")
    if st.button("Add income card"): st.session_state["selected"]={"kind":"income_new","id":None}; st.rerun()
    total=0.0
    for i,c in enumerate(scn["income_cards"]):
        preview=0.0; t=c.get("type"); p=c.get("payload",{})
        if t=="W-2": preview=w2_row_to_monthly(p)
        elif t=="Schedule C": preview=schc_rows_to_monthly([p])
        elif t=="K-1": preview=k1_rows_to_monthly([p])
        elif t=="1120": preview=c1120_rows_to_monthly([p])
        elif t=="Rental":
            if p.get("method")=="Schedule E": preview=rentals_schedule_e_monthly(p.get("lines",[]))
            else: preview=rentals_75pct_gross_monthly(p.get("gross_rents_annual",0.0)); preview+=0.75*float(p.get("subject_market_rent",0.0)) - float(p.get("subject_pitia",0.0))
        elif t=="Other": preview=other_income_rows_to_monthly([p])
        title=p.get("employer") or p.get("business_name") or p.get("entity_name") or p.get("corp_name") or p.get("property") or p.get("type") or t
        st.write(f"**{t}** — {title or ''} • ${preview:,.2f}/mo")
        cols=st.columns(3)
        if cols[0].button("Edit", key=f"i_edit_{c['id']}"): st.session_state["selected"]={"kind":"income","id":c["id"]}; st.rerun()
        if cols[1].button("Duplicate", key=f"i_dup_{c['id']}"):
            import copy; scn["income_cards"].insert(i+1, copy.deepcopy(c)); st.rerun()
        if cols[2].button("Remove", key=f"i_rm_{c['id']}"):
            scn["income_cards"].pop(i); st.rerun()
        total+=preview
    st.caption(f"Total monthly income (preview): ${total:,.2f}")
def render_debt_column(scn):
    st.subheader("All Debts/Liabilities")
    if st.button("Add debt card"): st.session_state["selected"]={"kind":"debt_new","id":None}; st.rerun()
    total=0.0
    for i,d in enumerate(scn["debt_cards"]):
        title = (d.get("type","") + (" • " + d.get("name","") if d.get("name") else ""))
        pay = float(d.get("monthly_payment",0.0))
        st.write(f"**{title}** — ${pay:,.2f}/mo")
        cols=st.columns(3)
        if cols[0].button("Edit", key=f"d_edit_{d['id']}"): st.session_state["selected"]={"kind":"debt","id":d["id"]}; st.rerun()
        if cols[1].button("Duplicate", key=f"d_dup_{d['id']}"):
            import copy; scn["debt_cards"].insert(i+1, copy.deepcopy(d)); st.rerun()
        if cols[2].button("Remove", key=f"d_rm_{d['id']}"):
            scn["debt_cards"].pop(i); st.rerun()
        total+=pay
    st.caption(f"Sum of listed payments (policy may adjust student loans): ${total:,.2f}")
def render_property_snapshot(scn):
    st.subheader("Property Info")
    h=scn["housing"]
    st.write(f"Price ${h.get('purchase_price',0):,.0f} | DP ${h.get('down_payment_amt',0):,.0f} | Rate {h.get('rate_pct',0):.3f}% | Term {h.get('term_years',0)}y")
    if st.button("Edit property & program (open sidebar)", key="prop_edit"): st.session_state["selected"]={"kind":"property","id":"housing"}; st.rerun()
