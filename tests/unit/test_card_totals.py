import ui.cards_income as ci
import ui.cards_debts as cd

def test_income_monthly_w2():
    card = {"type": "W-2", "payload": {"annual_salary": 120000, "pay_type": "Salary"}}
    assert ci.income_monthly(card) == 10000.0

def test_debt_monthly_student_loan():
    card = {"type": "student_loan", "sl_balance": 50000.0, "sl_documented_payment": 0.0, "sl_amortizing": False}
    assert cd.debt_monthly(card, "Conventional") == 500.0
