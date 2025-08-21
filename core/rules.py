def rule(code, severity, message, **ctx):
    return {"code":code,"severity":severity,"message":message,"context":ctx}
def evaluate_rules(state: dict):
    out=[]; t=state.get("totals",{}); f=state.get("flags",{})
    if (t.get("total_income",0) or 0)<=0: out.append(rule("NO_INCOME","critical","No income entered; DTI is not meaningful."))
    if t.get("fe") is not None and t.get("fe_target") is not None and t["fe"]>t["fe_target"]:
        out.append(rule("DTI_OVER_TARGET","warn","Front-end DTI exceeds target.",fe=t["fe"],fe_target=t["fe_target"]))
    if t.get("be") is not None and t.get("be_target") is not None and t["be"]>t["be_target"]:
        out.append(rule("DTI_OVER_TARGET","warn","Back-end DTI exceeds target.",be=t["be"],be_target=t["be_target"]))
    if f.get("k1_gate_ok") is False: out.append(rule("K1_DIST_LIQ","critical","K-1 used but distributions/liquidity not verified."))
    if f.get("c1120_all_100pct") is False: out.append(rule("C1120_OWN_LT_100","critical","1120 income must be 100% owner to count."))
    if f.get("support_continuance_ok") is False: out.append(rule("CONTINUANCE_REQ","critical","Support income requires ≥3 years continuance."))
    if f.get("rental_method_conflict"): out.append(rule("RENTAL_METHOD_CONFLICT","warn","Choose either Schedule E or 75% Gross, not both."))
    if f.get("rental_negative"): out.append(rule("NEGATIVE_RENTAL","warn","Net rental income is negative."))
    if f.get("high_ltv_cap"): out.append(rule("HIGH_LTV_CAP","warn","LTV appears above typical program caps."))
    if f.get("property_sanity_warn"): out.append(rule("PROPERTY_SANITY","warn","Taxes/HOI/HOA or MI may be out of expected ranges vs price."))
    if f.get("debt_lt_10_excluded"): out.append(rule("DEBT_LT_10_EXCLUDED","info","Some debts excluded due to <10 payments remaining."))
    if f.get("debt_payoff"): out.append(rule("DEBT_PAYOFF_AT_CLOSE","info","Some debts marked paid at close and excluded from DTI."))
    if f.get("sl_policy_applied"): out.append(rule("SL_POLICY_APPLIED","info","Student loan policy imputed a payment."))
    return out
def has_blocking(rules): return any(r.get("severity")=="critical" for r in rules)
