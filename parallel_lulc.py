from concurrent.futures import ProcessPoolExecutor
import os
import geopandas as gpd
import pandas as pd
from rasterio.mask import mask
import numpy as np
import rasterio
import multiprocessing

# Assuming other necessary imports are done and required functions are defined

def process_raster(input_raster_path, grid_path, output_path):
    """
    Process a single raster file to count pixels within grid cells.
    """
    lulc_raster = rasterio.open(input_raster_path)
    vector_layer = gpd.read_file(grid_path)
    vector_layer["centroid"] = vector_layer.geometry.centroid
    vector_layer["latitude"] = vector_layer.centroid.y
    vector_layer["longitude"] = vector_layer.centroid.x

    class_counts = []
    class_names = {0: "Cropland", 1: "Forest", 2: "Urban", 3: "Water", 4: "Baresoil", 5: "Pasture"}

    for index, row in vector_layer.iterrows():
        # The rest of your processing logic...
        geom = [row["geometry"].__geo_interface__]

        # Mask the raster to the current grid cell
        out_image, out_transform = mask(
            lulc_raster, geom, crop=True, nodata=lulc_raster.nodata
        )
        out_image = out_image[0]  # Assuming single band

        # Count pixels of each class
        unique, counts = np.unique(out_image, return_counts=True)
        count_dict = dict(zip(unique, counts))

        # Remove the count for NoData value if present
        nodata = lulc_raster.nodata
        if nodata in count_dict:
            del count_dict[nodata]

        named_counts = {v: 0 for k, v in class_names.items()}
        # Update named_counts with actual counts, leaving zeros where no pixels are found
        for k, v in count_dict.items():
            if k in class_names:  # Ensure the class is one we're interested in
                named_counts[class_names[k]] = v
        # Include centroid coordinates and the grid cell ID
        named_counts["grid_id"] = row["id"]  # Assuming there's an 'id' column in your grid
        named_counts["latitude"] = row["latitude"]
        named_counts["longitude"] = row["longitude"]

        class_counts.append(named_counts)
    # Save the DataFrame for this raster
    df = pd.DataFrame(class_counts)
    df.to_csv(output_path, index=False)

def main():
    grid_path = "data/grid_output/script_clipped_grid_2021.shp"
    input_dir = "data/input"
    output_dir = "data/output_parallel"
    raster_files = [f for f in os.listdir(input_dir) if f.endswith('.tif')]

    num_cores = multiprocessing.cpu_count()
    print(f"number of cores are {num_cores}")
    # Use ProcessPoolExecutor to execute the rasters in parallel
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = []
        for raster_file in raster_files:
            input_raster_path = os.path.join(input_dir, raster_file)
            output_csv_path = os.path.join(output_dir, os.path.splitext(raster_file)[0] + "_pixel_counts.csv")
            # Submit each raster processing task to the pool
            futures.append(executor.submit(process_raster, input_raster_path, grid_path, output_csv_path))
        for future in futures:
            future.result()
        # Optional: Wait for all futures to complete if you need to aggregate results or handle exceptions

if __name__ == "__main__":
    main()
