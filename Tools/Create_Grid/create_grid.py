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

    # Convert grid size from meters to degrees if needed
    srs = osr.SpatialReference(wkt=raster.GetProjectionRef())
    if srs.IsGeographic():
        avg_latitude = (y_max + y_min) / 2
        grid_size_degrees = meters_to_degrees(grid_size_meters, avg_latitude)
    else:
        grid_size_degrees = grid_size_meters

    # Create the output shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(output_grid):
        driver.DeleteDataSource(output_grid)
    grid_ds = driver.CreateDataSource(output_grid)

    # Set the spatial reference based on the input raster
    layer = grid_ds.CreateLayer(
        os.path.splitext(os.path.basename(output_grid))[0],
        srs,
        geom_type=ogr.wkbPolygon,
    )

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

    # Close the shapefile
    grid_ds.Destroy()
