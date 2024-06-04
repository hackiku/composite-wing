import os
from stl import mesh
import plotly.graph_objects as go
import numpy as np

def apply_transformations(vertices, scale_factor=1.0, translation_vector=None, rotation_matrix=None):
    """Apply transformations to the vertices."""
    if scale_factor != 1.0:
        vertices *= scale_factor
    if translation_vector is not None:
        vertices += translation_vector
    if rotation_matrix is not None:
        vertices = np.dot(vertices, rotation_matrix)
    return vertices

def load_stl(stl_path: str, scale_factor=1.0, translation_vector=None, rotation_matrix=None):
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
            xaxis=dict(visible=True),
            yaxis=dict(visible=True),
            zaxis=dict(visible=True)
        ))

        return fig
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def get_model_files(models_path='./models/'):
    """Get a list of STL files from the specified directory."""
    return [f for f in os.listdir(models_path) if f.endswith('.stl')]

def main():
    models_path = './models/'
    model_files = get_model_files(models_path)

    print("Available STL files:")
    for i, file in enumerate(model_files):
        print(f"{i + 1}. {file}")

    selected_index = int(input("Select an STL file by number: ")) - 1
    if 0 <= selected_index < len(model_files):
        model_path = os.path.join(models_path, model_files[selected_index])
        print(f"Selected file: {model_path}")

        # Example transformations
        scale_factor = 1.0
        translation_vector = np.array([0, 0, -100])
        rotation_matrix = np.eye(3)  # No rotation

        fig = load_stl(model_path, scale_factor, translation_vector, rotation_matrix)
        if fig:
            fig.show()
    else:
        print("Invalid selection")

if __name__ == "__main__":
    main()
