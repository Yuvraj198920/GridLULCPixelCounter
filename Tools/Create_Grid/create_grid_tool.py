import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from create_grid import create_grid
import threading


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

    def thread_target():
        try:
            create_grid(input_raster, output_grid, grid_size, update_progress)
            root.after(
                0, lambda: messagebox.showinfo("Success", "Grid created successfully!")
            )
        except Exception as e:
            root.after(
                0, lambda: messagebox.showerror("Error", f"Failed to create grid: {e}")
            )
        finally:
            # Reset the progress bar
            progress_var.set(0)
            progress_label.config(text="0%")

    # Run the create_grid function in a separate thread
    thread = threading.Thread(target=thread_target)
    thread.start()


def update_progress(current, total):
    percentage = int((current / total) * 100)
    progress_var.set(percentage)
    progress_label.config(text=f"{percentage}%")
    root.update_idletasks()


# Create the main window
root = tk.Tk()
root.title("Create Grid Tool")

# Input raster file
tk.Label(root, text="Input Raster:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_input_raster = tk.Entry(root, width=50)
entry_input_raster.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=browse_file).grid(
    row=0, column=2, padx=5, pady=5
)

# Output grid file
tk.Label(root, text="Output Grid File:").grid(
    row=1, column=0, sticky="e", padx=5, pady=5
)
entry_output_grid = tk.Entry(root, width=50)
entry_output_grid.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=browse_output_file).grid(
    row=1, column=2, padx=5, pady=5
)

# Grid size
tk.Label(root, text="Grid Size (meters):").grid(
    row=2, column=0, sticky="e", padx=5, pady=5
)
entry_grid_size = tk.Entry(root, width=10)
entry_grid_size.grid(row=2, column=1, sticky="w", padx=5, pady=5)

# Run button
tk.Button(root, text="Create Grid", command=run_script).grid(
    row=3, column=1, sticky="e", padx=5, pady=5
)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

# Progress label
progress_label = tk.Label(root, text="0%")
progress_label.grid(row=4, column=2, padx=5, pady=5)

# Run the main loop
root.mainloop()
