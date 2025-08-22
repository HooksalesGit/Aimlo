"""UI helper utilities."""
import streamlit as st

def show_sidebar():
    st.session_state["sidebar_visible"] = True

def hide_sidebar():
    st.session_state["sidebar_visible"] = False

def show_bottombar():
    st.session_state["bottombar_visible"] = True

def hide_bottombar():
    st.session_state["bottombar_visible"] = False
