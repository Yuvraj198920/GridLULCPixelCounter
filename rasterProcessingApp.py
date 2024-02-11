import tkinter as tk
from tkinter import filedialog, messagebox
from start_processing import start_processing


class RasterProcessingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Raster Processing Tool")
        self.geometry("600x200")

        # Grid Path Entry
        tk.Label(self, text="Grid Shapefile:").grid(row=0, sticky=tk.W, padx=10, pady=5)
        self.grid_path_entry = tk.Entry(self, width=70)
        self.grid_path_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_grid_path).grid(
            row=0, column=2, padx=10, pady=5
        )

        # Input Directory Entry
        tk.Label(self, text="Input Directory:").grid(
            row=1, sticky=tk.W, padx=10, pady=5
        )
        self.input_dir_entry = tk.Entry(self, width=70)
        self.input_dir_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_input_dir).grid(
            row=1, column=2, padx=10, pady=5
        )

        # Output Directory Entry
        tk.Label(self, text="Output Directory:").grid(
            row=2, sticky=tk.W, padx=10, pady=5
        )
        self.output_dir_entry = tk.Entry(self, width=70)
        self.output_dir_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_output_dir).grid(
            row=2, column=2, padx=10, pady=5
        )

        # Combined CSV File Path Entry
        tk.Label(self, text="Combined CSV Path:").grid(
            row=3, sticky=tk.W, padx=10, pady=5
        )
        self.combined_csv_entry = tk.Entry(self, width=70)
        self.combined_csv_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_combined_csv).grid(
            row=3, column=2, padx=10, pady=5
        )

        # Start Processing Button
        tk.Button(
            self, text="Start Processing", command=self.on_process_button_click
        ).grid(row=4, column=1, pady=20)

    def browse_grid_path(self):
        filepath = filedialog.askopenfilename(filetypes=[("Shapefile", "*.shp")])
        self.grid_path_entry.delete(0, tk.END)
        self.grid_path_entry.insert(0, filepath)

    def browse_input_dir(self):
        folder_selected = filedialog.askdirectory()
        self.input_dir_entry.delete(0, tk.END)
        self.input_dir_entry.insert(0, folder_selected)

    def browse_output_dir(self):
        folder_selected = filedialog.askdirectory()
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(0, folder_selected)

    def browse_combined_csv(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        self.combined_csv_entry.delete(0, tk.END)
        self.combined_csv_entry.insert(0, filepath)

    def on_process_button_click(self):
        grid_path = self.grid_path_entry.get()
        input_dir = self.input_dir_entry.get()
        output_dir = self.output_dir_entry.get()
        combined_csv_path = self.combined_csv_entry.get()
        # Input validation (optional)
        if not grid_path or not input_dir or not output_dir or not combined_csv_path:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return
        # Call the processing function
        try:
            start_processing(grid_path, input_dir, output_dir, combined_csv_path)
            messagebox.showinfo("Success", "Processing completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = RasterProcessingApp()
    app.mainloop()
