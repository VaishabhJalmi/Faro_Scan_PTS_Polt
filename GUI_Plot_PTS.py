import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

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

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PTS files", "*.pts")])
    if file_path:
        try:
            data = read_pts_file(file_path)
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the PTS file: {e}")
    return None

def on_plot_3d():
    data = select_file()
    if data is not None:
        plot_3d(data)

def on_plot_1d():
    data = select_file()
    if data is not None:
        plot_1d_changes(data)

# GUI setup
root = tk.Tk()
root.title("PTS File Plotter - Designed by Vaishabh Jalmi")
root.geometry("400x200")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label = ttk.Label(frame, text="Select a PTS file to plot:")
label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

button_plot_3d = ttk.Button(frame, text="Plot 3D", command=on_plot_3d)
button_plot_3d.grid(row=1, column=0, padx=(0, 5))

button_plot_1d = ttk.Button(frame, text="Plot 1D", command=on_plot_1d)
button_plot_1d.grid(row=1, column=1, padx=(5, 0))

# Make the GUI responsive
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
