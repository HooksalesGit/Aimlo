import streamlit as st
from ui.sidebar_editor import render_guidance_center

def test_guidance_center_disclosures(monkeypatch):
    outputs = []
    monkeypatch.setattr(st, 'segmented_control', lambda label, opts, key=None: 'Disclosures')
    monkeypatch.setattr(st, 'caption', lambda msg: outputs.append(msg))
    render_guidance_center({}, warnings=[])
    assert outputs, 'disclosure text should be rendered'
