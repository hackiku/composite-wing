import os
from stl import mesh
import plotly.graph_objects as go
import numpy as np

# https://3dviewer.net/

def apply_transformations(vertices, scale_factor=1.0, translation_vector=None, rotation_matrix=None):
    """Apply transformations to the vertices."""
    if scale_factor != 1.2:
        vertices *= scale_factor
    if translation_vector is not None:
        vertices += translation_vector
    if rotation_matrix is not None:
        vertices = np.dot(vertices, rotation_matrix)
    return vertices

def load_stl(stl_path: str, scale_factor=1.0, translation_vector=None, rotation_matrix=None, width=800, height=600):
    """Load an STL file and return Plotly figure data for visualization with optional transformations."""
    try:
        your_mesh = mesh.Mesh.from_file(stl_path)
        
        # Extract vertices and faces
        vertices = your_mesh.vectors.reshape(-1, 3)
        faces = np.arange(len(vertices), dtype=np.int32).reshape(-1, 3)

        # Apply transformations if any
        vertices = apply_transformations(vertices, scale_factor, translation_vector, rotation_matrix)

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
            xaxis=dict(visible=True,  backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="gray", showbackground=True, zerolinecolor="red", title="X"),
            yaxis=dict(visible=True, backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="gray", showbackground=True, zerolinecolor="green", title="Y"),
            zaxis=dict(visible=True, backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="gray", showbackground=True, zerolinecolor="blue", title="Z")
        ), width=600, height=600)

        

        return fig
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def get_model_files(models_path='./models/'):
    """Get a list of STL files from the specified directory."""
    return [f for f in os.listdir(models_path) if f.endswith('.stl')]
