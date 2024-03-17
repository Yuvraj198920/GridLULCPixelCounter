import tkinter as tk
from tkinter import filedialog, simpledialog
from create_grid import create_grid


def browse_file():
    filename = filedialog.askopenfilename(
        title="Select a Raster File", filetypes=[("TIFF files", "*.tif")]
    )
    entry_input_raster.delete(0, tk.END)
    entry_input_raster.insert(0, filename)


def browse_output_directory():
    directory = filedialog.askdirectory(title="Select Output Directory")
    entry_output_grid.delete(0, tk.END)
    entry_output_grid.insert(0, directory)


def run_script():
    input_raster = entry_input_raster.get()
    output_grid = entry_output_grid.get()
    grid_size = float(entry_grid_size.get())
    create_grid(input_raster, output_grid, grid_size)
    tk.messagebox.showinfo("Success", "Grid created successfully!")


# Create the main window
root = tk.Tk()
root.title("Create Grid Tool")

# Input raster file
tk.Label(root, text="Input Raster:").grid(row=0, column=0, sticky="e")
entry_input_raster = tk.Entry(root, width=50)
entry_input_raster.grid(row=0, column=1)
tk.Button(root, text="Browse...", command=browse_file).grid(row=0, column=2)

# Output grid directory
tk.Label(root, text="Output Grid:").grid(row=1, column=0, sticky="e")
entry_output_grid = tk.Entry(root, width=50)
entry_output_grid.grid(row=1, column=1)
tk.Button(root, text="Browse...", command=browse_output_directory).grid(row=1, column=2)

# Grid size
tk.Label(root, text="Grid Size (meters):").grid(row=2, column=0, sticky="e")
entry_grid_size = tk.Entry(root, width=10)
entry_grid_size.grid(row=2, column=1, sticky="w")

# Run button
tk.Button(root, text="Create Grid", command=run_script).grid(
    row=3, column=1, sticky="e"
)

# Run the main loop
root.mainloop()
