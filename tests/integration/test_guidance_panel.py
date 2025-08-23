import streamlit as st
import streamlit as st
from core.guidance import load_field_hints
from ui.guidance_panel import render_guidance_panel


def _fake_tabs(options):
    class Dummy:
        def __enter__(self):
            return None
        def __exit__(self, exc_type, exc, tb):
            return False
    return [Dummy() for _ in options]


def test_panel_switch(monkeypatch):
    load_field_hints()
    monkeypatch.setattr(st, "tabs", lambda opts: _fake_tabs(opts))
    outputs = []
    monkeypatch.setattr(st, "markdown", lambda msg: outputs.append(msg))
    monkeypatch.setattr(st, "write", lambda msg: outputs.append(msg))
    monkeypatch.setattr(st, "caption", lambda msg: outputs.append(msg))

    st.session_state["active_program"] = "conventional"
    st.session_state["active_context"] = {"type": "w2", "field": None}
    render_guidance_panel()
    assert any("W-2 Income" in o for o in outputs)

    outputs.clear()
    st.session_state["active_context"] = {"type": "w2", "field": "annual_salary"}
    render_guidance_panel()
    assert any("Annual Salary" in o for o in outputs)
