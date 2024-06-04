import os
from stl import mesh
import plotly.graph_objects as go
import numpy as np

def load_stl(stl_path: str):
    """Load an STL file and return Plotly figure data for visualization."""
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

        return fig
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def get_model_files(models_path='./models/'):
    """Get a list of STL files from the specified directory."""
    return [f for f in os.listdir(models_path) if f.endswith('.stl')]
