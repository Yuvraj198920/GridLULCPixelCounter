import geopandas as gpd
import rasterio
from shapely.geometry import box

# Load the raster
with rasterio.open("data/input/LULC_1989.tif") as src:
    raster_bounds = src.bounds
    raster_crs = src.crs

# Create a bounding box polygon from the raster extent
bbox_polygon = box(*raster_bounds)

# Load the grid layer
grid = gpd.read_file("data/grid_output/grid_2000.shp").to_crs(raster_crs)

# Clip the grid by the bounding box
clipped_grid = gpd.clip(grid, bbox_polygon)
# Save the clipped grid to a new shapefile
clipped_grid.to_file("data/grid_output/script_clipped_grid_1989.shp")
