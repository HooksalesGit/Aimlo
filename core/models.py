from typing import Literal
from pydantic import BaseModel
class W2Job(BaseModel):
    id: str; borrower_id: int = 1; employer: str = ""; pay_type: Literal["Salary","Hourly"] = "Salary"
    annual_salary: float = 0.0; hourly_rate: float = 0.0; hours_per_week: float = 40.0
    ot_ytd: float = 0.0; bonus_ytd: float = 0.0; comm_ytd: float = 0.0; months_ytd: float = 0.0
    ot_ly: float = 0.0; bonus_ly: float = 0.0; comm_ly: float = 0.0; months_ly: float = 0.0; include_variable: int = 0
class SchC(BaseModel):
    id: str; borrower_id: int = 1; business_name: str = ""; year: int = 2024
    net_profit: float = 0.0; nonrecurring: float = 0.0; depletion: float = 0.0; depreciation: float = 0.0
    non_ded_meals: float = 0.0; use_of_home: float = 0.0; amort_casualty: float = 0.0; business_miles: float = 0.0; mile_dep_rate: float = 0.0
class K1(BaseModel):
    id: str; borrower_id: int = 1; entity_name: str = ""; type: Literal["1065","1120S"] = "1065"; year: int = 2024
    ownership_pct: float = 0.0; ordinary: float = 0.0; net_rental_other: float = 0.0; guaranteed_pmt: float = 0.0
    nonrecurring: float = 0.0; depreciation: float = 0.0; depletion: float = 0.0; amort_casualty: float = 0.0; notes_lt1yr: float = 0.0; non_ded_tande: float = 0.0
    verified_distributions: bool = False; analyzed_liquidity: bool = False
class C1120(BaseModel):
    id: str; borrower_id: int = 1; corp_name: str = ""; year: int = 2024; ownership_pct: float = 0.0
    taxable_income: float = 0.0; total_tax: float = 0.0; nonrecurring: float = 0.0; other_inc_loss: float = 0.0
    depreciation: float = 0.0; depletion: float = 0.0; amort_casualty: float = 0.0; notes_lt1yr: float = 0.0; non_ded_tande: float = 0.0; dividends_paid: float = 0.0
class RentalLine(BaseModel):
    id: str; borrower_id: int = 1; property: str = ""; year: int = 2024; rents: float = 0.0; expenses: float = 0.0; depreciation: float = 0.0
class OtherIncome(BaseModel):
    id: str; borrower_id: int = 1; type: str = "Social Security"; gross_monthly: float = 0.0; gross_up_pct: float = 0.0; continuance_3yr: bool = False
class Debt(BaseModel):
    id: str; borrower_id: int = 1; type: Literal["installment","revolving","student_loan","support"] = "installment"
    name: str = ""; monthly_payment: float = 0.0; remaining_payments: int | None = None
    exclude_lt_10: bool = False; pay_off_at_close: bool = False
    sl_balance: float = 0.0; sl_documented_payment: float = 0.0; sl_amortizing: bool = False
class Housing(BaseModel):
    purchase_price: float = 450000.0; down_payment_amt: float = 45000.0; rate_pct: float = 6.75; term_years: int = 30
    tax_rate_pct: float = 1.25; hoi_annual: float = 1800.0; hoa_monthly: float = 0.0; program: Literal["Conventional","FHA","VA","USDA","Jumbo"] = "Conventional"; finance_upfront: bool = False
