import streamlit as st

from ui import layout
import ui.sidebar_editor as sidebar_editor
from ui.sidebar_editor import render_drawer
from ui.summary_band import render_summary_band
from ui.utils import show_sidebar, hide_sidebar
from ui.cards_income import select_income_card


def test_sidebar_summary_smoke(monkeypatch):
    st.session_state.clear()
    scn = {"income_cards": [{"id": "abc", "type": "W-2", "payload": {}}], "debt_cards": [], "housing": {}}

    # Toggle drawer open/close
    show_sidebar()
    assert st.session_state["drawer_open"] is True
    hide_sidebar()
    assert st.session_state["drawer_open"] is False

    # Layout still renders 3 columns when drawer is hidden
    col_meta = {}

    def fake_columns(spec):
        n = len(spec) if isinstance(spec, (list, tuple)) else spec
        if "n" not in col_meta:
            col_meta["n"] = n
        class DummyCol:
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc, tb):
                return False
        return tuple(DummyCol() for _ in range(n))

    monkeypatch.setattr(st, "columns", fake_columns)
    layout.render_layout(scn)
    assert col_meta["n"] == 3

    # Auto-open drawer when selecting a card while hidden
    st.session_state["active_editor"] = None
    hide_sidebar()
    select_income_card("abc")
    monkeypatch.setattr(sidebar_editor, "render_context_form", lambda *a, **k: None)
    render_drawer(scn)
    assert st.session_state["drawer_open"] is True

    # Summary band renders sticky below top bar
    captured = {}
    def fake_markdown(msg, *a, **k):
        captured.setdefault("calls", []).append(msg)
    monkeypatch.setattr(st, "markdown", fake_markdown)
    label = render_summary_band({"TotalIncome":0,"PITIA":0,"FE":0,"BE":0,"FE_target":1,"BE_target":1,"LTV":0})
    assert any("#summary_toggle" in c and "position:sticky" in c for c in captured["calls"])
    assert label.startswith("Total Income")
