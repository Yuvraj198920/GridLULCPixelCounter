import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from queue import Queue, Empty
from start_processing import start_processing


class RasterProcessingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Raster Processing Tool")
        self.geometry("500x300")

        # Grid Path Entry
        tk.Label(self, text="Grid Shapefile:").grid(row=0, sticky=tk.W, padx=10, pady=5)
        self.grid_path_entry = tk.Entry(self, width=40)
        self.grid_path_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_grid_path).grid(
            row=0, column=2, padx=10, pady=5
        )

        # Input Directory Entry
        tk.Label(self, text="Input Directory:").grid(
            row=1, sticky=tk.W, padx=10, pady=5
        )
        self.input_dir_entry = tk.Entry(self, width=40)
        self.input_dir_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_input_dir).grid(
            row=1, column=2, padx=10, pady=5
        )

        # Output Directory Entry
        tk.Label(self, text="Output Directory:").grid(
            row=2, sticky=tk.W, padx=10, pady=5
        )
        self.output_dir_entry = tk.Entry(self, width=40)
        self.output_dir_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_output_dir).grid(
            row=2, column=2, padx=10, pady=5
        )

        # Combined CSV File Path Entry
        tk.Label(self, text="Combined CSV Path:").grid(
            row=3, sticky=tk.W, padx=10, pady=5
        )
        self.combined_csv_entry = tk.Entry(self, width=40)
        self.combined_csv_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_combined_csv).grid(
            row=3, column=2, padx=10, pady=5
        )

        # Start Processing Button
        self.process_button = tk.Button(
            self, text="Start Processing", command=self.on_process_button_click
        )
        self.process_button.grid(row=4, column=1, pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=100, mode="determinate"
        )
        self.progress.grid(row=5, column=0, columnspan=3, padx=10, pady=20, sticky="ew")
        self.progress.grid_remove()
        # Cancel Button
        self.cancel_button = tk.Button(
            self, text="Cancel", command=self.cancel_processing, state=tk.DISABLED
        )
        self.cancel_button.grid(row=6, column=1, pady=10)

        # Queue for inter-thread communication
        self.queue = Queue()

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
        # Disabling the process button and enabling the cancel button
        self.process_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        # Reset progress bar
        self.progress["value"] = 0
        self.progress.grid()
        # Starting the processing in a separate thread
        self.processing_thread = threading.Thread(
            target=self.run_processing, daemon=True
        )
        self.processing_thread.start()
        # Start checking the queue for messages and progress updates
        self.after(100, self.check_queue)

    def run_processing(self):
        grid_path = self.grid_path_entry.get()
        input_dir = self.input_dir_entry.get()
        output_dir = self.output_dir_entry.get()
        combined_csv_path = self.combined_csv_entry.get()
        start_processing(
            grid_path, input_dir, output_dir, combined_csv_path, self.queue
        )

    def reset_ui(self):
        self.process_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.progress.grid_remove()

    def check_queue(self):
        try:
            while True:  # Process all available messages
                message = self.queue.get_nowait()
                if "progress" in message:
                    print(f"Updating progress: {message['progress']}")
                    # Update the progress bar with the value from the message
                    self.progress["value"] = message["progress"]
                elif "complete" in message and message["complete"]:
                    # Handle completion message
                    messagebox.showinfo("Success", "Processing completed successfully.")
                    self.reset_ui()
                # Add handling for other message types as necessary
        except Empty:
            pass  # No more messages to process
        finally:
            # Schedule the next check if the processing thread is still active
            if self.processing_thread.is_alive():
                self.after(100, self.check_queue)

    def cancel_processing(self):
        # Implement functionality to safely terminate processing if possible
        print("Cancel feature needs proper implementation to safely stop processing.")
        self.reset_ui()


if __name__ == "__main__":
    app = RasterProcessingApp()
    app.mainloop()
