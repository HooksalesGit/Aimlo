import streamlit as st
from ui.theme import THEME


def render_bottombar(open_state, summary):
    colors = THEME["colors"]
    bg = colors.get("panel_bg", "#333")
    text = colors.get("panel_text", "#fff")
    border = colors.get("border", "#eee")
    transition = THEME["drawer"]["transition_ms"]

    def _num(val, default=0.0):
        try:
            return float(val)
        except (TypeError, ValueError):
            return default

    fe, be = _num(summary.get("FE")), _num(summary.get("BE"))
    fe_t, be_t = _num(summary.get("FE_target", 1.0), 1.0), _num(summary.get("BE_target", 1.0), 1.0)
    fe_ok = fe <= fe_t
    be_ok = be <= be_t

    st.markdown(
        f"""
    <style>
    .bottomdrawer{{position:fixed;left:0;right:0;bottom:0;background:{bg};color:{text};border-top:1px solid {border};padding:8px;transform:translateY(100%);transition:transform {transition}ms;z-index:998}}
    .bottomdrawer.open{{transform:translateY(0);}}
    .bottomdrawer span{{margin-right:16px}}
    </style>
    """,
        unsafe_allow_html=True,
    )

    classes = "bottomdrawer open" if open_state else "bottomdrawer"
    st.markdown(
        f"""
    <div class='{classes}'>
        <span><b>Income</b> ${summary.get('TotalIncome',0):,.2f}</span>
        <span><b>PITIA</b> ${summary.get('PITIA',0):,.2f}</span>
        <span><b>FE</b> {fe:.2%} ({'PASS' if fe_ok else 'CHECK'})</span>
        <span><b>BE</b> {be:.2%} ({'PASS' if be_ok else 'CHECK'})</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if open_state:
        if st.button("▼", key="bottombar_hide"):
            from ui.utils import hide_bottombar
            hide_bottombar()
            st.rerun()
        st.markdown(
            "<style>#bottombar_hide{position:fixed;bottom:40px;right:10px;z-index:1000}</style>",
            unsafe_allow_html=True,
        )
