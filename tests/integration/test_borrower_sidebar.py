import streamlit as st
from contextlib import contextmanager
from core.scenarios import default_scenario
from ui.sidebar_editor import render_borrowers_editor

def test_render_borrowers_editor(monkeypatch):
    st.session_state.clear()
    scn = default_scenario()
    calls = []
    def fake_text_input(label, value="", key=None):
        calls.append(label)
        return value
    def fake_number_input(label, value=0, min_value=None, max_value=None, step=None, key=None):
        calls.append(label)
        return value
    @contextmanager
    def fake_expander(label, expanded=False):
        yield
    monkeypatch.setattr(st, "text_input", fake_text_input)
    monkeypatch.setattr(st, "number_input", fake_number_input)
    monkeypatch.setattr(st, "expander", fake_expander)
    monkeypatch.setattr(st, "button", lambda *args, **kwargs: False)
    monkeypatch.setattr(st, "subheader", lambda *args, **kwargs: None)
    render_borrowers_editor(scn)
    assert "First name" in calls
    assert "Estimated credit score" in calls


def test_remove_borrower(monkeypatch):
    st.session_state.clear()
    scn = default_scenario()
    calls = []

    def fake_text_input(label, value="", key=None):
        calls.append(label)
        return value

    def fake_number_input(label, value=0, min_value=None, max_value=None, step=None, key=None):
        calls.append(label)
        return value

    @contextmanager
    def fake_expander(label, expanded=False):
        yield

    def fake_button(label, key=None, **kwargs):
        return key == "br_rm_1"

    monkeypatch.setattr(st, "text_input", fake_text_input)
    monkeypatch.setattr(st, "number_input", fake_number_input)
    monkeypatch.setattr(st, "expander", fake_expander)
    monkeypatch.setattr(st, "button", fake_button)
    monkeypatch.setattr(st, "subheader", lambda *args, **kwargs: None)

    render_borrowers_editor(scn)
    assert 1 not in scn["borrowers"]
    assert 2 in scn["borrowers"]
