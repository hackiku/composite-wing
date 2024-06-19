# cad/cad_ui.py
# URL: [Insert URL here]

import streamlit as st
from cad.presets import aircraft_presets, onshape_projects
from cad.fetch_stl import fetch_stl
from cad.display_stl import load_stl
from cad.onshape_variables import fetch_onshape_variables

def cad_ui():
    if 'stl_model' not in st.session_state:
        st.session_state.stl_model = None
        st.session_state.selected_wing_model = "None"
        st.session_state.variables = {}

    selected_aircraft = st.session_state.current_preset
    selected_wing_model = st.selectbox("Wing Model", options=["None"] + list(aircraft_presets[selected_aircraft]['model'].keys()))
    
    if selected_wing_model != "None" and st.session_state.selected_wing_model != selected_wing_model:
        st.session_state.selected_wing_model = selected_wing_model
        with st.spinner('Fetching STL model and variables...'):
            try:
                project = aircraft_presets[selected_aircraft]['model']['project']
                eid = aircraft_presets[selected_aircraft]['model'][selected_wing_model]
                did = onshape_projects[project]['did']
                wv = onshape_projects[project]['wv']
                wvid = onshape_projects[project]['wvid']

                stl_content = fetch_stl(did, wv, wvid, eid)
                stl_path = f"/tmp/{selected_aircraft}_{selected_wing_model}_model.stl"
                with open(stl_path, 'wb') as f:
                    f.write(stl_content)
                st.session_state.stl_model = load_stl(stl_path)
                st.session_state.variables = fetch_onshape_variables.fetch_custom_variables(did, wv, wvid, eid)
            except Exception as e:
                st.error(f"Error: {e}")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.number_input('Span (mm)', value=st.session_state.variables.get('span', {}).get('value', 1200), key='span')
        st.number_input('Root (mm)', value=st.session_state.variables.get('root', {}).get('value', 400), key='root')
        st.number_input('Tip (mm)', value=st.session_state.variables.get('tip', {}).get('value', 100), key='tip')
        st.number_input('Front Sweep (deg)', value=st.session_state.variables.get('wing_sweep', {}).get('value', 20), key='front_sweep')
        st.number_input('Rib Increment (mm)', value=st.session_state.variables.get('rib_inc', {}).get('value', 20), key='rib_inc')
        st.write(f"Number of ribs = `{int(st.session_state.variables.get('rib_num_total', {}).get('value', 12))}`")

        if st.button("Update STL model", type="primary"):
            if st.session_state.selected_wing_model != "None":
                updated_variables = {
                    "span": st.session_state.span,
                    "root": st.session_state.root,
                    "tip": st.session_state.tip,
                    "front_sweep": st.session_state.front_sweep,
                    "rib_inc": st.session_state.rib_inc,
                    "rib_num_total": int(st.session_state.variables.get('rib_num_total', {}).get('value', 12)),
                }
                try:
                    fetch_onshape_variables.update_custom_variables(did, wv, wvid, eid, updated_variables)
                    st.success("Parameters applied and model updated.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("No Wing Model selected.")

    with col2:
        if st.session_state.stl_model:
            st.plotly_chart(st.session_state.stl_model)

    st.json(st.session_state.variables, expanded=False)