"""Document checklist derivation."""

def document_checklist(income_cards):
    """Return list of required docs based on income cards."""
    checklist = []
    types = [c.get("type") for c in income_cards]
    if "W-2" in types:
        checklist += ["30 days paystubs", "2 years W-2s", "VOE"]
    if "Schedule C" in types:
        checklist += ["1040s (2 years) incl. Sch C", "Proof of business activity"]
    if "K-1" in types:
        checklist += ["K-1s (2 years)", "Distribution history or liquidity analysis"]
    if "1120" in types:
        checklist += ["1120 returns (2 years)"]
    if "Rental" in types:
        checklist += ["Schedule E or lease/market rent docs"]
    if any(
        c.get("payload", {}).get("type") in ["Alimony", "Child Support", "Housing Allowance"]
        for c in income_cards
        if c.get("type") == "Other"
    ):
        checklist += ["Court order and proof of 3-year continuance"]
    return checklist
