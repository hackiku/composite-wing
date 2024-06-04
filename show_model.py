import streamlit as st
from stl import mesh
import plotly.graph_objects as go
import numpy as np
import os

def load_show(stl_path: str):
    try:
        your_mesh = mesh.Mesh.from_file(stl_path)
        
        # Extract vertices and faces
        vertices = your_mesh.vectors.reshape(-1, 3)
        faces = np.arange(len(vertices), dtype=np.int32).reshape(-1, 3)

        # Prepare data for Plotly
        x, y, z = vertices.T
        i, j, k = faces.T

        fig = go.Figure(data=[go.Mesh3d(
            x=x, y=y, z=z,
            i=i, j=j, k=k,
            color='orange',
            opacity=0.50
        )])

        fig.update_layout(scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        ))

        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error loading model: {e}")

def main():
    st.title('Interactive 3D Model Viewer in Streamlit')

    models_path = './models/'
    model_files = [f for f in os.listdir(models_path) if f.endswith('.stl')]

    selected_model = st.selectbox("Select an STL file", model_files)
    model_path = os.path.join(models_path, selected_model)

    if selected_model:
        st.success("Selected file: " + str(model_path))
        
        load_show(model_path)
        # if st.button('Show Mesh'):
            # load_show(model_path)

if __name__ == "__main__":
    main()
