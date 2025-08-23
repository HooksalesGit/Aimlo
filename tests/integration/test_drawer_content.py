import streamlit.testing.v1 as stt

SCRIPT = '''
import streamlit as st
from core.scenarios import default_scenario
from ui.sidebar_editor import render_drawer
st.session_state.clear()
scn = default_scenario()
st.session_state['drawer_open'] = True
st.session_state['active_editor'] = None
render_drawer(scn)
'''

def test_drawer_shows_boards():
    at = stt.AppTest.from_string(SCRIPT).run()
    subheaders = [el.value for el in at.sidebar.subheader]
    assert "All Income" in subheaders
    assert "All Debts/Liabilities" in subheaders
