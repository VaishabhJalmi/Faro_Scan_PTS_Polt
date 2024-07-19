import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

def read_pts_file(file_path):
    """Reads a PTS file and returns the data as a NumPy array."""
    with open(file_path, 'r') as file:
        data = np.loadtxt(file, skiprows=1)
    return data

def plot_3d(data):
    """Plots 3D data using pyvista."""
    x, y, z = data[:, 0], data[:, 1], data[:, 2]
    intensity = data[:, 3] if data.shape[1] > 3 else np.linalg.norm(data[:, :3], axis=1)
    
    point_cloud = pv.PolyData(np.column_stack((x, y, z)))
    point_cloud['intensity'] = intensity

    plotter = pv.Plotter()
    plotter.add_mesh(point_cloud, scalars='intensity', cmap='viridis', point_size=5, render_points_as_spheres=True)
    plotter.add_scalar_bar(title='Intensity')
    plotter.show()

def plot_1d_changes(data):
    """Plots 1D changes in pattern using matplotlib."""
    intensity = data[:, 3] if data.shape[1] > 3 else np.linalg.norm(data[:, :3], axis=1)
    changes = np.diff(intensity, prepend=intensity[0])

    plt.figure(figsize=(10, 4))
    plt.plot(changes, color='blue', label='Change in Pattern')
    plt.scatter(range(len(changes)), changes, c=changes, cmap='viridis')
    plt.colorbar(label='Change Intensity')
    plt.title('Changes in Pattern')
    plt.xlabel('Point Index')
    plt.ylabel('Change Intensity')
    plt.legend()
    plt.show()

# Main code
file_path = r'C:\Users\vaish\OneDrive\Documents\projects\PTS_file_plot\pts\4ft.pts'  # Replace with your PTS file path
data = read_pts_file(file_path)

# Plot 3D data
plot_3d(data)

# Plot 1D changes
plot_1d_changes(data)
