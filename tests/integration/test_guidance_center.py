import streamlit as st
from ui.disclosures import render_disclosures


def test_disclosures_tab(monkeypatch):
    outputs = []
    def fake_tabs(options):
        class Dummy:
            def __enter__(self):
                return None
            def __exit__(self, exc_type, exc, tb):
                return False
        return Dummy(), Dummy(), Dummy(), Dummy()
    monkeypatch.setattr(st, 'tabs', lambda opts: fake_tabs(opts))
    monkeypatch.setattr(st, 'caption', lambda msg: outputs.append(msg))
    render_disclosures([])
    assert outputs, 'disclosure text should be rendered'
