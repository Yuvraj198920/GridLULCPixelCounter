from concurrent.futures import ProcessPoolExecutor
import os
import geopandas as gpd
import pandas as pd
from rasterio.mask import mask
import numpy as np
import rasterio
import multiprocessing
import time
import logging
from pathlib import Path

# Setup basic configuration for logging
logging.basicConfig(
    filename="processing_errors.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

# Assuming other necessary imports are done and required functions are defined


def process_raster(input_raster_path, grid, output_path):
    """
    Process a single raster file to count pixels within grid cells.
    """
    try:
        lulc_raster = rasterio.open(input_raster_path)
        if grid.crs != lulc_raster.crs:
            vector_layer = grid.to_crs(lulc_raster.crs)
        vector_layer["centroid"] = vector_layer.geometry.centroid
        vector_layer["latitude"] = vector_layer.centroid.y
        vector_layer["longitude"] = vector_layer.centroid.x

        class_counts = []
        class_names = {
            0: "Cropland",
            1: "Forest",
            2: "Urban",
            3: "Water",
            4: "Baresoil",
            5: "Pasture",
        }
    except Exception as e:
        logging.error(f"Failed to process {input_raster_path}: {e}")
        return

    for index, row in vector_layer.iterrows():
        # The rest of your processing logic...
        geom = [row["geometry"].__geo_interface__]

        # Mask the raster to the current grid cell
        try:
            out_image, out_transform = mask(lulc_raster, geom, crop=True, nodata=-9999)
        except ValueError as e:
            logging.warning(
                f"Skipping geometry {row['id']} in {input_raster_path} due to error: {e}"
            )
            continue  # Skip to the next geometry

        out_image = out_image[0]  # Assuming single band

        # Initialize named_counts with default values
        named_counts = {class_name: 0 for class_name in class_names.values()}
        named_counts["grid_id"] = row["id"]  # Assuming there's an 'id' column
        named_counts["latitude"] = row["latitude"]
        named_counts["longitude"] = row["longitude"]

        # Count pixels of each class if the grid cell overlaps with raster data
        if not np.all(out_image == lulc_raster.nodata):
            unique, counts = np.unique(out_image, return_counts=True)
            count_dict = dict(zip(unique, counts))

            # Update named_counts with actual counts, excluding NoData values
            for k, v in count_dict.items():
                if k in class_names and k != lulc_raster.nodata:
                    named_counts[class_names[k]] = v

        # Append the counts (or defaults for non-overlapping cells) to the list
        class_counts.append(named_counts)
    # Save the DataFrame for this raster
    df = pd.DataFrame(class_counts)
    df.to_csv(output_path, index=False)


def main():
    start_time = time.perf_counter()

    grid_shapefile = gpd.read_file("data/grid_output/common_grid.shp")
    input_dir = "data/input"
    output_dir = "data/output_parallel"
    raster_files = [f for f in os.listdir(input_dir) if f.endswith(".tif")]

    num_cores = multiprocessing.cpu_count()
    print(f"number of cores are {num_cores}")
    # Use ProcessPoolExecutor to execute the rasters in parallel
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = []
        for raster_file in raster_files:
            input_raster_path = os.path.join(input_dir, raster_file)
            output_csv_path = os.path.join(
                output_dir, os.path.splitext(raster_file)[0] + "_pixel_counts.csv"
            )
            # Submit each raster processing task to the pool
            futures.append(
                executor.submit(
                    process_raster, input_raster_path, grid_shapefile, output_csv_path
                )
            )
        for future in futures:
            future.result()
        # Optional: Wait for all futures to complete if you need to aggregate results or handle exceptions

    end_time = time.perf_counter()
    # Calculate the execution time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


if __name__ == "__main__":
    main()
