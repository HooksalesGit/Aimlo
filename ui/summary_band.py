"""Top summary band replacing the old bottom drawer."""
from __future__ import annotations

import streamlit as st
from ui.theme import THEME
from core.calculators import principal_from_payment


def _clamp_pct(val: float) -> float:
    try:
        return max(0.0, min(100.0, float(val)))
    except (TypeError, ValueError):
        return 0.0


def render_summary_band(summary: dict) -> str:
    """Render collapsible summary band. Returns collapsed label for tests."""
    colors = THEME["colors"]
    spacing = THEME["spacing"]
    radii = THEME["radii"]
    st.session_state.setdefault("summary_expanded", False)
    expanded = st.session_state["summary_expanded"]

    income = float(summary.get("TotalIncome", 0.0))
    pitia = float(summary.get("PITIA", 0.0))
    fe = float(summary.get("FE", 0.0))
    be = float(summary.get("BE", 0.0))
    ltv = _clamp_pct(summary.get("LTV", 0.0))
    fe_t = float(summary.get("FE_target", 1.0))
    be_t = float(summary.get("BE_target", 1.0))

    def pct(x):
        return _clamp_pct(100 * float(x))

    if income <= 0:
        fe_str = be_str = "—"
        fe_status = be_status = ""
    else:
        fe_pct = pct(fe)
        be_pct = pct(be)
        fe_str = f"{fe_pct:.1f}%"
        be_str = f"{be_pct:.1f}%"
        fe_status = "PASS" if fe <= fe_t else "CHECK"
        be_status = "PASS" if be <= be_t else "CHECK"

    label = (
        f"Total Income ${income:,.2f} | "
        f"PITIA ${pitia:,.2f} | "
        f"FE {fe_str} {fe_status}".strip()
        + " | "
        + f"BE {be_str} {be_status}".strip()
        + " | "
        + f"LTV {ltv:.1f}% | "
        + f"Findings {summary.get('Findings', 0)}"
    )

    style = f"""
    <style>
    #summary_toggle{{width:100%;text-align:left;padding:{spacing['space_sm']}px;background:{colors['surface']};
    border:1px solid {colors['border']};border-radius:{radii['radius_md']}px;box-shadow:{THEME['shadows']['card']};
    position:sticky;top:60px;z-index:998;white-space:normal;}}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

    if st.button(label, key="summary_toggle"):
        st.session_state["summary_expanded"] = not expanded
        st.rerun()

    if st.session_state["summary_expanded"]:
        non_pi = sum(
            float(summary.get(k, 0.0))
            for k in ["Taxes", "HOI", "HOA", "MI_MIP"]
        )
        rate = float(summary.get("Rate", 0.0))
        term = int(summary.get("Term", 0))
        other = float(summary.get("OtherDebts", 0.0))
        dp_pct = float(summary.get("DownPaymentPct", 0.0))

        max_pi_fe = max(income * fe_t - non_pi, 0.0)
        max_pi_be = max(income * be_t - other - non_pi, 0.0)
        loan_fe = principal_from_payment(max_pi_fe, rate, term)
        loan_be = principal_from_payment(max_pi_be, rate, term)
        max_base = min(loan_fe, loan_be)
        max_purchase = max_base / (1 - dp_pct) if (1 - dp_pct) > 0 else 0.0

        st.markdown("### Snapshot")
        st.write(
            f"Program: {summary.get('Program','')} — Rate {rate:.2f}% — Term {term} yrs"
        )
        if summary.get("FinanceUpfront"):
            st.write("Upfront fees financed")
        st.write(
            f"Total Income ${income:,.2f} | PITIA ${pitia:,.2f} | FE {fe_str} {fe_status} | BE {be_str} {be_status} | LTV {ltv:.1f}%"
        )

        st.markdown("### Max Qualifiers")
        st.write(
            f"Max P&I (FE): ${max_pi_fe:,.2f} | Max P&I (BE): ${max_pi_be:,.2f}"
        )
        st.write(
            f"Max Base Loan: ${max_base:,.2f} | Max Purchase: ${max_purchase:,.2f}"
        )

        st.markdown("### Warnings & Findings")
        st.write("None")

        st.markdown("### Income & Debts")
        st.write(f"Other Debts ${other:,.2f}")

        st.markdown("### Housing Components")
        st.write(
            f"PI ${summary.get('PI',0):,.2f} | Taxes ${summary.get('Taxes',0):,.2f} | HOI ${summary.get('HOI',0):,.2f} | "
            f"HOA ${summary.get('HOA',0):,.2f} | MI/MIP ${summary.get('MI_MIP',0):,.2f} | Adjusted Loan ${summary.get('AdjustedLoan',0):,.2f}"
        )

        st.markdown("### Docs Progress")
        st.write(summary.get("DocsProgress", "0/0 complete"))

    return label

