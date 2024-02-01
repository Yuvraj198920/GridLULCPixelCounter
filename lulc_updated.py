import json
from osgeo import gdal
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
from rasterio.features import geometry_mask
import pandas as pd


grid_path = "data/clipped_function_2021.shp"
lulc_raster_path = "data/LULC_2021.tif"

# Load the raster layer
lulc_raster = rasterio.open(lulc_raster_path)
# Load the vector layer
vector_layer = gpd.read_file(grid_path)

# Calculate centroids for each grid cell in the vector layer
vector_layer["centroid"] = vector_layer.geometry.centroid

# Extract latitude and longitude from centroids
vector_layer["latitude"] = vector_layer.centroid.y
vector_layer["longitude"] = vector_layer.centroid.x

class_counts = []

# Map class indices to names
class_names = {
    0: "Cropland",
    1: "Forest",
    2: "Urban",
    3: "Water",
    4: "Baresoil",
    5: "Pasture",
}

for index, row in vector_layer.iterrows():
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

# Convert class_counts to DataFrame and save as CSV
df = pd.DataFrame(class_counts)
df.to_csv("data/centroids_2021_classes_updated.csv", index=False)
