# Import necessary modules and functions
from concurrent.futures import ProcessPoolExecutor
import os
import geopandas as gpd
from multiprocessing import Queue
import multiprocessing
import time
from combine_csv import aggregate_csv_median
from parallel_lulc import process_raster


def start_processing(grid_path, input_dir, output_dir, combined_csv_path):
    start_time = time.perf_counter()
    grid_shapefile = gpd.read_file(grid_path)  # Use grid_path from GUI input

    num_cores = multiprocessing.cpu_count()
    queue = Queue()  # Initialize Queue

    # Set up and start the multiprocessing tasks using paths provided by the GUI
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = []
        for raster_file in os.listdir(input_dir):
            if raster_file.endswith(".tif"):
                input_raster_path = os.path.join(input_dir, raster_file)
                output_csv_path = os.path.join(
                    output_dir, os.path.splitext(raster_file)[0] + "_pixel_counts.csv"
                )
                futures.append(
                    executor.submit(
                        process_raster,
                        input_raster_path,
                        grid_shapefile,
                        output_csv_path,
                        queue,
                    )
                )

        # Process messages from the queue as before
        while any([future.running() for future in futures]):
            while not queue.empty():
                message = queue.get()
                print(message)  # Or update the GUI with this message
            time.sleep(1)

    # Aggregate results into a combined CSV using the path provided by the GUI
    aggregate_csv_median(output_dir, combined_csv_path)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    # Here you might also update the GUI to inform the user that processing is complete
