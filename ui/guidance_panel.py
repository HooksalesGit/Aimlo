"""Simple contextual guidance panel.

This component renders markdown pulled from the guidance packs. It is a
lightweight placeholder intended to validate the data-driven approach.
"""
import streamlit as st

from core import guidance


def render_guidance_panel():
    """Render a minimal guidance panel below the top bar."""
    if "guidance" not in st.session_state:
        return
    ctx = st.session_state.get("active_context", {"type": None, "field": None})
    program = st.session_state.get("active_program", "conventional")

    tabs = st.tabs(["Disclosures", "Guides", "Warnings", "Where to find"])

    with tabs[1]:  # Guides
        if ctx.get("field"):
            hint = guidance.get_field_hint(ctx["type"], ctx["field"])
            if hint:
                st.markdown(f"**{hint.get('label', '')}**")
                st.write(hint.get("what_it_is", ""))
                note = hint.get("program_notes", {}).get(program)
                if note:
                    st.caption(note)
            else:
                st.write("No guidance available.")
        elif ctx.get("type"):
            overview = guidance.get_type_hint(ctx["type"]).get("_overview", {})
            st.markdown(f"**{overview.get('label', '')}**")
            st.write(overview.get("what_it_is", ""))
        else:
            st.caption("Select a card or field to see guidance.")

