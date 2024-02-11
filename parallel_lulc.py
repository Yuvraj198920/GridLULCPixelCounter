from concurrent.futures import ProcessPoolExecutor
import os
import geopandas as gpd
import pandas as pd
from rasterio.mask import mask
import numpy as np
import rasterio
import multiprocessing
from multiprocessing import process, Queue
import time
import logging
from pathlib import Path

from combine_csv import aggregate_csv_median

import traceback

# Setup basic configuration for logging
logging.basicConfig(
    filename="processing_errors.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

# Assuming other necessary imports are done and required functions are defined


def process_raster(input_raster_path, grid, output_path, queue=None):
    """
    Process a single raster file to count pixels within grid cells.
    """
    try:
        lulc_raster = rasterio.open(input_raster_path)
        logging.info(f"Opened raster file: {input_raster_path}")
        if grid.crs != lulc_raster.crs:
            vector_layer = grid.to_crs(lulc_raster.crs)
        else:
            vector_layer = grid
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

        for index, row in vector_layer.iterrows():
            # The rest of your processing logic...
            geom = [row["geometry"].__geo_interface__]

            # Mask the raster to the current grid cell
            try:
                out_image, out_transform = mask(
                    lulc_raster, geom, crop=True, nodata=-9999
                )
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
        if not df.empty:
            df.to_csv(output_path, index=False)
            logging.info(f"CSV written successfully: {output_path}")
            if queue:
                queue.put(
                    {"message": f"CSV written for {input_raster_path}", "progress": 100}
                )
        else:
            logging.warning(f"DataFrame is empty for {input_raster_path}")
            if queue:
                queue.put(
                    {
                        "message": f"No data to write for {input_raster_path}",
                        "progress": 100,
                    }
                )
    except Exception as e:
        # Log the error with traceback information
        logging.error(
            f"Error processing {input_raster_path}: {e}\n{traceback.format_exc()}"
        )
        if queue:
            queue.put({"error": f"Error processing {input_raster_path}: {str(e)}"})
