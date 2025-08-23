import streamlit as st
from ui.tabs_dashboard import render_dashboard
from streamlit.delta_generator import DeltaGenerator


def test_dashboard_metrics_zero_income(monkeypatch):
    captured = {}

    def fake_metric(self, label, value, *a, **k):
        captured[label] = value

    monkeypatch.setattr(DeltaGenerator, "metric", fake_metric)

    # suppress non-essential Streamlit calls
    monkeypatch.setattr(st, "subheader", lambda *a, **k: None)
    monkeypatch.setattr(st, "error", lambda *a, **k: None)
    monkeypatch.setattr(st, "warning", lambda *a, **k: None)
    monkeypatch.setattr(st, "info", lambda *a, **k: None)
    monkeypatch.setattr(st, "checkbox", lambda *a, **k: False)
    monkeypatch.setattr(st, "write", lambda *a, **k: None)
    monkeypatch.setattr(st, "caption", lambda *a, **k: None)
    monkeypatch.setattr(st, "download_button", lambda *a, **k: None)

    st.session_state.clear()
    summary = {
        "TotalIncome": 0.0,
        "PITIA": 3329.95,
        "FE": 0.5,
        "BE": 0.6,
        "FE_target": 0.31,
        "BE_target": 0.43,
    }

    render_dashboard(summary, {}, [], "Test")

    assert captured["Total Income"] == "$0.00"
    assert captured["PITIA"] == "$3,329.95"
    assert captured["FE DTI"] == "—"
    assert captured["BE DTI"] == "—"


def test_dashboard_metrics_percent(monkeypatch):
    captured = {}

    def fake_metric(self, label, value, *a, **k):
        captured[label] = value

    monkeypatch.setattr(DeltaGenerator, "metric", fake_metric)
    monkeypatch.setattr(st, "subheader", lambda *a, **k: None)
    monkeypatch.setattr(st, "error", lambda *a, **k: None)
    monkeypatch.setattr(st, "warning", lambda *a, **k: None)
    monkeypatch.setattr(st, "info", lambda *a, **k: None)
    monkeypatch.setattr(st, "checkbox", lambda *a, **k: False)
    monkeypatch.setattr(st, "write", lambda *a, **k: None)
    monkeypatch.setattr(st, "caption", lambda *a, **k: None)
    monkeypatch.setattr(st, "download_button", lambda *a, **k: None)

    st.session_state.clear()
    summary = {
        "TotalIncome": 5000.0,
        "PITIA": 1500.0,
        "FE": 0.3,
        "BE": 0.4,
        "FE_target": 0.31,
        "BE_target": 0.43,
    }

    render_dashboard(summary, {}, [], "Test")

    assert captured["FE DTI"] == "30.00%"
    assert captured["BE DTI"] == "40.00%"
