import geopandas as gpd
import rasterio
from shapely.geometry import box

# Load the raster
with rasterio.open("data/LULC_2021.tif") as src:
    raster_bounds = src.bounds
    raster_crs = src.crs

# Create a bounding box polygon from the raster extent
bbox_polygon = box(*raster_bounds)

# Load the grid layer
grid = gpd.read_file("data/reprojecte_to4326_grid.shp").to_crs(raster_crs)

# Clip the grid by the bounding box
clipped_grid = gpd.clip(grid, bbox_polygon)
# Save the clipped grid to a new shapefile
clipped_grid.to_file("data/script_clipped_grid_2021.shp")
