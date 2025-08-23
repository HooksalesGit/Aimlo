import streamlit as st


def render_property_panel(scn):
    st.subheader("Property Info")
    h = scn.get("housing", {})
    price = h.get("purchase_price", 0)
    dp = h.get("down_payment_amt", 0)
    rate = h.get("rate_pct", 0)
    term = h.get("term_years", 0)
    st.write(f"Price ${price:,.0f} | DP ${dp:,.0f} | Rate {rate:.3f}% | Term {term}y")
    if st.button("Edit property & program (open sidebar)"):
        st.session_state["active_editor"] = {"kind": "property", "id": "housing"}
        st.rerun()
