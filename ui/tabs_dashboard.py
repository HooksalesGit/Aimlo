import streamlit as st, io, csv, json
from core.rules import evaluate_rules, has_blocking
from core.presets import DISCLAIMER
def render_dashboard(summary: dict, flags: dict, checklist: list, scenario_name: str):
    st.header(f"Dashboard — {scenario_name}")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total Income", f"${summary.get('TotalIncome',0):,.2f}")
    c2.metric("PITIA", f"${summary.get('PITIA',0):,.2f}")
    c3.metric("FE DTI", f"{summary.get('FE',0.0):.2%}")
    c4.metric("BE DTI", f"{summary.get('BE',0.0):.2%}")
    state={"totals":{"total_income":summary.get("TotalIncome",0.0),"housing_total":summary.get("PITIA",0.0),"other_debts":summary.get("OtherDebts",0.0),"fe":summary.get("FE",0.0),"be":summary.get("BE",0.0),"fe_target":summary.get("FE_target",1.0),"be_target":summary.get("BE_target",1.0)},"flags":flags}
    rules=evaluate_rules(state)
    st.subheader("Warnings & Findings")
    for r in rules:
        if r["severity"]=="critical": st.error(f"[{r['code']}] {r['message']}")
        elif r["severity"]=="warn": st.warning(f"[{r['code']}] {r['message']}")
        else: st.info(f"[{r['code']}] {r['message']}")
    st.subheader("Documentation Checklist")
    for item in checklist: st.checkbox(item, key=f"doc_{scenario_name}_{item}")
    st.write('---')
    st.caption(DISCLAIMER)
    st.subheader("Exports")
    st.download_button("Download scenario JSON", data=json.dumps({"summary":summary,"flags":flags,"checklist":checklist}, indent=2).encode("utf-8"), file_name=f"amalo_{scenario_name}.json", mime="application/json")
    csv_buf=io.StringIO(); w=csv.writer(csv_buf)
    w.writerow(["Scenario","TotalIncome","PITIA","OtherDebts","FE","BE"])
    w.writerow([scenario_name, summary.get("TotalIncome",0.0), summary.get("PITIA",0.0), summary.get("OtherDebts",0.0), summary.get("FE",0.0), summary.get("BE",0.0)])
    st.download_button("Download CSV Summary", data=csv_buf.getvalue().encode("utf-8"), file_name=f"amalo_{scenario_name}.csv", mime="text/csv")
    return rules
