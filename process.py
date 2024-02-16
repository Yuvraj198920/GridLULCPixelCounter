# process.py
import time


def gdal_process(file_path, output_queue):
    # Simulate GDAL processing
    print(f"Processing {file_path}")
    time.sleep(2)  # Simulate processing time
    # Placeholder for actual GDAL processing logic
    output_queue.put(f"Finished processing {file_path}")
