import copy, uuid
def new_id(prefix='id'): import uuid; return f"{prefix}_{uuid.uuid4().hex[:8]}"
def default_scenario():
    return {
        "borrowers": {
            1: {"first_name": "Borrower", "last_name": "1", "phone": "", "credit_score": 0},
            2: {"first_name": "Borrower", "last_name": "2", "phone": "", "credit_score": 0},
        },
        "housing": {"purchase_price":450000.0,"down_payment_amt":45000.0,"rate_pct":6.75,"term_years":30,"tax_rate_pct":1.25,"hoi_annual":1800.0,"hoa_monthly":0.0,"program":"Conventional","finance_upfront":False},
        "income_cards": [],
        "debt_cards": [],
        "settings": {"student_loan_policy":"Conventional"},
    }
def clone(payload): return copy.deepcopy(payload)
