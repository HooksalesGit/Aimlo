import streamlit as st


def render_bottombar(enabled, summary, checklist):
    if not enabled:
        return
    fe, be = summary.get("FE", 0.0), summary.get("BE", 0.0)
    fe_t, be_t = summary.get("FE_target", 1.0), summary.get("BE_target", 1.0)
    fe_ok = fe <= fe_t
    be_ok = be <= be_t
    docs_html = "".join(
        f"<div><input type='checkbox'> {item}</div>" for item in checklist
    )
    st.markdown(
        f"""
    <style>
    .bb{{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1px solid #eee;padding:8px;z-index:998}}
    .bb span{{margin-right:16px}}
    .doclist{{position:fixed;bottom:40px;right:0;background:#fff;border:1px solid #eee;padding:8px;max-height:200px;overflow-y:auto;z-index:999}}
    </style>
    <div class='bb'><span><b>Income</b> ${summary.get('TotalIncome',0):,.2f}</span>
    <span><b>PITIA</b> ${summary.get('PITIA',0):,.2f}</span>
    <span><b>FE</b> {fe:.2%} ({'PASS' if fe_ok else 'CHECK'})</span>
    <span><b>BE</b> {be:.2%} ({'PASS' if be_ok else 'CHECK'})</span></div>
    <div class='doclist'>{docs_html}</div>
    """,
        unsafe_allow_html=True,
    )
