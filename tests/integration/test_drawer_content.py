import streamlit.testing.v1 as stt

SCRIPT = '''
import streamlit as st
from core.scenarios import default_scenario
from ui.sidebar_editor import render_drawer
st.session_state.clear()
scn = default_scenario()
st.session_state['active_editor'] = None
render_drawer(scn)
'''

def test_drawer_shows_placeholder():
    at = stt.AppTest.from_string(SCRIPT).run()
    infos = [el.value for el in at.sidebar.info]
    assert "Select a card to edit" in infos
