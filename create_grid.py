import os
import geopandas as gpd
import rasterio
from shapely.geometry import box

def generate_grid_based_on_raster_extent_in_utm(raster_path, grid_size, output_path):
    """
    Generates a square grid overlay for a raster's extent in a UTM projection.

    Parameters:
    - raster_path: Path to the input raster file.
    - grid_size: The desired size of each grid cell in meters.
    - output_path: Path where the generated grid shapefile will be saved.
    """
    # Open the raster file to read its bounds and CRS
    with rasterio.open(raster_path) as dataset:
        bounds = dataset.bounds
        crs = dataset.crs

        # Calculate the number of grid cells needed to cover the raster
        width_in_cells = (bounds.right - bounds.left) // grid_size
        height_in_cells = (bounds.top - bounds.bottom) // grid_size

        # Generate grid cells
        grid_cells = []
        for i in range(int(width_in_cells) + 1):
            for j in range(int(height_in_cells) + 1):
                left = bounds.left + (i * grid_size)
                top = bounds.top - (j * grid_size)
                right = left + grid_size
                bottom = top - grid_size
                
                # Create a box (polygon) for each cell and add it to the list
                grid_cells.append(box(left, bottom, right, top))

        # Create a GeoDataFrame to hold the grid cells
        grid = gpd.GeoDataFrame(grid_cells, columns=['geometry'], crs=crs)

        # Save the grid to a new Shapefile
        grid.to_file(output_path)

# Example usage
if __name__ == "__main__":
    raster_path = "data/input/LULC_ourthe1988.tif"
    grid_size = 270  # in meters
    output_path = "data/grid_output/LULC_ourthe1988_grid.shp"
    generate_grid_based_on_raster_extent_in_utm(raster_path, grid_size, output_path)


