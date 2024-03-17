import os
import sys
from osgeo import gdal, ogr, osr
import math


def meters_to_degrees(meters, latitude):
    # Convert latitude to radians
    lat_rad = math.radians(latitude)
    # Calculate the number of degrees
    degrees = meters / (111320 * math.cos(lat_rad))
    return degrees


def create_grid(input_raster, output_grid, grid_size_meters):
    # Open the raster file
    raster = gdal.Open(input_raster)
    if raster is None:
        print(f"Failed to open raster file {input_raster}")
        sys.exit(1)

    # Get raster georeference info
    transform = raster.GetGeoTransform()
    x_min = transform[0]
    y_max = transform[3]

    cols = raster.RasterXSize
    rows = raster.RasterYSize

    # Calculate the extent of the raster
    x_max = x_min + (cols * transform[1])
    y_min = y_max + (rows * transform[5])

    # Convert grid size from meters to degrees
    # Use the average latitude for the conversion
    avg_latitude = (y_max + y_min) / 2
    grid_size_degrees = meters_to_degrees(grid_size_meters, avg_latitude)
    num_cells_x = math.ceil((x_max - x_min) / grid_size_degrees)
    num_cells_y = math.ceil((y_max - y_min) / grid_size_degrees)
    expected_total_cells = num_cells_x * num_cells_y
    # Create the output shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(output_grid):
        driver.DeleteDataSource(output_grid)
    grid_ds = driver.CreateDataSource(output_grid)

    # Set the spatial reference based on the input raster
    srs = osr.SpatialReference()
    srs.ImportFromWkt(raster.GetProjectionRef())

    # Create the layer
    layer = grid_ds.CreateLayer("grid_90_2", srs, geom_type=ogr.wkbPolygon)

    # Add an ID field
    id_field = ogr.FieldDefn("id", ogr.OFTInteger)
    layer.CreateField(id_field)

    # Generate the grid cells
    id = 0
    y = y_max
    while y > y_min:
        x = x_min
        while x < x_max:
            id += 1
            # Create a square polygon
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(x, y)
            ring.AddPoint(x + grid_size_degrees, y)
            ring.AddPoint(x + grid_size_degrees, y - grid_size_degrees)
            ring.AddPoint(x, y - grid_size_degrees)
            ring.AddPoint(x, y)

            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)

            # Create a new feature and set its geometry and ID
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetGeometry(poly)
            feature.SetField("id", id)
            layer.CreateFeature(feature)

            # Clean up
            feature.Destroy()

            x += grid_size_degrees
        y -= grid_size_degrees

    actual_total_cells = layer.GetFeatureCount()
    if actual_total_cells == expected_total_cells:
        print("Validation successful: The number of cells is correct.")
    else:
        print(
            f"Validation failed: Expected {expected_total_cells} cells, but got {actual_total_cells} cells."
        )
    # Close the shapefile
    grid_ds.Destroy()


# create_grid(
#     r"data/input/lulc_basin1988.tif", r"data/grid_output/grid_1988_from_script", 90
# )
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_grid.py <input_raster> <output_grid> <grid_size>")
        sys.exit(1)

    input_raster = sys.argv[1]
    output_grid = sys.argv[2]
    grid_size = float(sys.argv[3])

    create_grid(input_raster, output_grid, grid_size)
