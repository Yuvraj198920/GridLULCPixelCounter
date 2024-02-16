# Import necessary modules and functions
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import geopandas as gpd
import time
from combine_csv import aggregate_csv_median
from parallel_lulc import process_raster
import logging

# Setup logging
logging.basicConfig(
    filename="processing_errors.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def start_processing(grid_path, input_dir, output_dir, combined_csv_path, queue):
    start_time = time.perf_counter()
    grid_shapefile = gpd.read_file(grid_path)

    raster_files = [f for f in os.listdir(input_dir) if f.endswith(".tif")]
    total_rasters = len(raster_files)
    try:
        with ProcessPoolExecutor() as executor:
            # Dictionary to keep track of raster to future mapping
            future_to_raster = {
                executor.submit(
                    process_raster,
                    os.path.join(input_dir, rf),
                    grid_shapefile,
                    os.path.join(
                        output_dir, f"{os.path.splitext(rf)[0]}_pixel_counts.csv"
                    ),
                ): rf
                for rf in raster_files
            }

            for future in as_completed(future_to_raster):
                raster = future_to_raster[future]
                try:
                    # Attempt to get the result of the future
                    result = future.result()
                    rasters_processed += 1
                    progress = (rasters_processed / total_rasters) * 100
                    logging.info(f"Successfully processed {raster}")
                    # Send progress update to the GUI
                    queue.put(
                        {
                            "progress": progress,
                            "message": f"Successfully processed {raster}",
                        }
                    )
                except Exception as e:
                    logging.error(f"Error processing {raster}: {str(e)}")
                    # Send error message to the GUI
                    queue.put(
                        {"error": str(e), "message": f"Error processing {raster}"}
                    )

        aggregate_csv_median(output_dir, combined_csv_path)
        end_time = time.perf_counter()
        logging.info(f"Processing completed in {end_time - start_time} seconds")
    # Notify the GUI that processing is complete
    except Exception as e:
        logging.error(f"Unhandled exception in subprocess: {e}")
    queue.put(
        {
            "complete": True,
            "message": "Processing and aggregation completed successfully.",
        }
    )


def update_progress(progress, message):
    # Placeholder for updating progress, e.g., updating a GUI progress bar or printing to console
    print(f"{message} Progress: {progress}%")


# def main():
#     # Define static paths for testing
#     grid_path = "data\grid_output\common_grid_original.shp"
#     input_dir = "data\input"
#     output_dir = "data\output_parallel_tool"
#     combined_csv_path = "data\output_parallel_tool\combined_output.csv"

#     # Call start_processing with static variables
#     print("Starting processing with static variables...")
#     start_processing(
#         grid_path, input_dir, output_dir, combined_csv_path, update_progress
#     )


# if __name__ == "__main__":
#     main()
