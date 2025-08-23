import streamlit as st
import ui.layout as layout


def test_layout_smoke(monkeypatch):
    st.session_state.clear()
    scn = {"income_cards": [], "debt_cards": [], "housing": {}}

    col_meta = {}

    def fake_columns(spec):
        col_meta["n"] = len(spec) if isinstance(spec, (list, tuple)) else spec
        class DummyCol:
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc, tb):
                return False
        return DummyCol(), DummyCol(), DummyCol()

    monkeypatch.setattr(st, "columns", fake_columns)

    prop_called = {"called": False}

    def fake_render_property_panel(scn):
        prop_called["called"] = True

    monkeypatch.setattr(layout, "render_property_panel", fake_render_property_panel)

    layout.render_layout(scn)

    assert col_meta["n"] == 3
    assert prop_called["called"] is True
