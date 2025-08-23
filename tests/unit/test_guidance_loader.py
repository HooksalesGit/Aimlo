from core.guidance import load_field_hints, load_rulebook, get_field_hint


def test_load_field_hints():
    hints = load_field_hints()
    assert "w2" in hints
    assert get_field_hint("w2", "annual_salary")


def test_load_rulebook():
    rules = load_rulebook()
    assert "NO_INCOME" in rules
