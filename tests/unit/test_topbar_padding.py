import streamlit as st
from ui.topbar import render_topbar


def test_topbar_removes_padding(monkeypatch):
    captured = []

    def fake_markdown(html, unsafe_allow_html=False):
        captured.append(html)

    class DummyColumn:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def selectbox(self, *a, **k):
            options = a[1] if len(a) > 1 else []
            return options[0] if options else None
        def number_input(self, *a, **k):
            return 0.0
        def button(self, *a, **k):
            return False
        def markdown(self, *a, **k):
            pass

    monkeypatch.setattr(st, 'markdown', fake_markdown)
    monkeypatch.setattr(st, 'container', lambda: DummyColumn())
    monkeypatch.setattr(
        st,
        'columns',
        lambda *a, **k: [DummyColumn() for _ in range((a[0] if isinstance(a[0], int) else len(a[0])) if a else 1)],
    )
    monkeypatch.setattr(st, 'selectbox', lambda *a, **k: a[1][0] if len(a) > 1 and a[1] else None)
    monkeypatch.setattr(st, 'button', lambda *a, **k: False)
    monkeypatch.setattr(st, 'number_input', lambda *a, **k: 0.0)

    st.session_state.clear()
    st.session_state['scenarios'] = {'Default': {'borrowers': {1: {'first_name': '', 'last_name': ''}}}}
    st.session_state['scenario_name'] = 'Default'

    render_topbar()

    assert any('div.block-container{padding-top:0' in html for html in captured)
