# cad/cad_ui.py
import streamlit as st
from cad.presets import aircraft_presets, onshape_projects
from cad.fetch_stl import fetch_stl
from cad.display_stl import load_stl
from cad.onshape_variables import fetch_onshape_variables
from cad.export_step import export_step_from_preset

def compose_onshape_url(project, part_type, eid):
    did = onshape_projects[project]['did']
    wv = onshape_projects[project]['wv']
    wvid = onshape_projects[project]['wvid']
    return f"https://cad.onshape.com/documents/{did}/{wv}/{wvid}/e/{eid}"

def cad_ui():
    if 'stl_model' not in st.session_state:
        st.session_state.stl_model = None
        st.session_state.variables = {}

    selected_wing_model = st.selectbox("Wing Model", options=list(aircraft_presets[st.session_state.current_preset]['model'].keys()), index=0)

    if selected_wing_model:
        project = aircraft_presets[st.session_state.current_preset]['model']['project']
        did = onshape_projects[project]['did']
        wv = onshape_projects[project]['wv']
        wvid = onshape_projects[project]['wvid']
        eid = aircraft_presets[st.session_state.current_preset]['model'][selected_wing_model]

        with st.spinner('Fetching STL model and variables...'):
            try:
                stl_content = fetch_stl(did, wv, wvid, eid)
                stl_path = f"/tmp/{selected_wing_model}_model.stl"
                with open(stl_path, 'wb') as f:
                    f.write(stl_content)
                st.session_state.stl_model = load_stl(stl_path)
                st.session_state.variables = fetch_onshape_variables(did, wv, wvid, eid)
            except Exception as e:
                st.error(f"Error: {e}")

        # Display the Onshape URL for the selected part
        part_url = compose_onshape_url(project, selected_wing_model, eid)
        st.markdown(f"[Onshape URL →]({part_url})")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.session_state.variables:
            st.number_input('Span (mm)', value=st.session_state.variables.get('span', {}).get('value', 1200), key='span')
            st.number_input('Root (mm)', value=st.session_state.variables.get('root', {}).get('value', 400), key='root')
            st.number_input('Tip (mm)', value=st.session_state.variables.get('tip', {}).get('value', 100), key='tip')
            st.number_input('Front Sweep (deg)', value=st.session_state.variables.get('wing_sweep', {}).get('value', 20), key='front_sweep')
            st.number_input('Rib Increment (mm)', value=st.session_state.variables.get('rib_inc', {}).get('value', 20), key='rib_inc')
            st.write(f"Number of ribs = `{int(st.session_state.variables.get('rib_num_total', {}).get('value', 12))}`")
            
            if st.button("Update STL model", type="primary"):
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

    with col2:
        if st.session_state.stl_model:
            st.plotly_chart(st.session_state.stl_model)

    st.json(st.session_state.variables, expanded=False)

    # Add STEP file download section
    if st.button(f"💾 Download {selected_wing_model} STEP"):
        try:
            output_directory = f'cad/step/{st.session_state.current_preset}'
            exported_file = export_step_from_preset(did, wv, wvid, eid, output_directory)
            st.success(f"Exported STEP file: {exported_file}")
        except Exception as e:
            st.error(f"Failed to export STEP file: {e}")

