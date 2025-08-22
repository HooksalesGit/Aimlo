from core.checklist import document_checklist


def test_document_checklist_w2_k1_alimony():
    incomes = [
        {"type": "W-2", "payload": {}},
        {"type": "K-1", "payload": {}},
        {"type": "Other", "payload": {"type": "Alimony"}},
    ]
    docs = document_checklist(incomes)
    assert "30 days paystubs" in docs
    assert "K-1s (2 years)" in docs
    assert any("Court order" in d for d in docs)
