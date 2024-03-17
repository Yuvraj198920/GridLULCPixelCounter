import tkinter as tk
from tkinter import filedialog, messagebox
from create_grid import create_grid


def browse_file():
    filename = filedialog.askopenfilename(
        title="Select a Raster File", filetypes=[("TIFF files", "*.tif")]
    )
    entry_input_raster.delete(0, tk.END)
    entry_input_raster.insert(0, filename)


def browse_output_file():
    filename = filedialog.asksaveasfilename(
        title="Select Output Grid File",
        defaultextension=".shp",
        filetypes=[("Shapefile", "*.shp")],
    )
    entry_output_grid.delete(0, tk.END)
    entry_output_grid.insert(0, filename)


def run_script():
    input_raster = entry_input_raster.get()
    output_grid = entry_output_grid.get()
    grid_size = float(entry_grid_size.get())

    if not output_grid:
        messagebox.showerror("Error", "Please specify the output grid file path.")
        return

    try:
        create_grid(input_raster, output_grid, grid_size)
        messagebox.showinfo("Success", "Grid created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create grid: {e}")


# Create the main window
root = tk.Tk()
root.title("Create Grid Tool")

# Input raster file
tk.Label(root, text="Input Raster:").grid(row=0, column=0, sticky="e")
entry_input_raster = tk.Entry(root, width=50)
entry_input_raster.grid(row=0, column=1)
tk.Button(root, text="Browse...", command=browse_file).grid(row=0, column=2)

# Output grid file
tk.Label(root, text="Output Grid File:").grid(row=2, column=0, sticky="e")
entry_output_grid = tk.Entry(root, width=50)
entry_output_grid.grid(row=2, column=1)
tk.Button(root, text="Browse...", command=browse_output_file).grid(row=2, column=2)

# Grid size
tk.Label(root, text="Grid Size (meters):").grid(row=3, column=0, sticky="e")
entry_grid_size = tk.Entry(root, width=10)
entry_grid_size.grid(row=3, column=1, sticky="w")

# Run button
tk.Button(root, text="Create Grid", command=run_script).grid(
    row=4, column=1, sticky="e"
)

# Run the main loop
root.mainloop()
