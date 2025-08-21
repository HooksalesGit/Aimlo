from __future__ import annotations
from typing import List
def NZ(x):
    try: return max(0.0, float(x or 0.0))
    except: return 0.0
def monthly_payment(principal: float, rate_pct: float, term_years: int) -> float:
    L=NZ(principal); r=NZ(rate_pct)/100/12; n=int(NZ(term_years)*12)
    if n<=0: return 0.0
    if r==0: return L/n
    return L*r/(1-(1+r)**(-n))
def principal_from_payment(payment: float, rate_pct: float, term_years: int) -> float:
    P=NZ(payment); r=NZ(rate_pct)/100/12; n=int(NZ(term_years)*12)
    if n<=0: return 0.0
    if r==0: return P*n
    return P*(1-(1+r)**(-n))/r
def w2_row_to_monthly(r: dict)->float:
    if r.get("pay_type","Salary")=="Salary": base=NZ(r.get("annual_salary"))/12
    else: base=NZ(r.get("hourly_rate"))*NZ(r.get("hours_per_week"))*52/12
    if int(r.get("include_variable",0))!=1: return base
    ytd=NZ(r.get("ot_ytd"))+NZ(r.get("bonus_ytd"))+NZ(r.get("comm_ytd"))
    ly=NZ(r.get("ot_ly"))+NZ(r.get("bonus_ly"))+NZ(r.get("comm_ly"))
    m=NZ(r.get("months_ytd"))+NZ(r.get("months_ly"))
    var=(ytd+ly)/m if m>0 else 0.0
    return base+var
def schc_rows_to_monthly(rows: List[dict])->float:
    by_year={}
    for r in rows:
        y=int(r.get("year",0))
        adj=NZ(r.get("net_profit"))+NZ(r.get("nonrecurring"))+NZ(r.get("depletion"))+NZ(r.get("depreciation"))-NZ(r.get("non_ded_meals"))+NZ(r.get("use_of_home"))+NZ(r.get("amort_casualty"))+(NZ(r.get("business_miles"))*NZ(r.get("mile_dep_rate")))
        by_year[y]=by_year.get(y,0.0)+adj
    if not by_year: return 0.0
    return sum(by_year.values())/len(by_year)/12
def k1_rows_to_monthly(rows: List[dict])->float:
    by_year={}
    for r in rows:
        y=int(r.get("year",0))
        adj=NZ(r.get("ordinary"))+NZ(r.get("net_rental_other"))+NZ(r.get("guaranteed_pmt"))+NZ(r.get("nonrecurring"))+NZ(r.get("depreciation"))+NZ(r.get("depletion"))+NZ(r.get("amort_casualty"))-NZ(r.get("notes_lt1yr"))-NZ(r.get("non_ded_tande"))
        after=adj*(NZ(r.get("ownership_pct"))/100.0)
        by_year[y]=by_year.get(y,0.0)+after
    if not by_year: return 0.0
    return sum(by_year.values())/len(by_year)/12
def c1120_rows_to_monthly(rows: List[dict])->float:
    by_year={}
    for r in rows:
        if NZ(r.get("ownership_pct"))<100.0: continue
        y=int(r.get("year",0))
        adj=NZ(r.get("taxable_income"))-NZ(r.get("total_tax"))+NZ(r.get("nonrecurring"))+NZ(r.get("other_inc_loss"))+NZ(r.get("depreciation"))+NZ(r.get("depletion"))+NZ(r.get("amort_casualty"))-NZ(r.get("notes_lt1yr"))-NZ(r.get("non_ded_tande"))-NZ(r.get("dividends_paid"))
        by_year[y]=by_year.get(y,0.0)+adj
    if not by_year: return 0.0
    return sum(by_year.values())/len(by_year)/12
def rentals_schedule_e_monthly(lines: List[dict])->float:
    t=0.0
    for r in lines: t+=(NZ(r.get("rents"))-NZ(r.get("expenses"))+NZ(r.get("depreciation")))/12.0
    return t
def rentals_75pct_gross_monthly(gross_annual: float)->float: return 0.75*NZ(gross_annual)/12.0
def other_income_rows_to_monthly(rows: List[dict])->float:
    t=0.0
    for r in rows: t+=NZ(r.get("gross_monthly"))*(1+NZ(r.get("gross_up_pct"))/100.0)
    return t
def student_loan_payment(policy: str, balance: float, documented: float, amortizing: bool)->float:
    if policy=="Conventional":
        if amortizing and documented>0: return documented
        return 0.01*NZ(balance)
    elif policy=="FHA":
        if amortizing and documented>0: return documented
        return 0.005*NZ(balance)
    elif policy=="VA":
        if amortizing and documented>0: return documented
        return 0.05*NZ(balance)/12.0
    elif policy=="USDA":
        if amortizing and documented>0: return documented
        return 0.005*NZ(balance)
    return documented
def debts_monthly_total(cards, policy: str)->float:
    t=0.0
    for d in cards:
        if d.get("pay_off_at_close"): continue
        if d.get("exclude_lt_10") and (d.get("remaining_payments") or 0)<10: continue
        if d.get("type")=="student_loan":
            t+=student_loan_payment(policy, d.get("sl_balance",0.0), d.get("sl_documented_payment",0.0), bool(d.get("sl_amortizing",False)))
        else:
            t+=NZ(d.get("monthly_payment"))
    return t
from .presets import CONV_MI_BANDS, FHA_TABLE, VA_TABLE, USDA_TABLE
def pick_conv_mi_factor(ltv): 
    for floor,fac in CONV_MI_BANDS:
        if ltv>=floor: return fac
    return 0.0
def piti_components(pp, dp, rate, term, tax_pct, hoi_annual, hoa_mo, program, finance_upfront):
    pp=NZ(pp); dp=NZ(dp); base=max(0.0, pp-dp); ltv=0 if pp==0 else 100*base/pp
    taxes=pp*NZ(tax_pct)/100/12; hoi=NZ(hoi_annual)/12; hoa=NZ(hoa_mo)
    upfront=0.0; mi_mip=0.0
    if program=="Conventional":
        mi_mip=(pick_conv_mi_factor(ltv)*base)/12
    elif program=="FHA":
        upfront=FHA_TABLE["ufmip_pct"]*base; annual=FHA_TABLE["annual_mip"]; loan=base+(upfront if finance_upfront else 0.0); mi_mip=(annual*loan)/12
    elif program=="VA":
        upfront=VA_TABLE["first_use"]["default"]*base
    elif program=="USDA":
        upfront=USDA_TABLE["guarantee_upfront"]*base; annual=USDA_TABLE["annual_fee"]; loan=base+(upfront if finance_upfront else 0.0); mi_mip=(annual*loan)/12
    adjusted=base+(upfront if finance_upfront else 0.0)
    from math import isfinite
    from math import isnan
    pi=monthly_payment(adjusted, rate, term)
    return {"BaseLoan":base,"AdjustedLoan":adjusted,"LTV":ltv,"PI":pi,"Taxes":taxes,"HOI":hoi,"HOA":hoa,"MI_MIP":mi_mip,"PITIA":pi+taxes+hoi+hoa+mi_mip}
def dti(housing, other, income):
    inc=max(1e-6, NZ(income)); fe=NZ(housing)/inc; be=(NZ(housing)+NZ(other))/inc; return fe,be
