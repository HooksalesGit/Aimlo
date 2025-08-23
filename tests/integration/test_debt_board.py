import streamlit as st
from ui.cards_debts import render_debt_board


def test_render_debt_board_monkeypatch(monkeypatch):
    st.session_state.clear()
    scn = {
        "debt_cards": [
            {
                "id": "abcd1234",
                "borrower_id": 1,
                "type": "installment",
                "name": "Car loan",
                "monthly_payment": 100.0,
            }
        ]
    }

    calls = []

    def fake_button(label, key=None, **kwargs):
        calls.append({"label": label, "key": key, "kwargs": kwargs})
        return False

    class Dummy:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_container(border=True):
        return Dummy()

    def fake_columns(spec):
        return Dummy(), Dummy(), Dummy(), Dummy()

    monkeypatch.setattr(st, "button", fake_button)
    monkeypatch.setattr(st, "container", fake_container)
    monkeypatch.setattr(st, "columns", fake_columns)
    monkeypatch.setattr(st, "subheader", lambda *a, **k: None)
    monkeypatch.setattr(st, "write", lambda *a, **k: None)
    monkeypatch.setattr(st, "caption", lambda *a, **k: None)
    monkeypatch.setattr(st, "markdown", lambda *a, **k: None)
    monkeypatch.setattr(st, "rerun", lambda: None)

    render_debt_board(scn)

    assert any(
        call["key"] and call["key"].startswith("deb_open_") and "label_visibility" not in call["kwargs"]
        for call in calls
    )
