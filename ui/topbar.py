import streamlit as st
from core import presets as P
def render_topbar():
    st.markdown("""<style>.topbar{position:sticky;top:0;z-index:999;background:var(--background-color);padding:6px 6px;border-bottom:1px solid #eee}</style>""", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='topbar'>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns([2,5,3])
        with c1: st.markdown("### Aimlo")
        with c2:
            colA,colB,colC=st.columns(3)
            program_options=list(P.PROGRAM_PRESETS.keys())
            default_program=st.session_state.get("program", program_options[0])
            idx=program_options.index(default_program) if default_program in program_options else 0
            selected_program=colA.selectbox("Program", program_options, index=idx)
            st.session_state["program"]=selected_program
            fe_default=P.PROGRAM_PRESETS[selected_program]["fe_target"]
            be_default=P.PROGRAM_PRESETS[selected_program]["be_target"]
            st.session_state.setdefault("fe_target", fe_default); st.session_state.setdefault("be_target", be_default)
            st.session_state["fe_target"]=colB.number_input("FE Target", value=float(st.session_state["fe_target"]), min_value=0.0, max_value=1.0, step=0.01)
            st.session_state["be_target"]=colC.number_input("BE Target", value=float(st.session_state["be_target"]), min_value=0.0, max_value=1.0, step=0.01)
        with c3:
            scenarios = st.session_state["scenarios"]; names = list(scenarios.keys())
            current = st.session_state.get("scenario_name", names[0])
            idx = names.index(current) if current in names else 0
            cols = st.columns([3,1,1,1])
            choose = cols[0].selectbox("Scenario", names, index=idx, key="scenario_select")
            if choose != current:
                st.session_state["scenario_name"]=choose; st.experimental_rerun()
            if cols[1].button("＋", help="New scenario"):
                base=names[0]; scenarios[f"Scenario {len(names)+1}"] = {**scenarios[base]}; st.session_state["scenario_name"]=f"Scenario {len(names)+1}"; st.experimental_rerun()
            if cols[2].button("⧉", help="Duplicate current"):
                import copy; scenarios[current + " (copy)"] = copy.deepcopy(scenarios[current]); st.session_state["scenario_name"]=current + " (copy)"; st.experimental_rerun()
            if cols[3].button("🗑", help="Delete current"):
                if len(scenarios)>1: scenarios.pop(current, None); st.session_state["scenario_name"]=list(scenarios.keys())[0]; st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
